##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import connexion


def list_metrics():
    return connexion.problem(501,
                             'List metrics',
                             'Metrics listing not implemented')


def get_metric(name):
    return connexion.problem(501,
                             'Get a metric',
                             'metric retrieval not implemented')
