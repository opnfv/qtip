##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from qtip.loader.plan import load_collector
from qtip.collector import CollectorProp as CProp


def test_load_collector(collectors_config):
    for c in collectors_config:
        collector = load_collector(c[CProp.TYPE])
        assert collector.TYPE == c[CProp.TYPE]
