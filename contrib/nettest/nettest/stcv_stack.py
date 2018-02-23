##############################################################################
# Copyright (c) 2018 Spirent Communications and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import os
from time import sleep
import traceback

import heatclient.client as heatclient
from keystoneauth1 import loading
from keystoneauth1 import session


class StcvStack(object):
    STCV_CONFIG_FILE = 'stcv_config_file'
    STCV_HEAT_FILE = './heat_2stcv.yaml'
    STCV_USER_DATA = '''#cloud-config
    spirent:
        ntp: '''

    def __init__(self, name, **kwargs):
        self.logger = logging.getLogger(__name__)

        self.name = name
        self.pub_net_name = kwargs.get('pub_net_name')
        self.ntp_server_ip = kwargs.get('ntp_server_ip')
        self.lab_server_ip = kwargs.get('lab_server_ip')
        self.stcv_image = kwargs.get('stcv_image')
        self.stcv_flavor = kwargs.get('stcv_flavor')
        if kwargs.get('stcv_affinity'):
            self.stcv_affinity = 'affinity'
        else:
            self.stcv_affinity = 'anti-affinity'

        self.stack_id = None
        self._heatc_lient = None

    def _attach_to_openstack(self):
        creds = {"username": os.environ.get('OS_USERNAME'),
                 "password": os.environ.get('OS_PASSWORD'),
                 "auth_url": os.environ.get('OS_AUTH_URL'),
                 "project_domain_id": os.environ.get('OS_PROJECT_DOMAIN_ID'),
                 "project_domain_name": os.environ.get('OS_PROJECT_DOMAIN_NAME'),
                 "project_id": os.environ.get('OS_PROJECT_ID'),
                 "project_name": os.environ.get('OS_PROJECT_NAME'),
                 "tenant_name": os.environ.get('OS_TENANT_NAME'),
                 "tenant_id": os.environ.get("OS_TENANT_ID"),
                 "user_domain_id": os.environ.get('OS_USER_DOMAIN_ID'),
                 "user_domain_name": os.environ.get('OS_USER_DOMAIN_NAME')
                 }

        self.logger.debug("Creds: %s" % creds)

        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(**creds)
        sess = session.Session(auth)
        self._heat_client = heatclient.Client("1", session=sess)

    def _make_parameters(self):
        user_data = self.STCV_USER_DATA + self.ntp_server_ip
        file_path = os.getcwd() + '/' + self.STCV_CONFIG_FILE
        fd = open(file_path, 'w')
        fd.writelines(user_data)
        fd.close()

        return {
            'public_net_name': self.pub_net_name,
            'stcv_image': self.stcv_image,
            'stcv_flavor': self.stcv_flavor,
            'stcv_sg_affinity': self.stcv_affinity,
            'ntp_server_ip': self.ntp_server_ip
        }

    def acquire_ip_from_stack_output(self, output, key_name):
        ip = None
        for item in output:
            if item['output_key'] == key_name:
                ip = item['output_value']
                if isinstance(ip, list):
                    ip = ip[0]['ip_address']
                break

        return ip

    def create_stack(self):
        with open(self.STCV_HEAT_FILE) as fd:
            template = fd.read()

        self._attach_to_openstack()

        self.logger.debug("Creating stack")

        stack = self._heat_client.stacks.create(
            stack_name=self.name,
            template=template,
            parameters=self._make_parameters())

        self.stack_id = stack['stack']['id']

        while True:
            stack = self._heat_client.stacks.get(self.stack_id)
            status = getattr(stack, 'stack_status')
            self.logger.debug("Stack status=%s" % (status,))
            if (status == u'CREATE_COMPLETE'):
                self.stcv1_ip = self.acquire_ip_from_stack_output(stack.outputs, "STCv_1_Mgmt_Ip")
                self.stcv2_ip = self.acquire_ip_from_stack_output(stack.outputs, "STCv_2_Mgmt_Ip")
                self.stcv1_tst_ip = self.acquire_ip_from_stack_output(stack.outputs, "STCv_1_Tst_Ip")
                self.stcv2_tst_ip = self.acquire_ip_from_stack_output(stack.outputs, "STCv_2_Tst_Ip")
                break
            if (status == u'DELETE_COMPLETE'):
                self.stack_id = None
                break
            if (status == u'CREATE_FAILED'):
                self.status_reason = getattr(stack, 'stack_status_reason')
                sleep(5)
                self._heat_client.stacks.delete(stack_id=self.stack_id)
            sleep(2)

    def delete_stack(self):
        if self.stack_id is None:
            raise Exception('stack does not exist')

        self._attach_to_openstack()
        while True:
            stack = self._heat_client.stacks.get(self.stack_id)
            status = getattr(stack, 'stack_status')
            self.logger.debug("Stack status=%s" % (status,))
            if (status == u'CREATE_COMPLETE'):
                self._heat_client.stacks.delete(stack_id=self.stack_id)
            if (status == u'DELETE_COMPLETE'):
                self.stack_id = None
                break
            if (status == u'DELETE_FAILED'):
                sleep(5)
                self._heat_client.stacks.delete(stack_id=self.stack_id)
            sleep(2)

    def get_west_stcv_ip(self):
        return self.stcv1_ip

    def get_west_stcv_tst_ip(self):
        return self.stcv1_tst_ip

    def get_east_stcv_ip(self):
        return self.stcv2_ip

    def get_east_stcv_tst_ip(self):
        return self.stcv2_tst_ip


if __name__ == '__main__':
    try:
        stack = StcvStack(name='stack1',
                          pub_net_name='external',
                          ntp_server_ip='192.168.37.151',
                          stcv_image='stcv-4.79',
                          stcv_flavor='m1.tiny',
                          affinity=False)
        stack.create_stack()

        print stack.get_east_stcv_ip()
        print stack.get_east_stcv_tst_ip()
        print stack.get_west_stcv_ip()
        print stack.get_west_stcv_tst_ip()

    except Exception as err:
        excstr = traceback.format_exc()
        print excstr
