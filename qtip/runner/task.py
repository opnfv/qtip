##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.loader.suite import Condition
from qtip.loader.suite import Suite
from qtip.runner.case import Case


class Task(object):
    """Benchmark task to execute a specific suite"""
    def __init__(self, suite_name, condition=None):
        super(Task, self).__init__()
        self._suite = Suite(suite_name)
        self.condition = condition if condition is not None else Condition()
        self.cases = []
        for case in self._suite.create_cases(condition):
            self.cases.append(Case(case.tool, case.conf))
