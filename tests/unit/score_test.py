##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path
import pytest
from qtip import score


def test_storperf(data_root):
    report_file = path.join(data_root, 'external', 'storperf', 'report.json')
    qpi_report = score.storperf(report_file)
    assert qpi_report['sections'][0]['score'] == pytest.approx(1.869, 0.1)  # IOPS
    assert qpi_report['sections'][1]['score'] == pytest.approx(0.722, 0.1)  # Throughput
    assert qpi_report['sections'][2]['score'] == pytest.approx(1.896, 0.1)  # Latency
    assert(qpi_report['score'] == 3064)  # 3064 is calculated manually
