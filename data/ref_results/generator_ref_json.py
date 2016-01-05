import os
import json

dict_ref={};
dict_ref['compute']={};
dict_ref['compute']['dpi']=8.12
dict_ref['compute']['whetstone']=859.1
dict_ref['compute']['dhrystone']=3146.66
dict_ref['compute']['ssl']={};
dict_ref['compute']['ssl']['RSA']={};
dict_ref['compute']['ssl']['AES']={};
dict_ref['compute']['ssl']['RSA']['512b']=22148.9
dict_ref['compute']['ssl']['RSA']['1024b']=7931.44
dict_ref['compute']['ssl']['RSA']['2048b']=1544.3
dict_ref['compute']['ssl']['RSA']['4096b']=161.92

dict_ref['compute']['ssl']['AES']['16B']=735490250
dict_ref['compute']['ssl']['AES']['64B']=788429210
dict_ref['compute']['ssl']['AES']['256B']=803323650
dict_ref['compute']['ssl']['AES']['1024B']=808861020
dict_ref['compute']['ssl']['AES']['8192B']=807701160


dict_ref['storage']={};
dict_ref['storage']['read']={};
dict_ref['storage']['write']={};
dict_ref['storage']['read']['IOPS']= 6995
dict_ref['storage']['write']['IOPS']= 6990

dict_ref['network']={};
dict_ref['network']['iperf']={};
dict_ref['network']['iperf']['throughput received(b/s)']=9973180000.0

with open('reference.json', 'w+') as result_json:
    json.dump(dict_ref, result_json, indent=4, sort_keys=True)

