##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from snaps.openstack.create_stack import StackSettings, OpenStackHeatStack
from snaps.openstack.os_credentials import OSCreds


os_creds = OSCreds(username='admin',
                   password='admin',
                   auth_url='http://localhost:5000/',
                   project_name='admin',
                   identity_api_version=3)

stack_settings = StackSettings(name='qtip_stack',
                               template_path='settings/heat_template.yaml')

stack = OpenStackHeatStack(os_creds, stack_settings)
qtip_stack = stack.create()
