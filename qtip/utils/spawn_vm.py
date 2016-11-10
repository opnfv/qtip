##############################################################################
# Copyright (c) 2016 Dell Inc, ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import sys
import yaml
import heatclient.client
import keystoneclient
import time
from env_setup import Env_setup
from create_zones import AvailabilityZone
import logger_utils

logger = logger_utils.QtipLogger('spawn_vm').get


class SpawnVM(Env_setup):

    def __init__(self, vm_info):
        logger.info('vm_info: %s' % vm_info)
        vm_role_ip_dict = vm_info.copy()
        self._keystone_client = None
        self._heat_client = None
        self._glance_client = None
        self._nova_client = None
        self.azone = AvailabilityZone()
        # TODO: it should clean up aggregates and stack after test case finished.
        self.azone.clean_all_aggregates()
        self.azone.create_aggs(vm_info['availability_zone'])
        self.heat_template = self.generate_heat_template(vm_info)
        self.create_stack(vm_role_ip_dict)

    @staticmethod
    def get_public_network():

        """
        TODO: GET THE NAMES OF THE PUBLIC NETWORKS for OTHER PROJECTS
        """
        installer = os.environ['INSTALLER_TYPE']

        if installer.lower() == 'fuel':
            return 'admin_floating_net'
        if installer.lower() == 'apex':
            return 'external'
        if installer.lower() == 'compass':
            return 'ext-net'
        if installer.lower() == 'joid':
            return 'ext-net'

    def generate_heat_template(self, vm_params):
        logger.info('Generating Heat Template')
        heat_dict = {}
        try:
            with open('./config/SampleHeat.yaml', 'r+') as H_temp:
                heat_dict = yaml.safe_load(H_temp)
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                logger.error(
                    'Error in qtip/config/SampleHeat.yaml at: (%s,%s)' % (mark.line + 1,
                                                                          mark.column + 1))
                logger.error('EXITING PROGRAM. Correct File and restart')
                sys.exit(1)

        fopen = open('./config/QtipKey.pub', 'r')
        fopenstr = fopen.read()
        fopenstr = fopenstr.rstrip()
        scriptcmd = '#!/bin/bash \n echo {0} >>  foo.txt \n echo {1} >> /root/.ssh/authorized_keys'.format(
            fopenstr, fopenstr)

        netName = self.get_public_network()
        heat_dict['heat_template_version'] = '2015-04-30'

        heat_dict['parameters']['public_network'] = {
            'type': 'string',
            'default': netName
        }

        for x in range(1, len(vm_params['availability_zone']) + 1):
            avail_zone = vm_params['availability_zone'][x - 1]

            heat_dict['parameters']['availability_zone_' + str(x)] = \
                {'description': 'Availability Zone of the instance',
                 'default': avail_zone,
                 'type': 'string'}

            heat_dict['resources']['public_port_' + str(x)] = \
                {'type': 'OS::Neutron::Port',
                 'properties': {'network': {'get_resource': 'network'},
                                'security_groups': [{'get_resource': 'security_group'}],
                                'fixed_ips': [{'subnet_id': {'get_resource': 'subnet'}}]}}

            heat_dict['resources']['floating_ip_' + str(x)] = {
                'type': 'OS::Neutron::FloatingIP',
                'properties': {'floating_network': {'get_param': 'external_net_name'}}}

            heat_dict['resources']['floating_ip_assoc_' + str(x)] = {
                'type': 'OS::Neutron::FloatingIPAssociation',
                'properties': {
                    'floatingip_id': {'get_resource': 'floating_ip_' + str(x)},
                    'port_id': {'get_resource': 'public_port_' + str(x)}}}

            heat_dict['resources']['my_instance_' + str(x)] = \
                {'type': 'OS::Nova::Server',
                 'properties': {'image': {'get_param': 'image'},
                                'networks':
                                    [{'port': {'get_resource': 'public_port_' + str(x)}}],
                                'flavor': {'get_resource': 'flavor'},
                                'availability_zone': avail_zone,
                                'security_groups': [{'get_resource': 'security_group'}],
                                'name': 'instance' + str(x),
                                'user_data_format': 'RAW',
                                'user_data': scriptcmd}}

            heat_dict['outputs']['instance_PIP_' + str(x)] = {
                'description': 'IP address of the instance',
                'value': {'get_attr': ['my_instance_' + str(x), 'first_address']}}

            heat_dict['outputs']['instance_ip_' + str(x)] = {
                'description': 'IP address of the instance',
                'value': {'get_attr': ['floating_ip_' + str(x), 'floating_ip_address']}}

            heat_dict['outputs']['availability_instance_' + str(x)] = {
                'description': 'Availability Zone of the Instance',
                'value': {'get_param': 'availability_zone_' + str(x)}}

        del heat_dict['outputs']['description']
        logger.info(heat_dict)

        return heat_dict

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

    def create_stack(self, vm_role_ip_dict):
        stackname = 'QTIP'
        heat = self._get_heat_client()

        self.delete_stack(stackname)

        logger.info('Start to create stack %s' % stackname)
        heat.stacks.create(stack_name=stackname, template=self.heat_template)

        stack_status = "IN_PROGRESS"
        while stack_status != 'COMPLETE':
            if stack_status == 'IN_PROGRESS':
                logger.debug('Create in Progress')
            if stack_status == 'CREATE_FAILED':
                raise RuntimeError("Stack %s created failed!" % stackname)
            stack_status = heat.stacks.get(stackname).status
            time.sleep(15)
        logger.info('Stack %s Created Complete!' % stackname)

        stack_outputs = heat.stacks.get(stackname).outputs

        for vm in range(len(vm_role_ip_dict['OS_image'])):
            for i in stack_outputs:
                instanceKey = "instance_ip_" + str(vm + 1)
                privateIPkey = 'instance_PIP_' + str(vm + 1)
                if i['output_key'] == instanceKey:
                    Env_setup.roles_dict[vm_role_ip_dict['role'][vm]] \
                        .append(str(i['output_value']))
                    Env_setup.ip_pw_list.append((str(i['output_value']), ''))

                if i['output_key'] == privateIPkey:
                    Env_setup.ip_pw_dict[vm_role_ip_dict['role'][vm]] = str(i['output_value'])

        logger.info('Getting Public IP(s): %s' % Env_setup.ip_pw_list)

    def delete_stack(self, stack_name):
        heat = self._get_heat_client()

        stacks = heat.stacks.list()
        exists = map(lambda x: x.stack_name, stacks)
        if stack_name in exists:
            logger.info("Delete stack %s" % stack_name)
            heat.stacks.delete(stack_name)
            while stack_name in exists:
                time.sleep(10)
                stacks = heat.stacks.list()
                exists = map(lambda x: x.stack_name, stacks)
                logger.debug("exists_stacks: %s" % exists)
        logger.info("%s doesn't exist" % stack_name)
