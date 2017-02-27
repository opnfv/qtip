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

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, 'scripts')
KEYNAME = 'QtipKey'
PRIVATE_KEY = '{0}/qtip/{1}'.format(os.environ['HOME'], KEYNAME)
PUBLIC_KEY = PRIVATE_KEY + '.pub'
HOST_FILE = '{0}/qtip/hosts'.format(os.environ['HOME'])


def check_file_exist(*files):
    if len(files) == 0:
        return False
    flag = True
    for f_item in files:
        flag &= os.path.isfile(f_item)
        print("Is {0} existed: {1}".format(f_item, flag))
    return flag


def clean_file(*files):
    if len(files) == 0:
        print('Nothing to clean')
        return False

    def clean(f):
        try:
            if check_file_exist(f):
                os.remove(f)
                print("Removed: {0}".format(f))
            else:
                print("Not exists: {0}".format(f))
            return True
        except OSError as error:
            print("Not able to Remove: {0}".format(f), error)
            return False

    results = map(clean, files)
    return len(results) == len(files) and False not in results


def generate_host_file(hostfile=HOST_FILE):
    installer_type = str(os.environ['INSTALLER_TYPE'].lower())
    installer_ip = str(os.environ['INSTALLER_IP'])

    if installer_type not in ["fuel"]:
        raise ValueError("%s is not supported" % installer_type)
    if not installer_ip:
        raise ValueError("The value of environment variable INSTALLER_IP is empty")

    cmd = "bash %s/generate_host_file.sh -i %s -a %s -d %s" % \
        (SCRIPT_DIR, installer_type, installer_ip, hostfile)
    os.system(cmd)
    return check_file_exist(hostfile)


def generate_keypair(keyname='QtipKey'):
    """Generating ssh keypair"""
    cmd = "ssh-keygen -t rsa -N "" -f {0} -q".format(keyname)
    os.system(cmd)
    return check_file_exist(PRIVATE_KEY, PUBLIC_KEY)


def pass_keypair(ip, private_key=PRIVATE_KEY):
    os.system('ssh-keyscan %s >> /root/.ssh/known_hosts' % ip)
    time.sleep(2)

    ssh_cmd = '%s/qtip_creds.sh %s %s' % (SCRIPT_DIR, ip, private_key)
    os.system(ssh_cmd)


def ssh_test(ip, private_key=PRIVATE_KEY, attempts=100):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, key_filename=private_key)

    for attempt in range(attempts):
        try:
            stdin, stdout, stderr = ssh.exec_command('uname')
            if not stderr.readlines():
                print("{0}: SSH test successful".format(ip))
                return True
        except socket.error:
            if attempt == (attempts - 1):
                return False
            print("%s times ssh test......failed" % attempt)
            time.sleep(2)
    return False
