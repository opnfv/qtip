##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import pickle
import json
import sys

os.system('inxi -b -c0 -n > $PWD/est_2')
est_ob = open("est_2", "r+")
est_ob2 = open("est_1", "w+")
in_string = est_ob.read().replace('\n', ' ')
cpu_idle = float(os.popen("""top -bn1 | grep "Cpu(s)" | awk '{print $8}'""").read().rstrip())
cpu_usage = 100 - cpu_idle
est_ob2.write(in_string)
est_ob.close()
est_ob2.close()

inxi_host = os.popen("""cat $PWD/est_1 | grep -o -P '(?<=Host:).*(?=Kernel)' """).read().lstrip().rstrip()
inxi_mem = os.popen("""cat $PWD/est_1 | grep -o -P '(?<=Memory:).*(?=MB)' """).read().lstrip().rstrip() + "MB"
inxi_cpu = os.popen("""cat $PWD/est_1 | grep -o -P '(?<=CPU).*(?=speed)' | cut -f2 -d':'""").read().lstrip().rstrip()
inxi_distro = os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Distro:).*(?=Machine:)' """).read().rstrip().lstrip()
inxi_kernel = os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Kernel:).*(?=Console:)' """).read().rstrip().lstrip()
inxi_HD = os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=HDD Total Size:).*(?=Info:)' """).read().rstrip().lstrip()
inxi_product = os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=product:).*(?=Mobo:)' """).read().rstrip().lstrip()

info_dict = {'hostname': inxi_host,
             'product': inxi_product,
             'os': inxi_distro,
             'kernel': inxi_kernel,
             'cpu': inxi_cpu,
             'cpu_usage': '{0}%'.format(str(round(cpu_usage, 3))),
             'memory_usage': inxi_mem,
             'disk_usage': inxi_HD}
network_flag = str(sys.argv[1]).rstrip()

if (network_flag == 'n'):

    info_dict['network_interfaces'] = {}
    tem_2 = """ cat $PWD/est_1 | grep -o -P '(?<=Network:).*(?=Info:)'"""
    print os.system(tem_2 + ' > Hello')
    i = int(os.popen(tem_2 + " | grep -o 'Card' | wc -l ").read())
    print i

    for x in range(1, i + 1):
            tem = """ cat $PWD/est_1 | grep -o -P '(?<=Card-""" + str(x) + """:).*(?=Card-""" + str(x + 1) + """)'"""
            if i == 1:
                tem = """ cat $PWD/est_1 | grep -o -P '(?<=Network:).*(?=Info:)'"""
                inxi_card_1 = ((os.popen(tem + " | grep -o -P '(?<=Card:).*(?=Drives:)'|sed 's/ *driver:.*//'").read().rstrip().lstrip()))
                print inxi_card_1
                info_dict['network_interfaces']['interface_' + str(x)] = {}
                info_dict['network_interfaces']['interface_' + str(x)]['network_card'] = inxi_card_1
                inxi_card_2 = ((os.popen(tem + "| grep -o -P '(?<=Card:).*(?=Drives:)'|sed -e 's/^.*IF: //'").read())).rstrip().lstrip()
                info_dict['network_interfaces']['interface_' + str(x)]['interface_info'] = inxi_card_2
            elif x < (i):
                print "two"
                inxi_card_1 = ((os.popen(tem + "| sed 's/ *driver:.*//'").read().rstrip().lstrip()))
                info_dict['network_interfaces']['interface_' + str(x)] = {}
                info_dict['network_interfaces']['interface_' + str(x)]['network_Card'] = inxi_card_1
                inxi_card_2 = ((os.popen(tem + "|sed -e 's/^.*IF: //'").read())).rstrip().lstrip()
                info_dict['network_interfaces']['interface_' + str(x)]['interface_info'] = inxi_card_2
            elif x == i:
                print "Three"
                info_dict['network_interfaces']['interface_' + str(x)] = {}
                inxi_card_1 = ((os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Card-""" + str(x) + """:).*(?=Drives:)'| sed 's/ *driver:.*//' """).read().rstrip().lstrip()))
                info_dict['network_interfaces']['interface_' + str(x)]['network_Card'] = inxi_card_1
                inxi_card_2 = ((os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Card-""" + str(x) + """:).*(?=Drives:)'| sed -e 's/^.*IF: //' """).read().rstrip().lstrip()))
                info_dict['network_interfaces']['interface_' + str(x)]['interface_info'] = inxi_card_2
            else:
                print "No network cards"
    os.system("bwm-ng -o plain -c 1 | grep -v '=' | grep -v 'iface' | grep -v '-'   > bwm_dump")
    n_interface = int(os.popen(" cat bwm_dump | grep -v 'total' |  wc -l ").read().rstrip())
    interface = {}
    for x in range(1, n_interface):
        interface_name = os.popen(" cat bwm_dump | awk 'NR==" + str(x) + "' | awk '{print $1}' ").read().rstrip().replace(':', '')
        interface[str(interface_name)] = {}
        interface[str(interface_name)]['Rx (KB/s)'] = os.popen(" cat bwm_dump | awk 'NR==" + str(x) + "' | awk '{print $2}' ").read().rstrip()
        interface[str(interface_name)]['Tx (KB/s)'] = os.popen(" cat bwm_dump | awk 'NR==" + str(x) + "' | awk '{print $4}' ").read().rstrip()
        interface[str(interface_name)]['Total (KB/s)'] = os.popen(" cat bwm_dump | awk 'NR== " + str(x) + "' | awk '{print $6}' ").read().rstrip()

    info_dict['interface_io'] = interface

print info_dict

with open('./sys_info_temp', 'w+')as out_info:
    pickle.dump(info_dict, out_info)

with open('temp', 'w+') as result_json:
    json.dump(info_dict, result_json, indent=4, sort_keys=True)
