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

from qtip.ansible_library.modules import fuel


def test_generate_inventory(data_root):
    nodes = json.load(open(os.path.join(data_root, 'external', 'fuel', 'fuel-node.json')))
    inventory = fuel.generate_inventory(nodes)
    assert dict(inventory['hosts']) == {
        u'ceph-osd': [u'node-26', u'node-28', u'node-27'],
        'cluster-4': [u'node-24',
                      u'node-26',
                      u'node-23',
                      u'node-28',
                      u'node-25',
                      u'node-27'],
        u'compute': [u'node-26', u'node-28', u'node-27'],
        u'controller': [u'node-24', u'node-23', u'node-25'],
        'hw-zte-servers': [u'node-24',
                           u'node-26',
                           u'node-23',
                           u'node-28',
                           u'node-25',
                           u'node-27'],
        u'mongo': [u'node-24']}
    assert dict(inventory['hosts_meta']) == {
        u'node-23': {'ansible_ssh_host': u'10.20.11.10', 'ansible_user': 'root', 'cluster': 4, 'ip': u'10.20.11.10',
                     'mac': u'74:4a:a4:01:71:61', 'name': u'Untitled (71:61)', 'online': True, 'os_platform': u'ubuntu',
                     'status': u'ready'},
        u'node-24': {'ansible_ssh_host': u'10.20.11.11', 'ansible_user': 'root', 'cluster': 4, 'ip': u'10.20.11.11',
                     'mac': u'74:4a:a4:01:73:50', 'name': u'Untitled (73:50)', 'online': True, 'os_platform': u'ubuntu',
                     'status': u'ready'},
        u'node-25': {'ansible_ssh_host': u'10.20.11.12', 'ansible_user': 'root', 'cluster': 4, 'ip': u'10.20.11.12',
                     'mac': u'74:4a:a4:00:d8:76', 'name': u'Untitled (d8:76)', 'online': True, 'os_platform': u'ubuntu',
                     'status': u'ready'},
        u'node-26': {'ansible_ssh_host': u'10.20.11.15', 'ansible_user': 'root', 'cluster': 4, 'ip': u'10.20.11.15',
                     'mac': u'74:4a:a4:01:61:ae', 'name': u'Untitled (61:ae)', 'online': True, 'os_platform': u'ubuntu',
                     'status': u'ready'},
        u'node-27': {'ansible_ssh_host': u'10.20.11.13', 'ansible_user': 'root', 'cluster': 4, 'ip': u'10.20.11.13',
                     'mac': u'74:4a:a4:01:82:c0', 'name': u'Untitled (82:c0)', 'online': True, 'os_platform': u'ubuntu',
                     'status': u'ready'},
        u'node-28': {'ansible_ssh_host': u'10.20.11.14', 'ansible_user': 'root', 'cluster': 4, 'ip': u'10.20.11.14',
                     'mac': u'74:4a:a4:01:74:63', 'name': u'Untitled (74:63)', 'online': True, 'os_platform': u'ubuntu',
                     'status': u'ready'}}
