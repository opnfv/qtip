##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import httplib

import connexion

from qtip.base import error
from qtip.loader import qpi


def list_qpis():
    qpi_spec_list = list(qpi.QPISpec.list_all())
    return qpi_spec_list, httplib.OK


def get_qpi(name):
    try:
        qpi_spec = qpi.QPISpec(name)
        return {'name': qpi_spec.name,
                'abspath': qpi_spec.abspath,
                'content': qpi_spec.content}, httplib.OK
    except error.NotFoundError:
        return connexion.problem(httplib.NOT_FOUND,
                                 'QPI Not Found',
                                 'Requested QPI Spec `' + name + '` not found.')
