##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import connexion


def list_qpis():
    return connexion.problem(501,
                             'List QPIs',
                             'QPIs listing not implemented')


def get_qpi(qpi_name):
    return connexion.problem(501,
                             'Get a QPI',
                             'QPI retrieval not implemented')
