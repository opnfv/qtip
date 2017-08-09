###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import os

from qtip.ansible_library.modules import apex_generate_inventory


def test_generate_inventory(data_root):
    baremetal_info = json.load(open(os.path.join(data_root, 'external',
                                                 'apex', 'baremetal_info.json')))
    server_info = json.load(open(os.path.join(data_root, 'external',
                                              'apex', 'server_info.json')))
    inventory = apex_generate_inventory.generate_inventory(baremetal_info, server_info)
    assert dict(inventory['hosts']) == {
        u'compute': [u'192.0.2.5', u'192.0.2.6'],
        u'control': [u'192.0.2.7', u'192.0.2.8', u'192.0.2.9']}
    assert dict(inventory['hosts_meta']) == {
        u'192.0.2.5': {'ansible_ssh_host': u'192.0.2.5', 'ansible_user': 'heat-admin'},
        u'192.0.2.6': {'ansible_ssh_host': u'192.0.2.6', 'ansible_user': 'heat-admin'},
        u'192.0.2.7': {'ansible_ssh_host': u'192.0.2.7', 'ansible_user': 'heat-admin'},
        u'192.0.2.8': {'ansible_ssh_host': u'192.0.2.8', 'ansible_user': 'heat-admin'},
        u'192.0.2.9': {'ansible_ssh_host': u'192.0.2.9', 'ansible_user': 'heat-admin'}}
