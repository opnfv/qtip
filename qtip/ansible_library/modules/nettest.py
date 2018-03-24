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

from collections import defaultdict
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
      name: s1,
      stack_type: stcv,
      public_network_name: public,
      stcv_affinity: True,
      stcv_image: STCv-4.80.2426,
      stcv_flavor: small.shared,
      lab_server_ip: 10.61.67.53,
      license_server_ip: 10.140.88.61
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            stack_type=dict(type='str'),
            public_network_name=dict(type='str'),
            stcv_affinity=dict(type='bool'),
            stcv_image=dict(type='str'),
            stcv_flavor=dict(type='str'),
            lab_server_ip=dict(type='str'),
            license_server_ip=dict(type='str')
        )
    )

    module.exit_json(changed=True, ansible_facts=qtip_nettest.run(name,
                                                                  stack_type,
                                                                  public_network_name,
                                                                  stcv_affinity,
                                                                  stcv_image,
                                                                  stcv_flavor,
                                                                  lab_server_ip,
                                                                  license_server_ip))


if __name__ == '__main__':
    main()
