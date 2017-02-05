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


def test_run(logfile_collector):
    collected = logfile_collector.run()
    assert collected['groupdict'] == {
        'event_posted': '1482894965.3',
        'host_down': '1482894965.51',
        'network_down': '1482894965.164096803',
        'notified': '1482894965.63',
        'vm_error': '1482894965.3'
    }
    assert list(collected['groups']) == ['1482894965.63',
                                         '1482894965.3',
                                         '1482894965.3',
                                         '1482894965.51',
                                         '1482894965.164096803']
