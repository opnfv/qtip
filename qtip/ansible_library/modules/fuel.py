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
import json

from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: fuel
short_description: collecting facts from fuel environments
description:
    - Use this module to create a dynamic inventory from fuel master.
version_added: "2.2"
author: "Yujun Zhang (@yujunz)"
options:
notes:
requirements:
    - Host 'fuel-master' is in ~/.ssh/config
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
- hosts: fuel-master
  tasks:
  - name: collect facts of fuel hosts
    fuel:
  - debug: var=hostvars
  - name: add compute node to ansible inventory
    add_host:
      name: "{{ hosts_meta[item]['ip'] }}"
      groups: fuel-compute
      ansible_user: root
      ansible_ssh_common_args: '-o StrictHostKeyChecking=No -o ProxyJump=fuel-master'
    with_items: "{{ hosts.compute }}"
- hosts: fuel-compute
  tasks:
  - name: check ssh connection
    ping:
'''


def generate_inventory(nodes):
    """Generate ansible inventory from node list in json format

    Modified from https://github.com/martineg/ansible-fuel-inventory/blob/master/fuel.py
    """
    hosts = defaultdict(list)
    hosts_meta = {}

    for node in nodes:
        # skip deleting, offline, deploying and discovering/unprovisioned nodes
        if node['pending_deletion'] or (not node['online']) \
                or node['status'] == 'deploying' or node['status'] == 'discover':
            continue

        hostname = node['hostname']
        cluster_id = node['cluster']
        hw_vendor = node['meta']['system']['manufacturer'].lower()

        [hosts[role.strip()].append(hostname) for role in node['roles'].split(",")]
        hosts["cluster-{0}".format(cluster_id)].append(hostname)
        hosts["hw-{0}-servers".format(hw_vendor)].append(hostname)

        node_meta = {
            'name': node['name'],
            'online': node['online'],
            'os_platform': node['os_platform'],
            'status': node['status'],
            'ip': node['ip'],
            'mac': node['mac'],
            'cluster': cluster_id,
            'ansible_ssh_host': node['ip'],
            'ansible_user': 'root'
        }
        hosts_meta[hostname] = node_meta

    return {'hosts': hosts, 'hosts_meta': hosts_meta}


def main():
    module = AnsibleModule(argument_spec=dict())

    cmd = [module.get_bin_path('fuel', True), 'node', '--json']
    (rc, out, err) = module.run_command(cmd)

    if rc is not None and rc != 0:
        return module.fail_json(msg=err)

    nodes = json.loads(out)

    module.exit_json(changed=False, ansible_facts=generate_inventory(nodes))


if __name__ == '__main__':
    main()
