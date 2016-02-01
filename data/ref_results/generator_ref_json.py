import os
import json

dict_ref={};
dict_ref['compute']={};
dict_ref['compute']['dpi_bm']=8.12
dict_ref['compute']['dpi_vm']=22.12

dict_ref['compute']['whetstone_bm']={};
dict_ref['compute']['whetstone_vm']={};
dict_ref['compute']['whetstone_bm']['single_cpu']=859.1
dict_ref['compute']['whetstone_bm']['multi_cpu']=859.1
dict_ref['compute']['whetstone_vm']['single_cpu']=859.1
dict_ref['compute']['whetstone_vm']['multi_cpu']=859.

dict_ref['compute']['dhrystone_bm']={};
dict_ref['compute']['dhrystone_vm']={};
dict_ref['compute']['dhrystone_bm']['single_cpu']=3231.7
dict_ref['compute']['dhrystone_bm']['multi_cpu']=103362.1
dict_ref['compute']['dhrystone_vm']['single_cpu']=2953.6
dict_ref['compute']['dhrystone_vm']['multi_cpu']=10585.8

dict_ref['compute']['ssl_bm']={};
dict_ref['compute']['ssl_bm']['RSA']={};
dict_ref['compute']['ssl_bm']['AES']={};
dict_ref['compute']['ssl_bm']['RSA']['512b']=22148.9
dict_ref['compute']['ssl_bm']['RSA']['1024b']=7931.44
dict_ref['compute']['ssl_bm']['RSA']['2048b']=1544.3
dict_ref['compute']['ssl_bm']['RSA']['4096b']=161.92
dict_ref['compute']['ssl_bm']['AES']['16B']=735490250
dict_ref['compute']['ssl_bm']['AES']['64B']=788429210
dict_ref['compute']['ssl_bm']['AES']['256B']=803323650
dict_ref['compute']['ssl_bm']['AES']['1024B']=808861020
dict_ref['compute']['ssl_bm']['AES']['8192B']=807701160

dict_ref['compute']['ssl_vm']={};
dict_ref['compute']['ssl_vm']['RSA']={};
dict_ref['compute']['ssl_vm']['AES']={};
dict_ref['compute']['ssl_vm']['RSA']['512b']=22148.9
dict_ref['compute']['ssl_vm']['RSA']['1024b']=7931.44
dict_ref['compute']['ssl_vm']['RSA']['2048b']=1544.3
dict_ref['compute']['ssl_vm']['RSA']['4096b']=161.92
dict_ref['compute']['ssl_vm']['AES']['16B']=735490250
dict_ref['compute']['ssl_vm']['AES']['64B']=788429210
dict_ref['compute']['ssl_vm']['AES']['256B']=803323650
dict_ref['compute']['ssl_vm']['AES']['1024B']=808861020
dict_ref['compute']['ssl_vm']['AES']['8192B']=807701160


dict_ref['compute']['ramspeed_bm']={};
dict_ref['compute']['ramspeed_bm']['INTmem']={};
dict_ref['compute']['ramspeed_bm']['FLOATmem']={};
dict_ref['compute']['ramspeed_bm']['INTmem']['Average (MB/s)']=11775.85
dict_ref['compute']['ramspeed_bm']['FLOATmem']['Average (MB/s)']=9780.23

dict_ref['compute']['ramspeed_vm']={};
dict_ref['compute']['ramspeed_vm']['INTmem']={};
dict_ref['compute']['ramspeed_vm']['FLOATmem']={};
dict_ref['compute']['ramspeed_vm']['INTmem']['Average (MB/s)']=11775.85
dict_ref['compute']['ramspeed_vm']['FLOATmem']['Average (MB/s)']=9780.23


dict_ref['storage']={};
dict_ref['storage']['fio_bm']={};
dict_ref['storage']['fio_bm']['read']={};
dict_ref['storage']['fio_bm']['write']={};
dict_ref['storage']['fio_bm']['read']['IOPS']=6693
dict_ref['storage']['fio_bm']['write']['IOPS']=6688

dict_ref['storage']['fio_vm']={};
dict_ref['storage']['fio_vm']['read']={};
dict_ref['storage']['fio_vm']['write']={};
dict_ref['storage']['fio_vm']['read']['IOPS']=2239
dict_ref['storage']['fio_vm']['write']['IOPS']=2237

dict_ref['network']={};
dict_ref['network']['iperf_bm']={};
dict_ref['network']['iperf_vm']={};
dict_ref['network']['iperf_vm_2']={};
dict_ref['network']['iperf_bm']['throughput received(b/s)']=944473000.0
dict_ref['network']['iperf_vm']['throughput received(b/s)']=14416700000.0
dict_ref['network']['iperf_vm_2']['throughput received(b/s)']=2461530000.0
with open('reference.json', 'w+') as result_json:
    json.dump(dict_ref, result_json, indent=4, sort_keys=True)

