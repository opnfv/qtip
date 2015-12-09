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

class Env_setup():
    roles_ip_list = []  # ROLE and its corresponding IP address list
    ip_pw_list = []  # IP and password, this will be used to ssh
    roles_dict = defaultdict(list)
    ip_pw_dict = defaultdict(list)
    ip_pip_list = []
    vm_parameters = defaultdict(list)
    benchmark_details= defaultdict()
    benchmark = ''

    def __init__(self):
        print '\nParsing class initiated\n'

    def writeTofile(self, role):
        fname2 = open('/etc/ansible/hosts', 'w')
        print role.items()
        for k in role:
            fname2.write('[' + k + ']\n')
            num = len(role[k])
            for x in range(num):
                fname2.write(role[k][x] + '\n')
        fname2.close

    def sshtest(self, lister):
        print 'list: ',lister
        for k, v in lister:
            ipvar = k
            pwvar = v
            print '\nBeginning SSH Test!\n'
            if v != '':
                print ('\nSSH->>>>> %s\n' % k)
                time.sleep(2)

                ssh_c = 'ssh-keyscan {0} >> ~/.ssh/known_hosts'.format(k)

                os.system(ssh_c)
                ssh_cmd = 'expect ./data/ssh_exch.exp {0} {1}'.format(
                    ipvar, pwvar)
                res = os.system(ssh_cmd)
                '''
                for infinity in range(10000):
                    try :
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname = k , username = 'root', password = v)
                        stdin, stdout, stderr = ssh.exec_command('ls')
                        print('SSH successful')
                        break
                    except:
                        print 'Retrying SSH'
                        time.sleep(1)
                '''
            if v == '':
                print ('SSH->>>>>', k)
                ssh_c = 'ssh-keyscan {0} >> ~/.ssh/known_hosts'.format(k)

                time.sleep(3)
                os.system(ssh_c)
                
                for infinity in range(10000):
                    try :
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname = k )
                        stdin, stdout, stderr = ssh.exec_command('ls')
                        break
                    except:
                        print 'Retrying SSH'
                
    def pingtest(self, lister):
        pingFlag = 0
        
        for k, v in lister.iteritems():
            time.sleep(10)
            for val in v:
                ipvar = val
                ping_cmd = 'ping -D -c1 {0}'.format(ipvar)
                while os.system(ping_cmd) != 0:
                    print '\nWaiting for machine\n'
                    time.sleep(10)
                pingFlag = 0
                print ('\n\n %s is UP \n\n ' % ipvar)

    def GetHostMachineinfo(self, Hosttag):
        num = len(Hosttag)
        offset = len(self.roles_ip_list)

        for x in range(num):
            hostlabel = 'machine_' + str(x + 1)
            self.roles_ip_list.insert(
                offset, (Hosttag[hostlabel]['role'], Hosttag[hostlabel]['ip']))
            self.ip_pw_list.insert(
                offset, (Hosttag[hostlabel]['ip'], Hosttag[hostlabel]['pw']))

    def GetVirtualMachineinfo(self, Virtualtag):
        num = len(Virtualtag)
        for x in range(num):
            hostlabel = 'virtualmachine_' + str(x + 1)
            for k, v in Virtualtag[hostlabel].iteritems():
                self.vm_parameters[k].append(v)

    def GetBenchmarkDetails(self, detail_dic):
        
        print detail_dic
        for k,v in detail_dic.items():
            self.benchmark_details[k]= v

    def parse(self, configfilepath):
        try:
            fname = open(configfilepath, 'r+')
            doc = yaml.load(fname)
#			valid_file = validate_yaml.Validate_Yaml(doc)
            fname.close()
            for scenario in doc:
                self.benchmark = doc['Scenario']['benchmark']
            if doc['Context']['Virtual_Machines']:
                self.GetVirtualMachineinfo(doc['Context']['Virtual_Machines'])
            if doc['Context']['Host_Machines']:
                self.GetHostMachineinfo(doc['Context']['Host_Machines'])
            if doc.get('Scenario',{}).get('benchmark_details',{}):
                self.GetBenchmarkDetails(doc.get('Scenario',{}).get('benchmark_details',{}))
            
            for k, v in self.roles_ip_list:
                self.roles_dict[k].append(v)
            for k, v in self.ip_pw_list:
                self.ip_pw_dict[k].append(v)
            return (
                self.benchmark,
                self.roles_dict.items(),
                self.vm_parameters,
                self.benchmark_details.items(),
                self.ip_pw_dict.items())
        except KeyboardInterrupt:
            fname.close()
            print 'ConfigFile Closed: exiting!'
            sys.exit(0)

    def updateAnsible(self):
        self.writeTofile(self.roles_dict)

    def callpingtest(self):
        self.pingtest(self.roles_dict)

    def callsshtest(self):
        self.sshtest(self.ip_pw_list)
