##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from os import path

from qtip.reporter.console import ConsoleReporter


@pytest.fixture
def console_reporter():
    return ConsoleReporter({})


@pytest.fixture
def result_path():
    result = path.join(path.dirname(__file__), path.pardir, path.pardir,
                       'data/reporter')
    return result


def test_constructor(console_reporter):
    assert isinstance(console_reporter, ConsoleReporter)


def test_dhrystone(console_reporter, result_path):
    """ Test dhrystone report"""

    result = console_reporter.render('dhrystone', result_path)
    assert "Benchmark: dhrystone" in result
    assert "Number: 40" in result
    assert "Score: 63529.6" in result
    assert "Single CPU:" in result
    assert "Total CPUs: 40" in result


def test_whetstone(console_reporter, result_path):
    """ Test whetstone output"""

    result = console_reporter.render('whetstone', result_path)
    assert "Benchmark: whetstone" in result
    assert "Results:" in result
    assert "Multi CPU:" in result
    assert "Number: 40" in result
    assert "Score: 21198.3" in result
    assert "Single CPU:" in result


def test_dpi(console_reporter, result_path):
    """ Test dpi report"""

    result = console_reporter.render('dpi', result_path)
    assert "Benchmark: dpi" in result
    assert "Bits per Second: 3.638" in result
    assert "Packets per Second: 1.45" in result
    assert "Bits per Second: 3.69" in result
    assert "Packets per Second: 1.458" in result


def test_ramspeed(console_reporter, result_path):
    """ Test ramspeed report """

    result = console_reporter.render('ramspeed', result_path)
    assert "Float Addition: 10217.62" in result
    assert "Float Average: 9176.88" in result
    assert "Float Copy: 8127.13" in result
    assert "Float Scale: 8085.40" in result
    assert "Float Triad: 10277.38" in result
    assert "Integer Addition: 11471.63" in result
    assert "Integer Average: 11396.35" in result


def test_ssl(console_reporter, result_path):
    """ Test ssl report"""

    result = console_reporter.render('ssl', result_path)
    assert "AES 128 CBC (bytes):" in result
    assert "256: 584951.30k" in result
    assert "RSA SIGN:" in result
    assert "2048: 9.9" in result
    assert "RSA VERIFY:" in result
    assert "4096: 7688.5" in result


def test_sys(console_reporter, result_path):
    """ Test sys_info """

    result = console_reporter.render('ssl', result_path)
    assert "System Information:" in result
    assert "Host Name: node-38.zte.com.cn" in result
    assert "Memory: 4403.7/128524.1MB" in result
