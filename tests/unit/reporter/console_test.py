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
    assert "Benchmark..............................................................." \
           "...................dhrystone" in result


def test_whetstone(console_reporter, result_path):
    """ Test whetstone output"""

    result = console_reporter.render('whetstone', result_path)
    assert "Number................................................................." \
           "...........................40" in result
    assert "Total CPUs............................................................." \
           "...........................40" in result


def test_dpi(console_reporter, result_path):
    """ Test dpi report"""

    result = console_reporter.render('dpi', result_path)
    assert "Bits per Second..................................................." \
           ".............................3.638" in result
    assert "Packets per Second................................................" \
           ".............................1.458" in result


def test_ramspeed(console_reporter, result_path):
    """ Test ramspeed report """

    result = console_reporter.render('ramspeed', result_path)
    assert "Float Addition........................................................" \
           "......................10522.33" in result
    assert "Integer Average........................................................" \
           ".....................11466.52" in result


def test_ssl(console_reporter, result_path):
    """ Test ssl report"""

    result = console_reporter.render('ssl', result_path)
    assert "8192............................................................." \
           ".........................667303.94k" in result
    assert "1024.............................................................." \
           "..........................100088.3" in result


def test_sys(console_reporter, result_path):
    """ Test sys_info """

    result = console_reporter.render('ssl', result_path)
    assert "System Information" in result
    assert "Host Name........................................................" \
           ".................node-38.zte.com.cn" in result
    assert "Operating System.................................................." \
           "...............Ubuntu 16.04 xenial" in result
