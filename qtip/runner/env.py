##############################################################################
# Copyright (c) 2016 Dell Inc, ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import paramiko
import socket
import time
from os import path
from os.path import expanduser

SCRIPT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir,
                       'scripts')
CONFIG_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir,
                       'config')
PRIVATE_KEY = CONFIG_DIR + 'QtipKey'
PUBLIC_KEY = CONFIG_DIR + 'QtipKey.pub'
IPS_FILE = expanduser('~') + "/qtip/ips.log"


def fetch_compute_ips_via_installer():
    clean_file(IPS_FILE)

    installer_type = str(os.environ['INSTALLER_TYPE'].lower())
    installer_ip = str(os.environ['INSTALLER_IP'])
    if installer_type not in ["fuel"]:
        raise RuntimeError("%s is not supported" % installer_type)
    if not installer_ip:
        raise RuntimeError("undefine environment variable INSTALLER_IP")

    cmd = "bash %s/fetch_compute_ips.sh -i %s -a %s" % \
        (SCRIPT_DIR, installer_type, installer_ip)
    os.system(cmd)
    if path.isfile(IPS_FILE):
        return True
    else:
        return False


def parse_ips():
    ip_list = []
    with open(IPS_FILE, "r") as outfile:
        data = outfile.read()
        if data:
            ip_list.extend(data.rstrip('\n').split('\n'))
    return ip_list


def ssh_test(ip):
    os.system('ssh-keyscan %s >> /root/.ssh/known_hosts' % ip)
    time.sleep(2)

    ssh_cmd = '%s/qtip_creds.sh %s' % (SCRIPT_DIR, ip)
    os.system(ssh_cmd)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, key_filename='{0}/QtipKey'.format(CONFIG_DIR))

    for attempts in range(100):
        try:
            stdin, stdout, stderr = ssh.exec_command('uname')
            if not stderr.readlines():
                print("{0}: SSH test successful")
                return True
        except socket.error:
            if attempts == 99:
                return False
            time.sleep(2)


def ping_test(ip, attempts=30):
    ping_cmd = 'ping -D -c1 {0}'.format(ip)
    for i in range(attempts):
        if os.system(ping_cmd):
            print('\nWaiting for machine\n')
            time.sleep(10)
        else:
            print('\n\n %s is UP \n\n ' % ip)
            return True
        if i == 29:
            return False


def check_nodes_connectivity():
    ip_list = parse_ips()
    for ip in ip_list:
        if not ping_test(ip):
            raise RuntimeError("{0}: Ping test failed".format(ip))
        if not ssh_test(ip):
            raise RuntimeError("{0}: SSH test failed".format(ip))


def generate_host_file():
    ip_list = parse_ips()
    with open('{0}/hosts'.format(CONFIG_DIR), 'w') as host_file:
        for index, item in enumerate(ip_list):
            host_file.write("[host_{0}]\n".format(index))
            host_file.write(item + '\n')


def generate_keypair():
    """Generating ssh keypair"""
    if not clean_keypair():
        raise RuntimeError("Cann't remove old keypair")

    cmd = "ssh-keygen -t rsa -N "" -f {0} -q".format(PRIVATE_KEY)
    os.system(cmd)

    if path.isfile(PRIVATE_KEY) and path.isfile(PUBLIC_KEY):
        return True
    else:
        return False


def clean_file(file_path):
    try:
        if path.isfile(file_path):
            os.remove(file_path)
            print("Removed: " + file_path)
        else:
            print("Not exists: " + file_path)
    except OSError, error:
        print("Not able to Remove: " + file_path, error)
        return False
    return True


def clean_keypair():
    flag = True
    flag &= clean_file(PRIVATE_KEY)
    flag &= clean_file(PUBLIC_KEY)
    return flag
