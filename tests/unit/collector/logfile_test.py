##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.collector.logfile import LogfileCollector


@pytest.fixture
def logfile_collector(logfile_config, plan):
    return LogfileCollector(logfile_config, plan)


# TODO(yujunz) fix me
@pytest.xfail
def test_run(logfile_collector):
    collected = logfile_collector.run()
    assert list(collected) == []
