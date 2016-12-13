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


class PerfTest(Benchmark):
    """WIP(yujunz):
    a perftest is the driver of external performance test tools
    It is usually referred in a suite to collect performance metric"""

    # paths to search for perftest
    _paths = [path.join(p, 'perftest') for p in Benchmark._paths]
