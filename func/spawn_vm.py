##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import sys
from collections import defaultdict
from func.env_setup import Env_setup
from func.fetchimg import FetchImg
import yaml
import heatclient.client
import keystoneclient
import glanceclient
from novaclient import client
import time
import json
from func.create_zones import create_zones

class SpawnVM(Env_setup):
    vm_role_ip_dict = defaultdict(list)
    installer = ''

    def __init__(self, vm_info):
        print 'SpawnVM Class initiated'
        vm_role_ip_dict = vm_info.copy()
        print 'Generating Heat Template\n'
        self._keystone_client = None
        self._heat_client = None
        self._glance_client = None
        self._nova_client = None
        nova =self. _get_nova_client()
        azoneobj = create_zones()
        azoneobj.create_agg(vm_info['availability_zone'])
        installer= self.get_installer_type()
        self.Heat_template1 = self.HeatTemplate_vm(vm_info,installer)
        self.create_stack(vm_role_ip_dict, self.Heat_template1)

    def get_installer_type(self):
        print 'Getting Installer Name'
        return os.environ['INSTALLER_TYPE']
    
    def get_public_network(self,installer_detected):
    
        '''
        TODO: GET THE NAMES OF THE PUBLIC NETWORKS for OTHER PROJECTS
        '''        
        print 'Getting Public Network'
        if installer_detected.lower() == 'fuel':
            return 'net04_ext'
        if installer_detected.lower() == 'apex':
            return 'net04_ext'
        if installer_detected.lower() == 'compass':
            return 'net04_ext'
            
    def HeatTemplate_vm(self, vm_params, installer):
        try:
            Heat_Dic=''
            with open('./heat/SampleHeat.yaml', 'r+') as H_temp:
                Heat_Dic = yaml.load(H_temp)
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                print 'Error in qtip/heat/SampleHeat.yaml at: (%s,%s)' % (mark.line + 1, mark.column + 1)
                print 'EXITING PROGRAM. Correct File and restart'
                sys.exit(0)
        fopen = open('./data/QtipKey.pub', 'r')
        fopenstr = fopen.read()
        fopenstr = fopenstr.rstrip()
        scriptcmd = '#!/bin/bash \n echo {0} >>  foo.txt \n echo {1} >> /root/.ssh/authorized_keys'.format(
            fopenstr, fopenstr)
            
        netName = self.get_public_network(installer)
        print netName
        Heat_Dic['heat_template_version'] = '2014-10-16'
        Heat_Dic['resources']['KeyPairSavePrivate'] = {
            'type': 'OS::Nova::KeyPair',
            'properties': {
                    'save_private_key': 'true',
                    'name': 'my_key'
            }
        }
        Heat_Dic['parameters']['public_network'] = {
            'type': 'string',
            #'default': vm_params['public_network'][0]
            'default': netName
        }
        for x in range(1, len(vm_params['availability_zone']) + 1):
            avail_zone = vm_params['availability_zone'][x - 1]
            img = vm_params['OS_image'][x - 1]
            flavor = vm_params['flavor'][x - 1]

            Heat_Dic['parameters']['availability_zone_' +str(x)] = {
                 'description': 'Availability Zone of the instance',
                 'default': avail_zone,
                 'type': 'string'

                 }

            Heat_Dic['resources']['public_port_' +str(x)] = {
                    'type': 'OS::Neutron::Port',
                    'properties': {
                        'network': {'get_resource': 'private_network'},
                        'security_groups': [{ 'get_resource': 'demo1_security_Group'}],
                        'fixed_ips': [
                            {'subnet_id': {'get_resource': 'private_subnet'}}]}}

            Heat_Dic['resources']['floating_ip_' + str(x)] = {
                'type': 'OS::Neutron::FloatingIP',
                'properties': {
                    'floating_network': {'get_param': 'public_network'}}}

            Heat_Dic['resources']['floating_ip_assoc_' + str(x)] = {
                'type': 'OS::Neutron::FloatingIPAssociation',
                'properties': {
                    'floatingip_id': {'get_resource': 'floating_ip_' + str(x)},
                    'port_id': {'get_resource': 'public_port_' + str(x)}}}

            Heat_Dic['resources']['my_instance_' + str(x)] = {
                'type': 'OS::Nova::Server',
                'properties': {
                    'image': img,
                    'networks':[
                    {'port': {'get_resource': 'public_port_' + str(x)}}],
                    'flavor': flavor,
                    'availability_zone': avail_zone,
                    'name': 'instance' + str(x),
                    'key_name': {'get_resource': 'KeyPairSavePrivate'},
                    'user_data_format': 'RAW',
                    'user_data': scriptcmd}}

            Heat_Dic['resources']['demo1_security_Group'] = {
                'type': 'OS::Neutron::SecurityGroup',
                'properties': {
                    'name': 'demo1_security_Group',
                    'rules': [{
                        'protocol': 'tcp',
                        'port_range_min': 22,
                        'port_range_max': 5201},
                        {'protocol': 'udp',
                        'port_range_min': 22,
                        'port_range_max': 5201},
                        {'protocol': 'icmp'}]}}

            Heat_Dic['outputs']['instance_PIP_' +str(x)] = {
                'description': 'IP address of the instance',
                'value': {'get_attr': ['my_instance_' + str(x), 'first_address']}}
            Heat_Dic['outputs']['instance_ip_' +str(x)] = {
                'description': 'IP address of the instance',
                'value': {'get_attr': ['floating_ip_' + str(x), 'floating_ip_address']}}

            Heat_Dic['outputs']['availability_instance_' + str(x)] = {
                'description': 'Availability Zone of the Instance',
                'value': { 'get_param': 'availability_zone_'+str(x)}}


        Heat_Dic['outputs']['KeyPair_PublicKey'] = {
            'description': 'Private Key',
            'value': {'get_attr': ['KeyPairSavePrivate', 'private_key']}
        }
        del Heat_Dic['outputs']['description']
        return Heat_Dic

    def _get_keystone_client(self):
        '''returns a keystone client instance'''

        if self._keystone_client is None:
            self._keystone_client = keystoneclient.v2_0.client.Client(
                auth_url=os.environ.get('OS_AUTH_URL'),
                username=os.environ.get('OS_USERNAME'),
                password=os.environ.get('OS_PASSWORD'),
                tenant_name=os.environ.get('OS_TENANT_NAME'))
        return self._keystone_client

    def _get_nova_client(self):
        if self._nova_client is None:
            keystone = self._get_keystone_client()
            self._nova_client = client.Client('2', token=keystone.auth_token)
        return self._nova_client

    def _get_heat_client(self):
        '''returns a heat client instance'''
        if self._heat_client is None:
            keystone = self._get_keystone_client()
            heat_endpoint = keystone.service_catalog.url_for(
                service_type='orchestration')
            self._heat_client = heatclient.client.Client(
                '1', endpoint=heat_endpoint, token=keystone.auth_token)
        return self._heat_client

    def _get_glance_client(self):
        if self._glance_client is None:
            keystone = self._get_keystone_client()
            glance_endpoint = keystone.service_catalog.url_for(
                service_type='image')
            self._glance_client = glanceclient.Client(
                '2', glance_endpoint, token=keystone.auth_token)
        return self._glance_client

    def create_stack(self, vm_role_ip_dict, Heat_template):

        stackname = 'QTIP'
        heat = self._get_heat_client()
        glance = self._get_glance_client()

        available_images = []
        for image_list in glance.images.list():

            available_images.append(image_list.name)

        if 'QTIP_CentOS' in available_images:
            print 'Image Present'

        elif 'QTIP_CentOS' not in available_images:
            fetchImage = FetchImg()
            fetchImage.download()
            print 'Uploading Image to Glance. Please wait'
            qtip_image = glance.images.create(
                name='QTIP_CentOS',
                visibility='public',
                disk_format='qcow2',
                container_format='bare')
            qtip_image = glance.images.upload(
                qtip_image.id, open('./Temp_Img/QTIP_CentOS.qcow2'))
        json_temp = json.dumps(Heat_template)

        for checks in range(3):
            for prev_stacks in heat.stacks.list():

                if prev_stacks.stack_name == 'QTIP':
                    print 'QTIP Stacks exists.\nDeleting Existing Stack'
                    heat.stacks.delete('QTIP')
                    time.sleep(10)

        print '\nStack Creating Started\n'

        try:
            heat.stacks.create(stack_name=stackname, template=Heat_template)
        except:
            print 'Create Failed :( '

        cluster_detail = heat.stacks.get(stackname)
        while(cluster_detail.status != 'COMPLETE'):
            if cluster_detail.status == 'IN_PROGRESS':
                print 'Stack Creation in Progress'
            cluster_detail = heat.stacks.get(stackname)
            time.sleep(10)
        print 'Stack Created'
        print 'Getting Public IP(s)'
        zone = []
        s=0
        for vm in range(len(vm_role_ip_dict['OS_image'])):

            for I in cluster_detail.outputs:
                availabilityKey = 'availability_instance_'+str(vm+1)

                if I['output_key'] == availabilityKey:
                    zone.insert(s,str(I['output_value']))
                    s=s+1
            for i in cluster_detail.outputs:
                instanceKey = "instance_ip_" + str(vm + 1)
                privateIPkey = 'instance_PIP_' + str(vm +1)
                if i['output_key'] == instanceKey:
                    Env_setup.roles_dict[vm_role_ip_dict['role'][vm]].append(
                                                        str(i['output_value']))
                    Env_setup.ip_pw_list.append((str(i['output_value']),''))

                if i['output_key'] == privateIPkey:
                    Env_setup.ip_pw_dict[vm_role_ip_dict['role'][vm]]=str(i['output_value'])
                if i['output_key'] == 'KeyPair_PublicKey':
                    sshkey = str(i['output_value'])

        with open('./data/my_key.pem', 'w') as fopen:
            fopen.write(sshkey)
        fopen.close()
        print Env_setup.ip_pw_list
