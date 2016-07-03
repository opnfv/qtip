##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import sys
from collections import defaultdict
import yaml
import time
import paramiko
import socket


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
        f_name_2 = open('./data/hosts', 'w')
        print role.items()
        for k in role:
            f_name_2.write('[' + k + ']\n')
            num = len(role[k])
            for x in range(num):
                f_name_2.write(role[k][x] + '\n')
        f_name_2.close()

    @staticmethod
    def ssh_test(lister):
        print 'list: ', lister
        for k, v in lister:
            ip_var = k
            print '\nBeginning SSH Test!\n'
            if v != '':
                print ('\nSSH->>>>> {0} {1}\n'.format(k, v))
                time.sleep(2)

                ssh_c = 'ssh-keyscan {0} >> ~/.ssh/known_hosts'.format(k)
                os.system(ssh_c)
                ssh_cmd = './data/qtip_creds.sh  {0}'.format(ip_var)
                print ssh_cmd
                os.system(ssh_cmd)
                for infinity in range(100):
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(k, key_filename='./data/QtipKey')
                        stdin, stdout, stderr = ssh.exec_command('ls')
                        print('SSH successful')
                        for line in stdout:
                            print '... ' + line.strip('\n')
                        break
                    except socket.error:
                        print 'Retrying aSSH %s' % infinity
                        time.sleep(1)
            if v == '':
                print ('SSH->>>>>', k)
                ssh_c = 'ssh-keyscan {0} >> ~/.ssh/known_hosts'.format(k)

                time.sleep(3)
                os.system(ssh_c)

                for infinity in range(10):
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(k, key_filename='./data/QtipKey')
                        stdin, stdout, stderr = ssh.exec_command('ls')
                        print('SSH successful')
                        for line in stdout:
                            print '... ' + line.strip('\n')
                        break
                    except socket.error:
                        print 'Retrying SSH %s' % infinity

    @staticmethod
    def ping_test(lister):

        for k, v in lister.iteritems():
            time.sleep(10)
            for val in v:
                ipvar = val
                ping_cmd = 'ping -D -c1 {0}'.format(ipvar)
                while os.system(ping_cmd) != 0:
                    print '\nWaiting for machine\n'
                    time.sleep(10)
                print ('\n\n %s is UP \n\n ' % ipvar)

    def get_host_machine_info(self, host_tag):

        num = len(host_tag)
        offset = len(self.roles_ip_list)
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
            doc = yaml.load(f_name)
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
