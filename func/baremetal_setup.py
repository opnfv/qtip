##############################################################################
# Copyright (c) 2016 ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
from os.path import expanduser
import random
import logging
from func.env_setup import Env_setup

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class Baremetal(Env_setup):

    def __init__(self, args):
        super(Baremetal, self).__init__(args)
        self.get_host_machine_info(self.args['Context']['Host_Machines'])

    def setup(self):
        print "baremetal test setup"
        for ip, pw in self.ip_pw_list:
            cmd = './data/qtip_creds.sh %s' % ip
            print "run command: %s " % cmd
            os.system(cmd)

    def cleanup(self):
        print "baremetal test cleanup"

    @staticmethod
    def fetch_compute_ips():
        LOG.info("Fetch compute ips through installer")
        ips = []

        installer_type = str(os.environ['INSTALLER_TYPE'].lower())
        installer_ip = str(os.environ['INSTALLER_IP'])
        if installer_type not in ["fuel", "compass"]:
            raise RuntimeError("%s is not supported" % installer_type)
        if not installer_ip:
            raise RuntimeError("undefine environment variable INSTALLER_IP")

        cmd = "bash ./data/fetch_compute_ips.sh -i %s -a %s" % \
            (installer_type, installer_ip)
        LOG.info(cmd)
        os.system(cmd)
        home = expanduser("~")
        with open(home + "/ips.log", "r") as file:
            data = file.read()
        if data:
            ips.extend(data.rstrip('\n').split('\n'))
        LOG.info("All compute ips: %s" % ips)
        return ips

    def check_machine_ips(self, host_tag):
        LOG.info("Check machine ips")
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
                    LOG.info(info)
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
        for k, v in self.roles_ip_list:
            self.roles_dict[k].append(v)
        for k, v in self.ip_pw_list:
            self.ip_pw_dict[k].append(v)

    def update_ansible(self):
        f_name_2 = open('./data/hosts', 'w')
        for k in self.roles_dict:
            f_name_2.write('[' + k + ']\n')
            for item in self.roles_dict[k]:
                f_name_2.write(item + '\n')
        f_name_2.close()
