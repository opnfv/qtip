###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import time

import mock
import pytest

from qtip.util import env


def test_all_files_exist(tmpdir):
    exist_file = tmpdir.mkdir('qtip').join('hello.txt')
    exist_file.write("hello")
    non_exist_file = tmpdir.strpath + '/tmp.txt'
    assert env.all_files_exist() is False
    assert env.all_files_exist(str(exist_file))
    assert env.all_files_exist(non_exist_file) is False
    assert env.all_files_exist(str(exist_file), non_exist_file) is False


def test_clean_file(tmpdir):
    exist_file = tmpdir.mkdir('qtip').join('hello.txt')
    exist_file.write("hello")
    non_exist_file = tmpdir.strpath + '/tmp.txt'

    assert env.clean_file() is False
    assert env.clean_file(str(exist_file))
    assert env.clean_file(non_exist_file)


def test_generate_host_file_without_setenv(monkeypatch):
    def setenv(*args):
        monkeypatch.setenv('INSTALLER_TYPE', args[0])
        monkeypatch.setenv('INSTALLER_IP', args[1])

    with pytest.raises(KeyError) as excinfo:
        env.generate_host_file()
    assert 'INSTALLER_TYPE' in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        setenv('fuel_1', '10.20.0.2')
        env.generate_host_file()
    assert 'fuel_1 is not supported' in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        setenv('fuel', '')
        env.generate_host_file()
    assert 'The value of environment variable INSTALLER_IP is empty' \
           in str(excinfo.value)


def test_generate_host_file(monkeypatch, tmpdir):
    monkeypatch.setenv('INSTALLER_TYPE', 'fuel')
    monkeypatch.setenv('INSTALLER_IP', '10.20.0.2')
    hostfile = tmpdir.mkdir('qtip').join('hosts')
    hostfile.write('')
    assert env.generate_host_file(str(hostfile))


def test_generate_keypair():
    with mock.patch('os.system') as mock_os:
        env.generate_keypair()
        assert mock_os.call_count == 1


def test_pass_keypair(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda s: None)
    with mock.patch('os.system') as mock_os:
        env.pass_keypair('10.20.0.10')
        assert mock_os.call_count == 2


@pytest.mark.parametrize("stderrinfo, expected", [
    ('', True),
    ('sorry', False)
])
@mock.patch('paramiko.SSHClient')
def test_ssh_is_ok(mock_sshclient, stderrinfo, expected):
    stderr = mock.MagicMock()
    stderr.readlines.return_value = stderrinfo
    test_ssh_client = mock_sshclient.return_value
    test_ssh_client.exec_command.return_value = ('', '', stderr)
    result = env.ssh_is_ok('10.20.0.3')
    assert result == expected
    test_ssh_client.connect.assert_called_once_with(
        '10.20.0.3', key_filename=env.PRIVATE_KEY)
    test_ssh_client.exec_command.assert_called_with('uname')
