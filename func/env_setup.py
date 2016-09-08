##############################################################################
# Copyright (c) 2016 Dell Inc, ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
from collections import defaultdict
import time
import paramiko
import socket
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class Env_setup(object):
    def __init__(self, args):
        self.roles_ip_list = []
        self.ip_pw_list = []
        self.roles_dict = defaultdict(list)
        self.ip_pw_dict = defaultdict(list)
        self.proxy_info = {}
        self.benchmark_details = defaultdict()
        self.benchmark = ''
        self.args = args.copy()

    def handler_args(self):
        if self.args['Scenario']['benchmark']:
            self.benchmark = self.args['Scenario']['benchmark']
        if self.args.get('Scenario', {}).get('benchmark_details', {}):
            self.get_bench_mark_details(self.args.get('Scenario', {}).get('benchmark_details', {}))
        if 'Proxy_Environment' in self.args['Context'].keys():
            self.proxy_info['http_proxy'] = self.args['Context']['Proxy_Environment']['http_proxy']
            self.proxy_info['https_proxy'] = self.args['Context']['Proxy_Environment']['https_proxy']
            self.proxy_info['no_proxy'] = self.args['Context']['Proxy_Environment']['no_proxy']
        return (
            self.benchmark,
            self.benchmark_details.items(),
            self.proxy_info)

    def get_bench_mark_details(self, detail_dic):
        print "detail_dic: %s" % detail_dic
        for k, v in detail_dic.items():
            self.benchmark_details[k] = v

    @staticmethod
    def ssh_test(host):
        for ip, pw in host:
            print '\nBeginning SSH Test: %s \n' % ip
            os.system('ssh-keyscan %s >> ~/.ssh/known_hosts' % ip)
            time.sleep(2)

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, key_filename='./data/QtipKey')

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

    def call_ping_test(self):
        self.ping_test(self.roles_dict)

    def call_ssh_test(self):
        self.ssh_test(self.ip_pw_list)
