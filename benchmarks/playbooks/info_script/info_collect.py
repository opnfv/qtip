import os
import pickle
import time
import datetime
import json
<<<<<<< HEAD
import sys

os.system('inxi -b -c0 -n > $PWD/est_2')
est_ob=open("est_2","r+")
est_ob2=open("est_1","w+")
in_string= est_ob.read().replace('\n',' ')
cpu_idle=float(os.popen("""top -bn1 | grep "Cpu(s)" | awk '{print $8}'""").read().rstrip())
cpu_usage= 100-cpu_idle
est_ob2.write(in_string);
est_ob.close()
est_ob2.close()

Info_dict={};
inxi_host=os.popen("""cat $PWD/est_1 | grep -o -P '(?<=Host:).*(?=Kernel)' """).read().lstrip().rstrip()
inxi_mem=os.popen("""cat $PWD/est_1 | grep -o -P '(?<=Memory:).*(?=Init)' """).read().lstrip().rstrip()
inxi_cpu=os.popen("""cat $PWD/est_1 | grep -o -P '(?<=CPU).*(?=speed)' | cut -f2 -d':'""").read().lstrip().rstrip()
inxi_distro=os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Distro:).*(?=Machine:)' """).read().rstrip().lstrip()
inxi_kernel=os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Kernel:).*(?=Console:)' """).read().rstrip().lstrip()
inxi_HD=os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=HDD Total Size:).*(?=Info:)' """).read().rstrip().lstrip()
inxi_product=os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=product:).*(?=Mobo:)' """).read().rstrip().lstrip()



Info_dict['1_Hostname']=inxi_host
Info_dict['2_Product']=inxi_product
Info_dict['3_OS Distribution']=inxi_distro
Info_dict['4_Kernel']=inxi_kernel
Info_dict['5_CPU']=inxi_cpu
Info_dict['6_CPU_Usage']=str(round(cpu_usage,3))+'%'
Info_dict['7_Memory Usage']=inxi_mem
Info_dict['8_Disk usage']=inxi_HD
network_flag=str(sys.argv[1]).rstrip()

