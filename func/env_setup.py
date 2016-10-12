##############################################################################
# Copyright (c) 2016 Dell Inc, ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import random
import socket
import sys
import time
from collections import defaultdict
from os.path import expanduser
import paramiko
import yaml
from utils import logger_utils

logger = logger_utils.QtipLogger('env_setup').get


class Env_setup:

    roles_ip_list = []  # ROLE and its corresponding IP address list
    ip_pw_list = []  # IP and password, this will be used to ssh
    roles_dict = defaultdict(list)
    ip_pw_dict = defaultdict(list)
    ip_pip_list = []
    vm_parameters = defaultdict(list)
    benchmark_details = defaultdict()
    benchmark = ''

    def __init__(self):
        print '\nParsing class initiated\n'
        self.roles_ip_list[:] = []
        self.ip_pw_list[:] = []
        self.roles_dict.clear()
        self.ip_pw_dict.clear()
        self.ip_pip_list[:] = []
        self.proxy_info = {}
        self.vm_parameters.clear()
        self.benchmark_details.clear()
        self.benchmark = ''

    @staticmethod
    def write_to_file(role):
        f_name_2 = open('./config/hosts', 'w')
        print role.items()
        for k in role:
            f_name_2.write('[' + k + ']\n')
            num = len(role[k])
            for x in range(num):
                f_name_2.write(role[k][x] + '\n')
        f_name_2.close()

    @staticmethod
    def ssh_test(hosts):
        for ip, pw in hosts:
            print '\nBeginning SSH Test: %s \n' % ip
            os.system('ssh-keyscan %s >> ~/.ssh/known_hosts' % ip)
            time.sleep(2)

            ssh_cmd = './scripts/qtip_creds.sh %s' % ip
            print "run command: %s " % ssh_cmd
            os.system(ssh_cmd)

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, key_filename='./config/QtipKey')


            for attempts in range(100):
                try:
                    stdin, stdout, stderr = ssh.exec_command('uname')
                    if not stderr.readlines():
                        print('SSH successful')
                        break
                except socket.error:
                    print 'SSH is still unavailable, retry!'
                    time.sleep(2)
                    if attempts == 99:
                        print "Try 99 times, SSH failed: %s" % ip

    @staticmethod
    def ping_test(lister, attempts=30):
        for k, v in lister.iteritems():
            time.sleep(10)
            for val in v:
                ipvar = val
                ping_cmd = 'ping -D -c1 {0}'.format(ipvar)
                for i in range(attempts):
                    if os.system(ping_cmd) != 0:
                        print '\nWaiting for machine\n'
                        time.sleep(10)
                    else:
                        break
                print ('\n\n %s is UP \n\n ' % ipvar)

    @staticmethod
    def fetch_compute_ips():
        logger.info("Fetch compute ips through installer")
        ips = []

        installer_type = str(os.environ['INSTALLER_TYPE'].lower())
        installer_ip = str(os.environ['INSTALLER_IP'])
        if installer_type not in ["fuel", "compass"]:
            raise RuntimeError("%s is not supported" % installer_type)
        if not installer_ip:
            raise RuntimeError("undefine environment variable INSTALLER_IP")

        cmd = "bash ./scripts/fetch_compute_ips.sh -i %s -a %s" % \
            (installer_type, installer_ip)
        logger.info(cmd)
        os.system(cmd)
        home = expanduser("~")
        with open(home + "/ips.log", "r") as file:
            data = file.read()
        if data:
            ips.extend(data.rstrip('\n').split('\n'))
        logger.info("All compute ips: %s" % ips)
        return ips

    def check_machine_ips(self, host_tag):
        logger.info("Check machine ips")
        ips = self.fetch_compute_ips()
        ips_num = len(ips)
        num = len(host_tag)
        if num > ips_num:
            err = "host num %s > compute ips num %s" % (num, ips_num)
            raise RuntimeError(err)

        for x in range(num):
            hostlabel = 'machine_' + str(x + 1)
            if host_tag[hostlabel]['ip']:
                if host_tag[hostlabel]['ip'] in ips:
                    info = "%s's ip %s is defined by test case yaml file" % \
                        (hostlabel, host_tag[hostlabel]['ip'])
                    logger.info(info)
                else:
                    err = "%s is not in %s" % (host_tag[hostlabel]['ip'], ips)
                    raise RuntimeError(err)
            else:
                host_tag[hostlabel]['ip'] = random.choice(ips)
                info = "assign ip %s to %s" % (host_tag[hostlabel]['ip'], hostlabel)
            ips.remove(host_tag[hostlabel]['ip'])

    def get_host_machine_info(self, host_tag):
        num = len(host_tag)
        offset = len(self.roles_ip_list)
        self.check_machine_ips(host_tag)
        for x in range(num):
            hostlabel = 'machine_' + str(x + 1)
            self.roles_ip_list.insert(
                offset, (host_tag[hostlabel]['role'], host_tag[hostlabel]['ip']))
            self.ip_pw_list.insert(
                offset, (host_tag[hostlabel]['ip'], host_tag[hostlabel]['pw']))

    def get_virtual_machine_info(self, virtual_tag):

        num = len(virtual_tag)
        for x in range(num):
            host_label = 'virtualmachine_' + str(x + 1)
            for k, v in virtual_tag[host_label].iteritems():
                self.vm_parameters[k].append(v)

    def get_bench_mark_details(self, detail_dic):

        print detail_dic
        for k, v in detail_dic.items():
            self.benchmark_details[k] = v

    def parse(self, config_file_path):
        try:
            f_name = open(config_file_path, 'r+')
            doc = yaml.safe_load(f_name)
            f_name.close()
            if doc['Scenario']['benchmark']:
                self.benchmark = doc['Scenario']['benchmark']
            if doc['Context']['Virtual_Machines']:
                self.get_virtual_machine_info(doc['Context']['Virtual_Machines'])
            if doc['Context']['Host_Machines']:
                self.get_host_machine_info(doc['Context']['Host_Machines'])
            if doc.get('Scenario', {}).get('benchmark_details', {}):
                self.get_bench_mark_details(doc.get('Scenario', {}).get('benchmark_details', {}))
            if 'Proxy_Environment' in doc['Context'].keys():
                self.proxy_info['http_proxy'] = doc['Context']['Proxy_Environment']['http_proxy']
                self.proxy_info['https_proxy'] = doc['Context']['Proxy_Environment']['https_proxy']
                self.proxy_info['no_proxy'] = doc['Context']['Proxy_Environment']['no_proxy']
            for k, v in self.roles_ip_list:
                self.roles_dict[k].append(v)
            for k, v in self.ip_pw_list:
                self.ip_pw_dict[k].append(v)
            return (
                self.benchmark,
                self.vm_parameters,
                self.benchmark_details.items(),
                self.proxy_info)
        except KeyboardInterrupt:
            print 'ConfigFile Closed: exiting!'
            sys.exit(0)

    def update_ansible(self):
        self.write_to_file(self.roles_dict)

    def call_ping_test(self):
        self.ping_test(self.roles_dict)

    def call_ssh_test(self):
        self.ssh_test(self.ip_pw_list)
