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
    """Test dhrystone report"""

    result = console_reporter.render('dhrystone', result_path)
    assert 'Benchmark .........................................dhrystone' in result
    assert 'CPU Usage ......................................... 3%' in result
    assert 'Multi CPU' in result


def test_whetstone(console_reporter, result_path):
    """ Test whetstone output"""

    result = console_reporter.render('whetstone', result_path)
    assert 'Number ............................................ 1' in result
    assert 'Score ............................................. 633.2' in result
    assert 'Single CPU' in result


def test_dpi(console_reporter, result_path):
    """ Test dpi report"""

    result = console_reporter.render('dpi', result_path)
    assert 'CPU Usage ......................................... 3%' in result
    assert 'Bits per Second ................................... 3.638' in result
    assert 'Packets per Second ................................ 1.45' in result


def test_ramspeed(console_reporter, result_path):
    """ Test ramspeed report """

    result = console_reporter.render('ramspeed', result_path)
    assert 'Float Addition .................................... 10522.33' in result
    assert 'Float Average .....................................  9465.11' in result
    assert 'Float Copy ........................................ 8434.94' in result
    assert 'Float Scale ....................................... 8436.36' in result
    assert 'Float Triad ....................................... 10466.82' in result
    assert 'Integer Addition .................................. 11489.06' in result
    assert 'Integer Average ................................... 11466.52' in result
    assert 'Integer Copy ...................................... 11398.52' in result
    assert 'Integer Scale ..................................... 11413.87' in result


def test_ssl(console_reporter, result_path):
    """ Test ssl report"""

    result = console_reporter.render('ssl', result_path)
    assert 'AES 128 CBC (bytes)' in result
    assert '16 ................................................ 602261.15k' in result
    assert '64 ................................................ 650967.68k' in result
    assert '256 ............................................... 663959.64k' in result
    assert '1024 .............................................. 654325.42k' in result
    assert '8192 .............................................. 667303.94k' in result


def test_sys(console_reporter, result_path):
    """ Test sys_info """

    result = console_reporter.render('ssl', result_path)
    assert 'Disk .............................................. 1200.3GB (1.0% used)' in result
    assert 'Host Name ......................................... node-38.zte.com.cn' in result
    assert 'Kernel ............................................ 4.4.0-62-generic x86_64 (64 bit)'\
           in result
    assert 'Memory ............................................ 4403.7/128524.1MB' in result
    assert 'Operating System .................................. Ubuntu 16.04 xenial' in result
