##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path

from benchmark import Benchmark


class TestPlan(Benchmark):
    """WIP(yujunz):
    a test plan is consist of test condition and several suites which can be
    executed by user"""

    # paths to search for suites
    _paths = [path.join(p, 'testplan') for p in Benchmark._paths]
