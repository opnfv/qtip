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


class Suite(Benchmark):
    """WIP(yujunz):
    a suite is consist of one or several perf tests and produces one QPI.
    It must be executed as part of testplan
    """

    # paths to search for suites
    _paths = [path.join(p, 'suite') for p in Benchmark._paths]


class Condition(object):
    """Suite execution condition"""
    pass
