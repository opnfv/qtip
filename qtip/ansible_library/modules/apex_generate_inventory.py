#!/usr/bin/python

###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from collections import defaultdict
import re

from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: apex
short_description: collecting facts from apex environments
description:
    - Use this module to create a dynamic inventory from apex undercloud.
version_added: "2.2"
author: "Zhihui Wu"
options:
  baremetal_info:
    description:
      - return value from "openstack baremetal node list
        --fields instance_uuid properties provision_state --format json"
  server_info:
    description:
      - return value from "openstack server list --format json"
notes:
requirements:
    - Host 'apex-undercloud' is in ~/.ssh/config
'''

RETURN = '''
ansible_facts:
  description: facts collected for ansible
  returned: success
  type: dictionary
  contains:
    hosts:
      description: host grouped by role
      type: dict
    hosts_meta:
      description: hosts meta data indexed by hostname
      type: dict
'''

EXAMPLES = '''
---
- hosts: apex-undercloud
  tasks:
  - name: collect facts of apex hosts
    apex_generate_inventory:
      baremetal_info: "{{ baremetal_info.stdout | from_json }}"
      server_info: "{{ server_info.stdout | from_json }}"
'''


def generate_inventory(baremetal_info, server_info):
    """Generate ansible inventory in json format"""

    hosts = defaultdict(list)
    hosts_meta = {}

    for node in baremetal_info:
        if node['Provisioning State'].lower() == 'active':
            role = re.findall('.*profile:(compute|control)', node['Properties']['capabilities'])[0]
            for server in server_info:
                if server['ID'] == node['Instance UUID']:
                    node_ip = re.findall('.+=(\d+.\d+.\d+.\d+)$', server['Networks'])[0]
                    hosts[role].append(node_ip)
                    # To match ssh.cfg.j2 template
                    hosts_meta[node_ip] = {'ansible_ssh_host': node_ip,
                                           'ansible_user': 'heat-admin'}

    for host in hosts:
        hosts[host].sort()

    return {'hosts': hosts, 'hosts_meta': hosts_meta}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            baremetal_info=dict(type='list'),
            server_info=dict(type='list')
        )
    )

    baremetal_info = module.params['baremetal_info']
    server_info = module.params['server_info']

    module.exit_json(changed=True,
                     ansible_facts=generate_inventory(baremetal_info, server_info))


if __name__ == '__main__':
    main()
