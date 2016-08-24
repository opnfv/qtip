##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from func.ansible_api import AnsibleApi


class TestClass:
    def test_call_ansible_api_success(self):
        ansible_api = AnsibleApi()
        ret = ansible_api.execute_playbook('tests/data/hosts',
                                           'tests/data/test.yml',
                                           'data/QtipKey',
                                           {'keys': 'test'})
        assert ret == 3
