###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import time

import pytest
import mock
from collections import defaultdict
import socket

from qtip.util import env
from qtip.util.env import AnsibleEnvSetup


@pytest.fixture(scope='session')
def ansible_envsetup():
    return AnsibleEnvSetup()


@pytest.fixture()
def hostfile(tmpdir):
    fake_hostfile = tmpdir.join('hosts')
    fake_hostfile.write("[hosts]\n")
    fake_hostfile.write("10.20.0.3")
    return fake_hostfile


@pytest.fixture()
def private_key(tmpdir):
    fake_private_key = tmpdir.join('QtipKey')
    fake_private_key.write("fake keypair")
    return fake_private_key


@pytest.fixture()
def public_key(tmpdir):
    fake_public_key = tmpdir.join('QtipKey.pub')
    fake_public_key.write("fake public key")
    return fake_public_key


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


def test_init(ansible_envsetup):
    assert 'AnsibleEnvSetup' in str(type(ansible_envsetup))
    assert ansible_envsetup.keypair == defaultdict(str)
    assert ansible_envsetup.hostfile is None
    assert ansible_envsetup.host_ip_list == []


def test_setup_exception(mocker, ansible_envsetup, hostfile):
    with mock.patch.object(AnsibleEnvSetup, 'check_hostfile', side_effect=RuntimeError()):
        mock_os = mocker.patch('sys.exit')
        ansible_envsetup.setup({'hostfile': str(hostfile)})
        assert mock_os.call_count == 1


# TODO(zhihui_wu) Need find a smart way to write this pytest
def test_setup(mocker, ansible_envsetup):
    mock_check_hostfile = \
        mocker.patch.object(AnsibleEnvSetup, 'check_hostfile')
    mock_generate_default_hostfile = \
        mocker.patch.object(AnsibleEnvSetup, 'generate_default_hostfile')
    mock_fetch_ip = \
        mocker.patch.object(AnsibleEnvSetup, 'fetch_host_ip_from_hostfile')
    mock_check_keypair = \
        mocker.patch.object(AnsibleEnvSetup, 'check_keypair')
    mock_generate_default_keypair = \
        mocker.patch.object(AnsibleEnvSetup, 'generate_default_keypair')
    mock_pass_keypair = \
        mocker.patch.object(AnsibleEnvSetup, 'pass_keypair_to_remote')
    mock_check_ssh = \
        mocker.patch.object(AnsibleEnvSetup, 'check_hosts_ssh_connectivity')

    ansible_envsetup.setup({'keypair': str(private_key),
                            'hostfile': str(hostfile)})
    mock_check_hostfile.assert_called_with(str(hostfile))
    mock_fetch_ip.assert_called_with()
    mock_check_keypair.assert_called_with(str(private_key))
    mock_pass_keypair.assert_called_with()
    mock_check_ssh.assert_called_with()

    ansible_envsetup.setup({'keypair': str(private_key)})
    mock_generate_default_hostfile.assert_called_with()
    mock_fetch_ip.assert_called_with()
    mock_check_keypair.assert_called_with(str(private_key))
    mock_pass_keypair.assert_called_with()
    mock_check_ssh.assert_called_with()

    ansible_envsetup.setup({'hostfile': str(hostfile)})
    mock_check_hostfile.assert_called_with(str(hostfile))
    mock_fetch_ip.assert_called_with()
    mock_generate_default_keypair.assert_called_with()
    mock_pass_keypair.assert_called_with()
    mock_check_ssh.assert_called_with()

    ansible_envsetup.setup()
    mock_generate_default_hostfile.assert_called_with()
    mock_fetch_ip.assert_called_with()
    mock_generate_default_keypair.assert_called_with()
    mock_pass_keypair.assert_called_with()
    mock_check_ssh.assert_called_with()


def test_check_keypair(mocker, ansible_envsetup, private_key, public_key):
    with mocker.patch.object(env, 'all_files_exist', return_value=True):
        ansible_envsetup.check_keypair(str(private_key))
    assert ansible_envsetup.keypair['private'] == str(private_key)
    assert ansible_envsetup.keypair['public'] == str(public_key)


