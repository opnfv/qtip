#!/usr/bin/python

###############################################################
# Copyright (c) 2018 ZTE Corporation and Others
# taseer94@gmail.com
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import contrib.nettest_client.nettest_client as qtip_nettest
from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nettest
short_description: execute Spirent testcases
description:
    - Use this module to execute network performance benchmarking
version_added: "1.0"
author: "Taseer Ahmed"
'''

RETURN = '''
ansible_facts:
  description: network benchmark tests
  returned: success
  type: dictionary
  contains:
    result:
'''

EXAMPLES = '''
---
- hosts: apex-undercloud
  tasks:
  - name: execute network performance test
    nettest:
'''

def main():
    module = AnsibleModule(argument_spec=dict())

    module.exit_json(changed=True, ansible_facts=qtip_nettest.run())


if __name__ == '__main__':
    main()
