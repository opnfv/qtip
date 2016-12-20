##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.base.benchmark import Property
from qtip.spec.metric import MetricSpec


class Case(object):
    def __init__(self, spec, paths=None):
        self.metric_spec = MetricSpec(spec[Property.METRIC], paths=paths)
        self.config = spec[Property.CONFIG]