def test_check_keypair_failed(mocker, ansible_envsetup):
    mocker.patch.object(env, 'all_files_exist', return_value=False)
    with pytest.raises(RuntimeError) as excinfo:
        ansible_envsetup.check_keypair(str(private_key))
    assert 'The keypairs you in the configuration file ' \
           'is invalid or not existed.' == str(excinfo.value)
    assert ansible_envsetup.keypair['private'] == ''
    assert ansible_envsetup.keypair['public'] == ''


@pytest.mark.parametrize("file_existence, expected", [
    (True, 0),
    (False, 1)
])
def test_generate_default_keypair(mocker, ansible_envsetup, file_existence, expected):
    mock_os = mocker.patch('os.system')
    mocker.patch.object(env, 'all_files_exist', return_value=file_existence)
    ansible_envsetup.generate_default_keypair()
    assert mock_os.call_count == expected
    assert ansible_envsetup.keypair['private'] == env.PRIVATE_KEY
    assert ansible_envsetup.keypair['public'] == env.PUBLIC_KEY


@pytest.mark.parametrize("ips, expected", [
    (['10.20.0.3'], 1),
    (['10.20.0.3', '10.20.0.4'], 2)
])
def test_pass_keypair_to_remote_successful(mocker, ansible_envsetup, ips, expected):
    ansible_envsetup.host_ip_list = ips
    mock_pass_keypair = \
        mocker.patch.object(AnsibleEnvSetup, '_pass_keypair', return_value=True)
    ansible_envsetup.pass_keypair_to_remote()
    assert mock_pass_keypair.call_count == expected


def test_pass_keypair_to_remote_failed(mocker, ansible_envsetup):
    ansible_envsetup.host_ip_list = ['10.20.0.3']
    mocker.patch.object(AnsibleEnvSetup, '_pass_keypair', return_value=False)
    with pytest.raises(RuntimeError) as excinfo:
        ansible_envsetup.pass_keypair_to_remote()
    assert "Failed on passing keypair to remote." in str(excinfo.value)


def test_pass_keypair(monkeypatch, mocker, ansible_envsetup):
    monkeypatch.setattr(time, 'sleep', lambda s: None)
    mock_os = mocker.patch('os.system')
    ansible_envsetup._pass_keypair('10.20.0.3', str(private_key))
    assert mock_os.call_count == 2


def test_pass_keypair_exception(ansible_envsetup):
    with mock.patch('os.system', side_effect=Exception()) as mock_os:
        result = ansible_envsetup._pass_keypair('10.20.0.3', str(private_key))
        assert result is False
        assert mock_os.call_count == 1


def test_check_hostfile(mocker, ansible_envsetup, hostfile):
    ansible_envsetup.check_hostfile(str(hostfile))
    assert ansible_envsetup.hostfile == str(hostfile)

    with pytest.raises(RuntimeError) as excinfo:
        mocker.patch.object(env, 'all_files_exist', return_value=False)
        ansible_envsetup.check_hostfile(str(hostfile))
    assert str(excinfo.value) == 'The hostfile {0} is invalid or not ' \
                                 'existed.'.format(str(hostfile))


def test_default_hostfile_non_existed(mocker, ansible_envsetup):
    with mocker.patch.object(env, 'all_files_exist', return_value=False):
            mock_generate_hostfile_via_installer = \
                mocker.patch.object(AnsibleEnvSetup,
                                    '_generate_hostfile_via_installer')
            ansible_envsetup.generate_default_hostfile()
            mock_generate_hostfile_via_installer.assert_called_once_with()


def test_default_hostfile_existed(mocker, ansible_envsetup):
    with mocker.patch.object(env, 'all_files_exist', return_value=True):
        mock_generate_hostfile_via_installer = \
            mocker.patch.object(AnsibleEnvSetup,
                                '_generate_hostfile_via_installer')
        ansible_envsetup.generate_default_hostfile()
        mock_generate_hostfile_via_installer.assert_not_called()


