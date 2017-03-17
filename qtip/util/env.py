##############################################################################
# Copyright (c) 2017 ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from collections import defaultdict
import os
from os import path
import re
import socket
import sys
import time

import paramiko

from qtip.util.logger import QtipLogger

logger = QtipLogger('env').get

SCRIPT_DIR = path.join(path.dirname(__file__), path.pardir, 'scripts')
KEYNAME = 'QtipKey'
PRIVATE_KEY = '{0}/qtip/{1}'.format(os.environ['HOME'], KEYNAME)
PUBLIC_KEY = PRIVATE_KEY + '.pub'
HOST_FILE = '{0}/qtip/hosts'.format(os.environ['HOME'])


def all_files_exist(*files):
    if len(files) == 0:
        return False
    flag = True
    for f_item in files:
        flag &= path.isfile(f_item)
        logger.info("Is {0} existed: {1}".format(f_item, flag))
    return flag


def clean_file(*files):
    if len(files) == 0:
        logger.info('Nothing to clean')
        return False

    def clean(f):
        try:
            if all_files_exist(f):
                os.remove(f)
                logger.info("Removed: {0}".format(f))
            else:
                logger.info("Not exists: {0}".format(f))
            return True
        except OSError as error:
            logger.error("Not able to Remove: {0}".format(f), error)
            return False

    results = map(clean, files)
    return len(results) == len(files) and False not in results


class AnsibleEnvSetup(object):
    def __init__(self):
        self.keypair = defaultdict(str)
        self.hostfile = None
        self.host_ip_list = []

    def setup(self, config={}):
        try:
            if 'hostfile' in config:
                self.check_hostfile(config['hostfile'])
            else:
                self.generate_default_hostfile()
            self.fetch_host_ip_from_hostfile()
            if 'keypair' in config:
                self.check_keypair(config['keypair'])
            else:
                self.generate_default_keypair()
            self.pass_keypair_to_remote()
            self.check_hosts_ssh_connectivity()
        except Exception as error:
            logger.info(error)
            sys.exit(1)

    def check_keypair(self, keypair):
        self.keypair = defaultdict(str)
        if all_files_exist(keypair, '{0}.pub'.format(keypair)):
            self.keypair['private'] = keypair
            self.keypair['public'] = '{0}.pub'.format(keypair)
        else:
            raise RuntimeError("The keypairs you in the configuration file"
                               " is invalid or not existed.")

    def generate_default_keypair(self):
        if not all_files_exist(PRIVATE_KEY, PUBLIC_KEY):
            logger.info("Generate default keypair {0} under "
                        "{1}".format(KEYNAME, os.environ['HOME']))
            cmd = '''ssh-keygen -t rsa -N "" -f {0} -q -b 2048'''.format(PRIVATE_KEY)
            os.system(cmd)
        self.keypair['private'] = PRIVATE_KEY
        self.keypair['public'] = PUBLIC_KEY

    def pass_keypair_to_remote(self):
        results = map(lambda ip: self._pass_keypair(ip, self.keypair['private']),
                      self.host_ip_list)

        if not (len(results) == len(self.host_ip_list) and False not in results):
            raise RuntimeError("Failed on passing keypair to remote.")

    @staticmethod
    def _pass_keypair(ip, private_key):
        try:
            os.system('ssh-keyscan %s >> /root/.ssh/known_hosts' % ip)
            time.sleep(2)
            ssh_cmd = '%s/qtip_creds.sh %s %s' % (SCRIPT_DIR, ip, private_key)
            os.system(ssh_cmd)
            logger.info('Pass keypair to remote hosts {0} successfully'.format(ip))
            return True
        except Exception as error:
            logger.error(error)
            return False

    def check_hostfile(self, hostfile):
        if all_files_exist(hostfile):
            self.hostfile = hostfile
        else:
            raise RuntimeError(
                "The hostfile {0} is invalid or not existed.".format(hostfile))

    def generate_default_hostfile(self):
        try:
            # check whether the file is already existed
            self.check_hostfile(HOST_FILE)
        except Exception:
            logger.info("Generate default hostfile {0} under "
                        "{1}".format(HOST_FILE, os.environ['HOME']))
            self._generate_hostfile_via_installer()

    def _generate_hostfile_via_installer(self):
        self.hostfile = None

        installer_type = str(os.environ['INSTALLER_TYPE'].lower())
        installer_ip = str(os.environ['INSTALLER_IP'])

        if installer_type not in ["fuel"]:
            raise ValueError("{0} is not supported".format(installer_type))
        if not installer_ip:
            raise ValueError(
                "The value of environment variable INSTALLER_IP is empty.")

        cmd = "bash %s/generate_host_file.sh -t %s -i %s -d %s" % \
              (SCRIPT_DIR, installer_type, installer_ip, HOST_FILE)
        os.system(cmd)

        self.hostfile = HOST_FILE

    def fetch_host_ip_from_hostfile(self):
        self.host_ip_list = []
        logger.info('Fetch host ips from hostfile...')
        with open(self.hostfile, 'r') as f:
            self.host_ip_list = re.findall('\d+.\d+.\d+.\d+', f.read())
        if self.host_ip_list:
            logger.info("The remote compute nodes: {0}".format(self.host_ip_list))
        else:
            raise ValueError("The hostfile doesn't include host ip addresses.")

    def check_hosts_ssh_connectivity(self):
        results = map(lambda ip: self._ssh_is_ok(ip, self.keypair['private']),
                      self.host_ip_list)
        if not (len(results) == len(self.host_ip_list) and False not in results):
            raise RuntimeError("Failed on checking hosts ssh connectivity.")

    @staticmethod
    def _ssh_is_ok(ip, private_key, attempts=100):
        logger.info('Check hosts {0} ssh connectivity...'.format(ip))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, key_filename=private_key)

        for attempt in range(attempts):
            try:
                stdin, stdout, stderr = ssh.exec_command('uname')
                if not stderr.readlines():
                    logger.info("{0}: SSH test successful.".format(ip))
                    return True
            except socket.error:
                logger.debug("%s times ssh test......failed." % str(attempt + 1))
                if attempt == (attempts - 1):
                    return False
                time.sleep(2)
        return False

    def cleanup(self):
        CI_DEBUG = os.getenv('CI_DEBUG')

        if CI_DEBUG is not None and CI_DEBUG.lower() == 'true':
            logger.info("DEBUG Mode: please do cleanup by manual.")
        else:
            for ip in self.host_ip_list:
                logger.info("Cleanup authorized_keys from {0}...".format(ip))
                cmd = 'bash {0}/cleanup_creds.sh {1} {2}'.format(
                    SCRIPT_DIR, ip, self.keypair['private'])
                os.system(cmd)

            logger.info("Cleanup hostfile and keypair.")
            clean_file(self.hostfile,
                       self.keypair['private'],
                       self.keypair['public'])
