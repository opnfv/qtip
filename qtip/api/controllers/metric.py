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
from qtip.loader import metric


def list_metrics():
    metric_list = list(metric.MetricSpec.list_all())
    metric_list = map(lambda x: x['name'], metric_list)
    return {'metrics': metric_list}, httplib.OK


@common.check_resource(resource='Metric')
def get_metric(name):
    metric_spec = metric.MetricSpec(name)
    return metric_spec.content
