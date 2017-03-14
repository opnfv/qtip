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

import common
from qtip.base import error
from qtip.loader import metric


def list_metrics():
    metric_list = list(metric.MetricSpec.list_all())
    return metric_list, httplib.OK


@common.get_one_exceptions(resource='metric')
def get_metric(name):
        metric_spec = metric.MetricSpec(name)
        return {'name': metric_spec.name,
                'abspath': metric_spec.abspath,
                'content': metric_spec.content}
