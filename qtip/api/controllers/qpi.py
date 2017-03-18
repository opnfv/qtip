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
    qpi_specs = list(qpi.QPISpec.list_all())
    qpis_by_name = [q['name'] for q in qpi_specs]
    return {'qpis': qpis_by_name}, httplib.OK


@common.check_endpoint_for_error(resource='QPI')
def get_qpi(name):
    qpi_spec = qpi.QPISpec(name)
    return qpi_spec.content
