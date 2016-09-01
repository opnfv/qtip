##############################################################################
# Copyright (c) 2016 Dell Inc, ZTE  and others.
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
from func.create_zones import AvailabilityZone
import json

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
        self. _get_nova_client()
        azoneobj = AvailabilityZone()
        azoneobj.clean_all_aggregates()
        azoneobj.create_agg(vm_info['availability_zone'])
        installer = os.environ['INSTALLER_TYPE']
        self.Heat_template1 = self.heat_template_vm(vm_info, installer)
        self.create_stack(vm_role_ip_dict, self.Heat_template1)

    @staticmethod
    def get_public_network(installer_detected):

        """
        TODO: GET THE NAMES OF THE PUBLIC NETWORKS for OTHER PROJECTS
        """
        if installer_detected == '':
            raise RuntimeError("installer is None")

        print 'Getting Public Network'
        if installer_detected.lower() == 'fuel':
            return 'admin_floating_net'
        if installer_detected.lower() == 'apex':
            return 'external'
        if installer_detected.lower() == 'compass':
            return 'ext-net'
        if installer_detected.lower() == 'joid':
            return 'ext-net'

    def heat_template_vm(self, vm_params, installer):
        Heat_Dic = {}
        try:
            with open('./heat/SampleHeat.yaml', 'r+') as H_temp:
                Heat_Dic = yaml.load(H_temp)
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                print 'Error in qtip/heat/SampleHeat.yaml at: (%s,%s)' % (   mark.line + 1, mark.column + 1)
                print 'EXITING PROGRAM. Correct File and restart'
                sys.exit(0)

        Heat_Dic['heat_template_version'] = '2015-04-30'
        netName = self.get_public_network(installer)
        Heat_Dic['parameters']['external_net_name']['default'] = netName
        
        for x in range(1, len(vm_params['availability_zone']) + 1):
            avail_zone = vm_params['availability_zone'][x - 1]
            Heat_Dic['parameters']['availability_zone_' + str(x)] = \
                {'description': 'Availability Zone of the instance',
                 'default': avail_zone,
                 'type': 'string'}

            Heat_Dic['resources']['floating_ip_' + str(x)] = \
                {'type': 'OS::Neutron::FloatingIP',
                 'properties': {'floating_network': {'get_param': 'external_net_name'}}}

            Heat_Dic['resources']['floating_ip_assoc_' + str(x)] = \
                {'type': 'OS::Nova::FloatingIPAssociation',
                 'properties': {
                    'floating_ip': {'get_resource': 'floating_ip_' + str(x)},
                    'server_id': {'get_resource': 'instance_' + str(x)}}}

            Heat_Dic['resources']['instance_' + str(x)] = \
                {'type': 'OS::Nova::Server',
                 'depends_on': ['subnet', 'keypair', 'flavor', 'security_group'],
                 'properties': {'image': {'get_param': 'image'},
                                'networks':
                                    [{'network': {'get_resource': 'network'}}],
                                'flavor': {'get_resource': 'flavor'},
                                'name': 'qtip_instance' + str(x),
                                'key_name': {'get_resource': 'keypair'},
                                'availability_zone': avail_zone,
                                'security_groups': [{'get_resource': 'security_group'}]}}

            Heat_Dic['outputs']['instance_PIP_' + str(x)] = {
                'description': 'Private IP address of the instance',
                'value': {'get_attr': ['instance_' + str(x), 'first_address']}}
            Heat_Dic['outputs']['instance_FIP_' + str(x)] = {
                'description': 'Floating IP address of the instance',
                'value': {'get_attr': ['floating_ip_' + str(x), 'floating_ip_address']}}

            Heat_Dic['outputs']['availability_instance_' + str(x)] = {
                'description': 'Availability Zone of the Instance',
                'value': {'get_param': 'availability_zone_' + str(x)}}
        
        del Heat_Dic['outputs']['description']            
       # print Heat_Dic
        return Heat_Dic

    def _get_keystone_client(self):
        """returns a keystone client instance"""

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
        """returns a heat client instance"""
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

    def prepare_qtip_image(self):
        glance = self._get_glance_client()

        available_images = []
        for image_list in glance.images.list():
            available_images.append(image_list.name)

        if 'QTIP_CentOS' in available_images:
            print 'Image Present'
        else:
            fetchImage = FetchImg()
            fetchImage.download()
            print 'Uploading Image to Glance. Please wait'
            qtip_image = glance.images.create(
                name='QTIP_CentOS',
                visibility='public',
                disk_format='qcow2',
                container_format='bare')
            res = glance.images.upload(qtip_image.id, 
                                      open('./Temp_Img/QTIP_CentOS.qcow2'))
            print res

    def delete_stack(self, stack_name):
        heat = self._get_heat_client()
        
        stacks = heat.stacks.list()
        exists = map(lambda x: x.stack_name, stacks)
        if stack_name in exists:
            heat.stacks.delete(stack_name)
            while stack_name in exists:
                time.sleep(10)
                stacks = heat.stacks.list()
                exists = map(lambda x: x.stack_name, stacks)
                print "exists_stacks: %s" % exists
        print "%s doesn't exist" % stack_name

    def create_stack(self, vm_role_ip_dict, heat_template):
        global sshkey
        stackname = 'QTIP'
        heat = self._get_heat_client()

        self.prepare_qtip_image()

        self.delete_stack('QTIP')

        print '\nStart to Create QTIP stack\n'
        json_template = json.dumps(heat_template)
        print "++++++++++++++++++++++++++++++++++++++"
        print json_template
        print "++++++++++++++++++++++++++++++++++++++"
        heat.stacks.create(stack_name=stackname, template=json_template)

        cluster_detail = heat.stacks.get(stackname)
        while cluster_detail.status != 'COMPLETE':
            if cluster_detail.status == 'IN_PROGRESS':
                print 'Stack Creation: in Progress'
            if cluster_detail.status == 'CREATE_FAILED':
                print 'Stack Creation: Create Failed!'
                raise RuntimeError("Stack QTIP created failed!") 
            cluster_detail = heat.stacks.get(stackname)
            time.sleep(10)
        print 'Stack QTIP Created Complete!'
        print "**************************"
        print cluster_detail
        print "**************************"
        print 'Getting Public IP(s)'
        zone = []
        s = 0
        for vm in range(len(vm_role_ip_dict['OS_image'])):

            for I in cluster_detail.outputs:
                availabilityKey = 'availability_instance_' + str(vm + 1)

                if I['output_key'] == availabilityKey:
                    zone.insert(s, str(I['output_value']))
                    s = s + 1
            for i in cluster_detail.outputs:
                instanceKey = "instance_FIP_" + str(vm + 1)
                privateIPkey = 'instance_PIP_' + str(vm + 1)
                if i['output_key'] == instanceKey:
                    Env_setup.roles_dict[vm_role_ip_dict['role'][vm]] \
                        .append(str(i['output_value']))
                    Env_setup.ip_pw_list.append((str(i['output_value']), ''))

                if i['output_key'] == privateIPkey:
                    Env_setup.ip_pw_dict[vm_role_ip_dict['role'][vm]] = str(i['output_value'])
                if i['output_key'] == 'KeyPair_PublicKey':
                    sshkey = str(i['output_value'])

        print Env_setup.ip_pw_list
