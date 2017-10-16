#!/usr/bin/python

###############################################################
# Copyright (c) 2017 ZTE Corporation and others
# taseer94@gmail.com
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
from collections import defaultdict

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: mcp
short_description: collecting facts from mcp environments
description:
    - Use this module to create a dynamic inventory from salt master (mcp).
version_added: "1.0"
author: "Taseer Ahmed (@Taseer)"
options:
notes:
requirements:
    - Host 'salt-master' is in ~/.ssh/config
'''

RETURN = '''
ansible_facts:
  description: facts collected for ansible
  returned: success
  type: dictionary
  contains:
    hosts:
      description: host grouped by hostname, cluster, role and manufacture
      type: dict
    hosts_meta:
      description: hosts meta data indexed by hostname
      type: dict
'''

EXAMPLES = '''
---
- hosts: salt-master
  tasks:
  - name: collect facts of mcp hosts
    mcp:
  - debug: var=hostvars
  - name: add compute node to ansible inventory
    add_host:
      name: "{{ hosts_meta[item]['ip'] }}"
      groups: mcp-compute
      ansible_user: root
      ansible_ssh_common_args: '-o StrictHostKeyChecking=No -o ProxyJump=salt-master'
    with_items: "{{ hosts.compute }}"
- hosts: mcp-compute
  tasks:
  - name: check ssh connection
    ping:
'''


def generate_inventory(nodes):
    """Generate ansible inventory from node list in json format"""
    hosts = defaultdict(list)
    hosts_meta = {}
    node_meta = {}

    for key, value in nodes.iteritems():
        if isinstance(value, dict):
            for k, v in value.iteritems():
                if k == "fqdn_ip4":
                    node_meta['ansible_ssh_host'] = v[0]
        node_meta['ansible_user'] = 'root'
        hosts_meta[key] = node_meta
        hosts['compute-nodes'].append(node_meta['ansible_ssh_host'])

    return {'hosts': hosts, 'hosts_meta': hosts_meta}


def main():
    module = AnsibleModule(argument_spec=dict())

    cmd = [module.get_bin_path('salt', True), '-C', '-t 5', '--static', '--out=json', 'cmp*', 'grains.item',
           'fqdn_ip4', 'host']
    (rc, out, err) = module.run_command(cmd)

    if rc is not None and rc != 0:
        return module.fail_json(msg=err)

    nodes = json.loads(out)

    module.exit_json(changed=False, ansible_facts=generate_inventory(nodes))


if __name__ == '__main__':
    main()
