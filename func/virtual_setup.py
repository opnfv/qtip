#############################################################################
# Copyright (c) 2016 Dell Inc, ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import sys
import json
import yaml
import time
import heatclient.client
import glanceclient
import keystoneclient
from func.create_zones import AvailabilityZone
from func.env_setup import Env_setup
from func.fetchimg import FetchImg


class Virtual(Env_setup):
    def __init__(self, args, installer_type):
        super(Virtual, self).__init__(args)
        self.args = args.copy()
        self.installer_type = installer_type
        self.vm_info = []
        self._keystone_client = None
        self._heat_client = None
        self._glance_client = None
        self._nova_client = None
        self.azone = None
        self.get_virtual_machine_info(self.args['Context']['Virtual_Machines'])

    def get_virtual_machine_info(self, args):
        for item in args.keys():
            self.vm_info.append({item: args[item]})

    def setup(self):
        print "Virtual test setup"
        self.azone = AvailabilityZone()
        self.azone.clean_all_aggregates()
        azones = []
        for index, vm in enumerate(self.vm_info):
            host_label = 'virtualmachine_' + str(index + 1)
            azones.append(vm[host_label]['availability_zone'])
        print azones
        self.azone.create_agg(azones)

        self.template = self.heat_template_vm(self.vm_info, self.installer_type)
        stack_outputs = self.create_stack(self.template)

        for index, vm in enumerate(self.vm_info):
            t = str(index + 1)
            host_label = 'virtualmachine_' + t
            floating_ip_name = 'instance_FIP_' + t
            uuid_name = 'instance_uuid_' + t

            for item in stack_outputs:
                if item['output_key'] == floating_ip_name:
                    role = vm[host_label]['role']
                    ip = item['output_value']
                    vm[host_label]['floating_ip'] = ip
                    self.roles_dict[role].append(ip)
                    self.roles_ip_list.append((role, ip))
                    self.ip_pw_list.append((ip, None))
                    self.ip_pw_dict[ip] = [None]
                if item['output_key'] == uuid_name:
                    vm[host_label]['uuid'] = item['output_value']

    def cleanup(self):
        print "Virtual test cleanup"
        self.delete_stack('QTIP')
        self.azone.clean_all_aggregates()

    @staticmethod
    def get_public_network(installer_detected):
        """
        TODO: GET THE NAMES OF THE PUBLIC NETWORKS for OTHER PROJECTS
        """
        if installer_detected == '':
            raise RuntimeError("installer is None")

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
                print 'Error in qtip/heat/SampleHeat.yaml at: (%s,%s)' % (mark.line + 1, mark.column + 1)
                print 'EXITING PROGRAM. Correct File and restart'
                sys.exit(0)

        Heat_Dic['heat_template_version'] = '2015-04-30'

        netName = self.get_public_network(installer)
        Heat_Dic['parameters']['external_net_name']['default'] = netName

        for index, vm in enumerate(self.vm_info):
            x = str(index + 1)
            host_label = 'virtualmachine_' + x
            Heat_Dic['parameters']['availability_zone_' + x] = \
                {'description': 'Availability Zone of the instance',
                 'default': vm[host_label]['availability_zone'],
                 'type': 'string'}

            Heat_Dic['resources']['public_port_' + x] = \
                {'type': 'OS::Neutron::Port',
                 'properties': {'network': {'get_resource': 'network'},
                                'security_groups': [{'get_resource': 'security_group'}],
                                'fixed_ips': [{'subnet_id': {'get_resource': 'subnet'}}]}}

            Heat_Dic['resources']['floating_ip_' + x] = \
                {'type': 'OS::Neutron::FloatingIP',
                 'properties': {'floating_network': {'get_param': 'external_net_name'}}}

            Heat_Dic['resources']['floating_ip_assoc_' + x] = {
                'type': 'OS::Neutron::FloatingIPAssociation',
                'properties': {
                    'floatingip_id': {'get_resource': 'floating_ip_' + x},
                    'port_id': {'get_resource': 'public_port_' + x}}}

            Heat_Dic['resources']['qtip_instance_' + x] = \
                {'type': 'OS::Nova::Server',
                 'depends_on': ['subnet', 'keypair', 'flavor', 'security_group'],
                 'properties': {'image': {'get_param': 'image'},
                                'networks':
                                    [{'port': {'get_resource': 'public_port_' + x}}],
                                'flavor': {'get_resource': 'flavor'},
                                'name': 'qtip_instance_' + x,
                                'key_name': {'get_resource': 'keypair'},
                                'availability_zone': vm[host_label]['availability_zone'],
                                'security_groups': [{'get_resource': 'security_group'}]}}

            Heat_Dic['outputs']['instance_PIP_' + x] = {
                'description': 'Private IP address of the instance',
                'value': {'get_attr': ['qtip_instance_' + x, 'first_address']}}
            Heat_Dic['outputs']['instance_FIP_' + x] = {
                'description': 'Floating IP address of the instance',
                'value': {'get_attr': ['floating_ip_' + x, 'floating_ip_address']}}

            Heat_Dic['outputs']['availability_instance_' + x] = {
                'description': 'Availability Zone of the Instance',
                'value': {'get_param': 'availability_zone_' + x}}

            Heat_Dic['outputs']['instance_uuid_' + x] = {
                'description': 'uuid of the instance_' + x,
                'value': {'get_attr': ['qtip_instance_' + x, 'show', 'id']}}

        del Heat_Dic['outputs']['description']
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
            glance.images.upload(qtip_image.id,
                                 open('./Temp_Img/QTIP_CentOS.qcow2'))

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

    def create_stack(self, heat_template):
        stackname = 'QTIP'
        stack_outputs = {}

        self.prepare_qtip_image()

        heat = self._get_heat_client()

        self.delete_stack('QTIP')

        print '\nStart to Create QTIP stack\n'
        json_template = json.dumps(heat_template)
        heat.stacks.create(stack_name=stackname, template=json_template)
        stack_status = "IN_PROGRESS"
        while stack_status != 'COMPLETE':
            if stack_status == 'IN_PROGRESS':
                print 'Stack Creation: in Progress'
            if stack_status == 'CREATE_FAILED':
                print 'Stack Creation: Create Failed!'
                raise RuntimeError("Stack QTIP created failed!")
            stack_status = heat.stacks.get(stackname).status
            time.sleep(15)
        print 'Stack QTIP Created Complete!'
        stack_outputs = heat.stacks.get(stackname).outputs
        return stack_outputs

    def update_ansible(self):
        f_name_2 = open('./data/hosts', 'w')
        for k in self.roles_dict:
            f_name_2.write('[' + k + ']\n')
            for item in self.roles_dict[k]:
                f_name_2.write(item + '  ansible_user=centos\n')
        f_name_2.close()

    def call_ssh_test(self):
        self.ssh_test(self.ip_pw_list, "centos")
