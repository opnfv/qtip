##############################################################################
# Copyright (c) 2018 Spirent Communications and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
from time import sleep

from rfc2544test import StcRfc2544Test
from stcv_stack import StcvStack


class NetTestMaster(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.stacks = []
        self.testcases = []

        self.stack_created = False
        self.status_reason = ''

    def get_stack_by_id(self, id):
        for stack in self.stacks:
            if id == stack.stack_id:
                return stack
        return None

    def get_stack_by_name(self, name):
        for stack in self.stacks:
            if name == stack.name:
                return stack
        return None

    def create_stack(self, name, stack_type, pub_net_name, **kwargs):
        if stack_type != 'stcv':
            raise Exception('only support stcv stack type currently')

        try:
            stack = StcvStack(name=name,
                              pub_net_name=pub_net_name,
                              ntp_server_ip=kwargs.get('license_server_ip'),
                              lab_server_ip=kwargs.get('lab_server_ip'),
                              stcv_image=kwargs.get('stcv_image'),
                              stcv_flavor=kwargs.get('stcv_flavor'),
                              stcv_affinity=kwargs.get('stcv_affinity'))
            stack.create_stack()
            self.stacks.append(stack)

        except Exception as err:
            self.logger.error('create stack fail. err = %s', str(err))
            raise err

        return stack

    def delete_stack(self, stack_id):
        stack = self.get_stack_by_id(stack_id)
        if stack is None:
            raise Exception('stack does not exist, stack_id = %s', stack_id)

        self.stacks.remove(stack)
        stack.delete_stack()

    def get_tc_result(self, tc_id):
        tc = self.get_tc_by_id(tc_id)
        return tc.get_result()

    def get_tc_status(self, tc_id):
        tc = self.get_tc_by_id(tc_id)
        return tc.get_status()

    def execute_testcase(self, name, category, stack_id, **kwargs):
        if category != 'rfc2544':
            raise Exception("currently only support rfc2544 test")

        stack = self.get_stack_by_id(stack_id)
        if stack is None:
            raise Exception("defined stack not exist, stack_id = %s", stack_id)

        tc = StcRfc2544Test(name=name,
                            lab_server_ip=stack.lab_server_ip,
                            license_server_ip=stack.ntp_server_ip,
                            west_stcv_admin_ip=stack.get_west_stcv_ip(),
                            west_stcv_tst_ip=stack.get_west_stcv_tst_ip(),
                            east_stcv_admin_ip=stack.get_east_stcv_ip(),
                            east_stcv_tst_ip=stack.get_east_stcv_tst_ip(),
                            stack_id=stack_id,
                            **kwargs)
        self.testcases.append(tc)
        tc.execute()

        return tc.tc_id

    def get_tc_by_id(self, id):
        for tc in self.testcases:
            if id == tc.tc_id:
                return tc
        return None

    def delete_testcase(self, tc_id):
        tc = self.get_tc_by_id(tc_id)

        if tc.status == 'finished':
            tc.delete_result()

        if tc.status == 'running':
            tc.cancel_run()

        self.testcases.remove(tc)


if __name__ == "__main__":
    try:
        nettest = NetTestMaster()
        stack_params = {
            "stcv_affinity": True,
            "stcv_image": "stcv-4.79",
            "stcv_flavor": "m1.tiny",
            "lab_server_ip": "192.168.37.122",
            "license_server_ip": "192.168.37.251"
        }

        stack = nettest.create_stack(name='stack1',
                                     stack_type='stcv',
                                     pub_net_name='external',
                                     **stack_params)
        tc_params = {
            'metric': 'throughput',
            'framesizes': [64, 128]
        }
        tc = nettest.execute_testcase(name='tc1',
                                      category='rfc2544',
                                      stack_id=stack.stack_id,
                                      **tc_params)

        print "test case id is %s" % tc.id

        status = tc.get_status()
        while (status != tc.TC_STATUS_FINISHED):
            if status == tc.TC_STATUS_ERROR:
                print "tc exectue fail, reason %s" % tc.get_err_reason()
                break
            sleep(2)
        if status == tc.TC_STATUS_FINISHED:
            print tc.get_result()

        nettest.delete_testcase(tc.id)

        nettest.delete_stack(stack.stack_id)

    except Exception as err:
        print err
