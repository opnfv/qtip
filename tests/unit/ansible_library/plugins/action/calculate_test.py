##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.ansible_library.plugins.action import calculate


def test_calc_metric(metric_spec, metrics, metric_baseline, metric_result):
    assert calculate.calc_metric(metric_spec,
                                 metrics['ssl_rsa'],
                                 metric_baseline) == metric_result


def test_calc_section(section_spec, metrics, section_baseline, section_result):
    assert calculate.calc_section(section_spec,
                                  metrics,
                                  section_baseline) == section_result


def test_calc_qpi(qpi_spec, metrics, qpi_baseline, qpi_result, section_spec, info):
    section_spec['score'] = 1.0
    assert calculate.calc_qpi(qpi_spec,
                              metrics,
                              info, qpi_baseline) == qpi_result


@pytest.mark.parametrize('metrics, baseline, expected', [
    (['612376.96k'], '612376.96k', 1)
])
def test_calc_score(metrics, baseline, expected):
    assert calculate.calc_score(metrics, baseline) == expected
