##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.reporter.console import ConsoleReporter


@pytest.fixture
def console_reporter():
    return ConsoleReporter({})


def test_constructor(console_reporter):
    assert isinstance(console_reporter, ConsoleReporter)


def test_timeline(console_reporter):

    result = console_reporter.render('timeline.json')
    assert "\n\nMONITORTIME\n\nT00" in result
    assert "1\n\n\nINSPECTORTIME\n\nT01" in result
    assert "\n\n\nCONTROLLERTIME\n\n" in result


def test_composition(console_reporter):

    result = console_reporter.render('detail.json')
    assert "Index: 0.0" in result
    assert "Plan: opnfv" in result
    assert "Start Time: 2017-02-24T14:48:44.543746" in result
    assert "Stop Time: 2017-02-24T15:48:44.543746" in result
    assert "CPU Usage: 3.0%" in result
    assert "Host Name: node-6.zte.com.cn" in result
    assert "Name: dpi" in result
    assert "Index: 95" in result
