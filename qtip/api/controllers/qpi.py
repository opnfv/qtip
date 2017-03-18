##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import httplib

from qtip.api.controllers import common
from qtip.loader import qpi


def list_qpis():
    qpi_spec_list = list(qpi.QPISpec.list_all())
    qpi_spec_list = map(lambda x: x['name'], qpi_spec_list)
    return {'qpis': qpi_spec_list}, httplib.OK


@common.check_resource(resource='QPI')
def get_qpi(name):
    qpi_spec = qpi.QPISpec(name)
    return qpi_spec.content