@pytest.mark.parametrize("test_input, expected", [
    (({}, KeyError), 'INSTALLER_TYPE'),
    (({'INSTALLER_TYPE': 'fuel'}, KeyError), 'INSTALLER_IP'),
    (({'INSTALLER_TYPE': 'fuel_1', 'INSTALLER_IP': '10.20.0.2'}, ValueError),
     'fuel_1 is not supported'),
    (({'INSTALLER_TYPE': 'fuel', 'INSTALLER_IP': ''}, ValueError),
     'The value of environment variable INSTALLER_IP is empty')
])
def test_generate_hostfile_via_installer_exception(monkeypatch, ansible_envsetup, test_input, expected):
    if test_input[0]:
        for key in test_input[0]:
            monkeypatch.setenv(key, test_input[0][key])

    with pytest.raises(test_input[1]) as excinfo:
        ansible_envsetup._generate_hostfile_via_installer()
    assert expected in str(excinfo.value)


def test_generate_hostfile_via_installer(monkeypatch, mocker, ansible_envsetup):
    monkeypatch.setenv('INSTALLER_TYPE', 'fuel')
    monkeypatch.setenv('INSTALLER_IP', '10.20.0.2')
    mock_os = mocker.patch('os.system')
    ansible_envsetup._generate_hostfile_via_installer()
    assert mock_os.call_count == 1
    assert ansible_envsetup.hostfile == env.HOST_FILE


def test_fetch_host_ip_from_hostfile(ansible_envsetup, hostfile):
    ansible_envsetup.hostfile = str(hostfile)
    ansible_envsetup.fetch_host_ip_from_hostfile()
    assert ansible_envsetup.host_ip_list == ['10.20.0.3']


def test_fetch_host_ip_from_empty_hostfile(ansible_envsetup, tmpdir):
    empty_hostfile = tmpdir.join('empty_hostfile')
    empty_hostfile.write("")
    ansible_envsetup.hostfile = str(empty_hostfile)
    with pytest.raises(ValueError) as excinfo:
        ansible_envsetup.fetch_host_ip_from_hostfile()
    assert str(excinfo.value) == "The hostfile doesn't include host ip addresses."


@pytest.mark.parametrize("ips, expected", [
    (['10.20.0.3'], 1),
    (['10.20.0.3', '10.20.0.4'], 2)
])
def test_check_hosts_ssh_connectivity(mocker, ansible_envsetup, ips, expected):
    ansible_envsetup.host_ip_list = ips
    mock_ssh_is_ok = \
        mocker.patch.object(AnsibleEnvSetup, '_ssh_is_ok', return_value=True)
    ansible_envsetup.check_hosts_ssh_connectivity()
    assert mock_ssh_is_ok.call_count == expected


def test_check_hosts_ssh_connectivity_failed(mocker, ansible_envsetup):
    ansible_envsetup.host_ip_list = ['10.20.0.3']
    mocker.patch.object(AnsibleEnvSetup, '_ssh_is_ok', return_value=False)
    with pytest.raises(RuntimeError) as excinfo:
        ansible_envsetup.check_hosts_ssh_connectivity()
    assert "Failed on checking hosts ssh connectivity." == str(excinfo.value)


@pytest.mark.parametrize("stderrinfo, expected", [
    ('', True),
    ('sorry', False)
])
def test_ssh_is_ok(mocker, ansible_envsetup, private_key, stderrinfo, expected):
    stderr = mock.MagicMock()
    stderr.readlines.return_value = stderrinfo
    mock_sshclient = mocker.patch('paramiko.SSHClient')
    test_ssh_client = mock_sshclient.return_value
    test_ssh_client.exec_command.return_value = ('', '', stderr)
    result = ansible_envsetup._ssh_is_ok('10.20.0.3', str(private_key))
    assert result == expected
    test_ssh_client.connect.assert_called_once_with(
        '10.20.0.3', key_filename=str(private_key))
    test_ssh_client.exec_command.assert_called_with('uname')


def test_ssh_exception(monkeypatch, mocker, ansible_envsetup):
    monkeypatch.setattr(time, 'sleep', lambda s: None)
    mock_sshclient = mocker.patch('paramiko.SSHClient')
    test_ssh_client = mock_sshclient.return_value
    test_ssh_client.exec_command.side_effect = socket.error()
    result = ansible_envsetup._ssh_is_ok('10.20.0.3', str(private_key), attempts=1)
    assert result is False
