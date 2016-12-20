##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.base.benchmark import Property
from qtip.spec.qpi import QPISpec
from qtip.runner.case import Case


class Suite(object):
    """a suite of benchmark cases under specified condition"""
    def __init__(self, spec, paths=None):
        self._paths = paths
        self.qpi_spec = QPISpec(spec[Property.QPI_SPEC], paths=paths)
        self.condition = spec[Property.CONDITION]
        self.cases = [Case(case_spec, paths)
                      for case_spec in spec[Property.CASES]]
