##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from datetime import datetime
from os import path

from qtip.base.benchmark import Benchmark


class TestPlan(Benchmark):
    """WIP(yujunz):
    a test plan is consist of test condition and several suites which can be
    executed by user"""

    # paths to search for suites
    _paths = [path.join(p, 'testplan') for p in Benchmark._paths]

    def __init__(self, name, info=None):
        super(TestPlan, self).__init__(name)

        # TODO(yujunz) load information from file
        self.info = info if info is not None else Info()
        self.tasks = []


class Info(object):
    """Basic benchmark plan information"""
    def __init__(self, facility="Demo Lab", engineer="Demo User"):
        self.facility = facility
        self.engineer = engineer
        self.datetime = datetime.now()