if (network_flag == 'n'):
    
    Info_dict['9_Network_Interfaces']={};
    tem_2=""" cat $PWD/est_1 | grep -o -P '(?<=Network:).*(?=Info:)'"""
    print os.system(tem_2+' > Hello')
    i=int(os.popen(tem_2+" | grep -o 'Card' | wc -l ").read())
    print i


    for x in range (1,i+1):
            tem=""" cat $PWD/est_1 | grep -o -P '(?<=Card-"""+str(x)+""":).*(?=Card-"""+str(x+1)+""")'"""
            if i == 1:
                tem=""" cat $PWD/est_1 | grep -o -P '(?<=Network:).*(?=Info:)'"""
                inxi_card_1=((os.popen(tem+" | grep -o -P '(?<=Card:).*(?=Drives:)'|sed 's/ *driver:.*//'").read().rstrip().lstrip()))
                print inxi_card_1
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]={};
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]['1_Network_Card']=inxi_card_1
                inxi_card_2=((os.popen(tem+"| grep -o -P '(?<=Card:).*(?=Drives:)'|sed -e 's/^.*IF: //'").read())).rstrip().lstrip()
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]['2_Interface_info']=inxi_card_2
            elif x < (i):
                print "two"
                #inxi_Card_temp=((os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Card-"""+str(x)+""":).*(?=Card-"""+str(x+1)+""")' """).read().rstrip().lstrip()))
                inxi_card_1=((os.popen(tem+"| sed 's/ *driver:.*//'").read().rstrip().lstrip()))
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]={};
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]['1_Network_Card']=inxi_card_1
                inxi_card_2=((os.popen(tem+"|sed -e 's/^.*IF: //'").read())).rstrip().lstrip()
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]['2_Interface_info']=inxi_card_2
            elif x == i:
                print "Three"
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]={};
                inxi_card_1=((os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Card-"""+str(x)+""":).*(?=Drives:)'| sed 's/ *driver:.*//' """).read().rstrip().lstrip()))
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]['1_Network_Card']=inxi_card_1
                inxi_card_2=((os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Card-"""+str(x)+""":).*(?=Drives:)'| sed -e 's/^.*IF: //' """).read().rstrip().lstrip()))
                Info_dict['9_Network_Interfaces']['Interface_'+str(x)]['2_Interface_info']=inxi_card_2 
            else:
                print "No network cards"
    os.system("bwm-ng -c 1 | grep -v '=' | grep -v 'iface' | grep -v '-'   > bwm_dump")
    n_interface=int(os.popen(" cat bwm_dump | grep -v 'total' |  wc -l ").read().rstrip())
    interface={};
    for x in range (1,n_interface):
        interface_name=os.popen(" cat bwm_dump | awk 'NR=="+str(x)+"' | awk '{print $1}' ").read().rstrip().replace(':','')
        interface[str(interface_name)]={};
        interface[str(interface_name)]['Rx (KB/s)']=os.popen(" cat bwm_dump | awk 'NR=="+str(x)+"' | awk '{print $2}' ").read().rstrip()
        interface[str(interface_name)]['Tx (KB/s)']=os.popen(" cat bwm_dump | awk 'NR=="+str(x)+"' | awk '{print $4}' ").read().rstrip()
        interface[str(interface_name)]['Total (KB/s)']=os.popen(" cat bwm_dump | awk 'NR== "+str(x)+"' | awk '{print $6}' ").read().rstrip()
 
    Info_dict['Interface I/O']=interface

print Info_dict
    
with open('./sys_info_temp','w+')as out_info:
    pickle.dump(Info_dict,out_info)

with open('temp','w+') as result_json:
    json.dump(Info_dict,result_json,indent=4,sort_keys=True)

=======

os.system('inxi -b -c0 -n > $PWD/est_2')
est_ob = open("est_2", "r+")
est_ob2 = open("est_1", "w+")
in_string = est_ob.read().replace('\n', ' ')

est_ob2.write(in_string)
est_ob.close()
est_ob2.close()

Info_dict = {}
inxi_host = os.popen(
    """cat $PWD/est_1 | grep -o -P '(?<=Host:).*(?=Kernel)' """).read().lstrip().rstrip()
inxi_mem = os.popen(
    """inxi -c0 | grep -o -P '(?<=Mem~).*(?=HDD)' """).read().lstrip().rstrip()
inxi_cpu = os.popen(
    """cat $PWD/est_1 | grep -o -P '(?<=CPU).*(?=speed)' | cut -f2 -d':'""").read().lstrip().rstrip()
#inxi_Speed=os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=max:).*(?=Graphics)' """).read().rstrip().lstrip()
inxi_distro = os.popen(
    """ cat $PWD/est_1 | grep -o -P '(?<=Distro:).*(?=Machine:)' """).read().rstrip().lstrip()
inxi_kernel = os.popen(
    """ cat $PWD/est_1 | grep -o -P '(?<=Kernel:).*(?=Console:)' """).read().rstrip().lstrip()
inxi_HD = os.popen(
    """ cat $PWD/est_1 | grep -o -P '(?<=HDD Total Size:).*(?=Info:)' """).read().rstrip().lstrip()
#inxi_system=os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Machine    System:).*(?=product:)' """).read().rstrip().lstrip()
inxi_product = os.popen(
    """ cat $PWD/est_1 | grep -o -P '(?<=product:).*(?=Mobo:)' """).read().rstrip().lstrip()
# print inxi_system


Info_dict['1_Hostname'] = inxi_host
Info_dict['2_Product'] = inxi_product
Info_dict['3_OS Distribution'] = inxi_distro
Info_dict['4_Kernel'] = inxi_kernel
Info_dict['5_CPU'] = inxi_cpu
Info_dict['6_Memory Usage'] = inxi_mem
Info_dict['7_Disk usage'] = inxi_HD
Info_dict['8_Network_Interfaces'] = {}

tem_2 = """ cat $PWD/est_1 | grep -o -P '(?<=Network:).*(?=Info:)'"""
print os.system(tem_2 + ' > Hello')
i = int(os.popen(tem_2 + " | grep -o 'Card' | wc -l ").read())
print i


for x in range(1, i + 1):
    tem = """ cat $PWD/est_1 | grep -o -P '(?<=Card-""" + str(
        x) + """:).*(?=Card-""" + str(x + 1) + """)'"""
    if i == 1:
        tem = """ cat $PWD/est_1 | grep -o -P '(?<=Network:).*(?=Info:)'"""
        inxi_card_1 = (
            (os.popen(
                tem +
                " | grep -o -P '(?<=Card:).*(?=Drives:)'|sed 's/ *driver:.*//'").read().rstrip().lstrip()))
        print inxi_card_1
        Info_dict['8_Network_Interfaces']['Interface_' + str(x)] = {}
        Info_dict['8_Network_Interfaces'][
            'Interface_' + str(x)]['1_Network_Card'] = inxi_card_1
        inxi_card_2 = (
            (os.popen(
                tem +
                "| grep -o -P '(?<=Card:).*(?=Drives:)'|sed -e 's/^.*IF: //'").read())).rstrip().lstrip()
        Info_dict['8_Network_Interfaces'][
            'Interface_' + str(x)]['2_Interface_info'] = inxi_card_2
    elif x < (i):
        print "two"
        #inxi_Card_temp=((os.popen(""" cat $PWD/est_1 | grep -o -P '(?<=Card-"""+str(x)+""":).*(?=Card-"""+str(x+1)+""")' """).read().rstrip().lstrip()))
        inxi_card_1 = (
            (os.popen(tem + "| sed 's/ *driver:.*//'").read().rstrip().lstrip()))
        Info_dict['8_Network_Interfaces']['Interface_' + str(x)] = {}
        Info_dict['8_Network_Interfaces'][
            'Interface_' + str(x)]['1_Network_Card'] = inxi_card_1
        inxi_card_2 = (
            (os.popen(tem + "|sed -e 's/^.*IF: //'").read())).rstrip().lstrip()
        Info_dict['8_Network_Interfaces'][
            'Interface_' + str(x)]['2_Interface_info'] = inxi_card_2
    elif x == i:
        print "Three"
        Info_dict['8_Network_Interfaces']['Interface_' + str(x)] = {}
        inxi_card_1 = (
            (os.popen(
                """ cat $PWD/est_1 | grep -o -P '(?<=Card-""" +
                str(x) +
                """:).*(?=Drives:)'| sed 's/ *driver:.*//' """).read().rstrip().lstrip()))
        Info_dict['8_Network_Interfaces'][
            'Interface_' + str(x)]['1_Network_Card'] = inxi_card_1
        inxi_card_2 = (
            (os.popen(
                """ cat $PWD/est_1 | grep -o -P '(?<=Card-""" +
                str(x) +
                """:).*(?=Drives:)'| sed -e 's/^.*IF: //' """).read().rstrip().lstrip()))
        Info_dict['8_Network_Interfaces'][
            'Interface_' + str(x)]['2_Interface_info'] = inxi_card_2
    else:
        print "No network cards"
print Info_dict
home_dir = str(os.popen("echo $HOME").read().rstrip())
with open('./sys_info_temp', 'w+')as out_info:
    pickle.dump(Info_dict, out_info)

#	 json.dump(Info_dict, out_json, sort_keys=True,separators=(',',':'),indent=4)
>>>>>>> 5a7dcc0... Networking testcases for QTIP Framework
