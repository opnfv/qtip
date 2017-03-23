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
    assert "Benchmark: dhrystone" in result.output
    assert "CPU Usage: 3%" in result.output
    assert "Number: 40" in result.output
    assert "Score: 63529.6" in result.output
    assert "Single CPU:" in result.output
    assert "Total CPUs: 40" in result.output


def test_whetstone(runner, result_path):
    """ Test whetstone output"""

    result = runner.invoke(cli, ['report', 'show', 'whetstone', '-p', result_path])
    assert "Benchmark: whetstone" in result.output
    assert "CPU Usage: 3%" in result.output
    assert "Results:" in result.output
    assert "Multi CPU:" in result.output
    assert "Number: 40" in result.output
    assert "Score: 21198.3" in result.output
    assert "Single CPU:" in result.output


def test_dpi(runner, result_path):
    """ Test dpi report"""
    result = runner.invoke(cli, ['report', 'show', 'dpi', '-p', result_path])
    assert "Benchmark: dpi" in result.output
    assert "CPU Usage: 3%" in result.output
    assert "Bits per Second: 3.638" in result.output
    assert "Packets per Second: 1.45" in result.output
    assert "Bits per Second: 3.69" in result.output
    assert "Packets per Second: 1.458" in result.output


def test_ramspeed(runner, result_path):
    """ Test ramspeed report """
    result = runner.invoke(cli, ['report', 'show', 'ramspeed', '-p', result_path])
    assert "Benchmark: ramspeed" in result.output
    assert "CPU Usage: 3%" in result.output
    assert "Float Addition: 10217.62" in result.output
    assert "Float Average: 9176.88" in result.output
    assert "Float Copy: 8127.13" in result.output
    assert "Float Scale: 8085.40" in result.output
    assert "Float Triad: 10277.38" in result.output
    assert "Integer Addition: 11471.63" in result.output
    assert "Integer Average: 11396.35" in result.output


def test_ssl(runner, result_path):
    """ Test ssl report"""

    result = runner.invoke(cli, ['report', 'show', 'ssl', '-p', result_path])
    assert "Benchmark: ssl" in result.output
    assert "CPU Usage: 3%" in result.output
    assert "AES 128 CBC (bytes):" in result.output
    assert "256: 584951.30k" in result.output
    assert "RSA SIGN:" in result.output
    assert "2048: 9.9" in result.output
    assert "RSA VERIFY:" in result.output
    assert "4096: 7688.5" in result.output


def test_sys(runner, result_path):
    """ Test sys_info """

    result = runner.invoke(cli, ['report', 'show', 'ssl', '-p', result_path])
    assert "System Information:" in result.output
    assert "Host Name: node-38.zte.com.cn" in result.output
    assert "Memory: 4403.7/128524.1MB" in result.output
