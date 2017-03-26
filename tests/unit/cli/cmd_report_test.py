###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest
from os import path

from click.testing import CliRunner
from qtip.cli.entry import cli


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="module")
def result_path():
    result = path.join(path.dirname(__file__), path.pardir, path.pardir,
                       'data/reporter')
    return result


def test_dhrystone(runner, result_path):
    """Test dhrystone report"""

    result = runner.invoke(cli, ['report', 'show', 'dhrystone', '-p', result_path])
    assert 'Benchmark .........................................dhrystone' in result.output
    assert 'CPU Usage ......................................... 3%' in result.output
    assert 'Multi CPU' in result.output


def test_whetstone(runner, result_path):
    """ Test whetstone output"""

    result = runner.invoke(cli, ['report', 'show', 'whetstone', '-p', result_path])
    assert 'Number ............................................ 1' in result.output
    assert 'Score ............................................. 633.2' in result.output
    assert 'Single CPU' in result.output


def test_dpi(runner, result_path):
    """ Test dpi report"""
    result = runner.invoke(cli, ['report', 'show', 'dpi', '-p', result_path])
    assert 'CPU Usage ......................................... 3%' in result.output
    assert 'Bits per Second ................................... 3.638' in result.output
    assert 'Packets per Second ................................ 1.45' in result.output


def test_ramspeed(runner, result_path):
    """ Test ramspeed report """
    result = runner.invoke(cli, ['report', 'show', 'ramspeed', '-p', result_path])
    assert 'Float Addition .................................... 10522.33' in result.output
    assert 'Float Average .....................................  9465.11' in result.output
    assert 'Float Copy ........................................ 8434.94' in result.output
    assert 'Float Scale ....................................... 8436.36' in result.output
    assert 'Float Triad ....................................... 10466.82' in result.output
    assert 'Integer Addition .................................. 11489.06' in result.output
    assert 'Integer Average ................................... 11466.52' in result.output
    assert 'Integer Copy ...................................... 11398.52' in result.output
    assert 'Integer Scale ..................................... 11413.87' in result.output


def test_ssl(runner, result_path):
    """ Test ssl report"""

    result = runner.invoke(cli, ['report', 'show', 'ssl', '-p', result_path])
    assert 'AES 128 CBC (bytes)' in result.output
    assert '16 ................................................ 602261.15k' in result.output
    assert '64 ................................................ 650967.68k' in result.output
    assert '256 ............................................... 663959.64k' in result.output
    assert '1024 .............................................. 654325.42k' in result.output
    assert '8192 .............................................. 667303.94k' in result.output


def test_sys(runner, result_path):
    """ Test sys_info """

    result = runner.invoke(cli, ['report', 'show', 'ssl', '-p', result_path])
    assert 'Disk .............................................. 1200.3GB (1.0% used)' in result.output
    assert 'Host Name ......................................... node-38.zte.com.cn' in result.output
    assert 'Kernel ............................................ 4.4.0-62-generic x86_64 (64 bit)'\
           in result.output
    assert 'Memory ............................................ 4403.7/128524.1MB' in result.output
    assert 'Operating System .................................. Ubuntu 16.04 xenial' in result.output
