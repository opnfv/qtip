##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.loader.perftest import Configuration
from qtip.loader.perftest import PerfTest


class Case(object):
    def __init__(self, name, conf=None):
        self._tool = PerfTest(name)
        self.conf = conf if conf is not None else Configuration()
