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
      description: host grouped by hostname, cluster, role and manufacture
      type: dict
    hosts_meta:
      description: hosts meta data indexed by hostname
      type: dict
'''

EXAMPLES = '''
---
- hosts: apex-undercloud
  tasks:
  - name: collect facts of fuel hosts
    fuel:
  - debug: var=hostvarsi
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


def generate_inventory(baremetal_info, server_info):
    """Generate ansible inventory from node list in json format

    Modified from https://github.com/martineg/ansible-fuel-inventory/blob/master/fuel.py
    """

    hosts = defaultdict(list)
    hosts_meta = {}

    for node in baremetal_info:
        if node['Provisioning State'].lower() == 'active':
            role = re.findall('.+profile:(\w+)$', node['Properties']['capabilities'])[0]
            for server in server_info:
                if server['ID'] == node['Instance UUID']:
                    node_ip = re.findall('.+=(\d+.\d+.\d+.\d+)$', server['Networks'])[0]
                    hosts[role].append(node_ip)
                    # To match ssh.cfg.j2 template
                    hosts_meta[node_ip] = {'ansible_ssh_host': node_ip}

    for host in hosts:
        hosts[host].sort()

    return {'hosts': hosts, 'hosts_meta': hosts_meta}


def main():
    module = AnsibleModule(argument_spec=dict())

    (rc, out, err) = module.run_command(['source ~/stackrc'])

    if rc is not None and rc != 0:
        return module.fail_json(msg=err)

    cmd = [module.get_bin_path('openstack', True),
           'baremetal',
           'list',
           '--fields instance_uuid properties provision_state',
           '--format json']
    (rc, out, err) = module.run_command(cmd)

    if rc is not None and rc != 0:
        return module.fail_json(msg=err)

    baremetal_info = json.loads(out)

    cmd = [module.get_bin_path('openstack', True),
           'server',
           'list',
           '--format json']
    (rc, out, err) = module.run_command(cmd)

    if rc is not None and rc != 0:
        return module.fail_json(msg=err)

    server_info = json.loads(out)

    module.exit_json(changed=False,
                     ansible_facts=generate_inventory(baremetal_info, server_info))


if __name__ == '__main__':
    main()
