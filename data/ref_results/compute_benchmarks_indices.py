from index_calculation import generic_index as get_index
from index_calculation import get_reference 
from result_accum import result_concat as concat

def dpi_index ():
    dpi_dict=concat('../../results/dpi/')
    dpi_bm_ref = get_reference('compute','dpi_bm')
    dpi_bm_index= get_index(dpi_dict,'dpi_bm',dpi_bm_ref,'4  DPI result', 'DPI_benchmark(Gb/s)')
    
    dpi_vm_ref = get_reference('compute','dpi_vm')
    dpi_vm_index= get_index(dpi_dict,'dpi_vm',dpi_vm_ref,'4  DPI result', 'DPI_benchmark(Gb/s)')

    dpi_index=(dpi_bm_index+dpi_vm_index)/2
    dpi_dict_i={};
    dpi_dict_i['1. Index']=dpi_index
    dpi_dict_i['2. Results']=dpi_dict
    return dpi_dict_i    

def dhrystone_index():

    dhrystone_dict=concat('../../results/dhrystone/')
    dhrystone_single_bm_ref = get_reference('compute','dhrystone_bm','single_cpu')
    dhrystone_single_bm_index= get_index(dhrystone_dict,'dhrystone_bm',dhrystone_single_bm_ref,'4  Dhrystone result','2.Single CPU test','2.Index score')
    
    dhrystone_multi_bm_ref = get_reference('compute','dhrystone_bm','multi_cpu')
    dhrystone_multi_bm_index= get_index(dhrystone_dict,'dhrystone_bm',dhrystone_multi_bm_ref,'4  Dhrystone result','3.Multi CPU test','2.Index score')
    
    dhrystone_bm_index=(dhrystone_single_bm_index+dhrystone_multi_bm_index)/2
    
    dhrystone_single_vm_ref = get_reference('compute','dhrystone_vm','single_cpu')
    dhrystone_single_vm_index= get_index(dhrystone_dict,'dhrystone_vm',dhrystone_single_vm_ref,'4  Dhrystone result','2.Single CPU test','2.Index score')
    
    dhrystone_multi_vm_ref = get_reference('compute','dhrystone_vm','multi_cpu')
    dhrystone_multi_vm_index= get_index(dhrystone_dict,'dhrystone_vm',dhrystone_multi_vm_ref,'4  Dhrystone result','3.Multi CPU test','2.Index score')
    
    dhrystone_vm_index=(dhrystone_single_vm_index+dhrystone_multi_vm_index)/2
    
    
    dhrystone_index=(dhrystone_bm_index+dhrystone_vm_index)/2
    dhrystone_dict_i={};
    dhrystone_dict_i['1. Index']=dhrystone_index
    dhrystone_dict_i['2. Results']=dhrystone_dict
    return dhrystone_dict_i

def whetstone_index():

    whetstone_dict=concat('../../results/whetstone/')
    whetstone_single_bm_ref = get_reference('compute','whetstone_bm','single_cpu')
    whetstone_single_bm_index= get_index(whetstone_dict,'whetstone_bm',whetstone_single_bm_ref,'4  Whetstone result','2.Single CPU test','2.Index score')
    
    whetstone_multi_bm_ref = get_reference('compute','whetstone_bm','multi_cpu')
    whetstone_multi_bm_index= get_index(whetstone_dict,'whetstone_bm',whetstone_multi_bm_ref,'4  Whetstone result','3.Multi CPU test','2.Index score')
    
    whetstone_bm_index=(whetstone_single_bm_index+whetstone_multi_bm_index)/2
    
    whetstone_single_vm_ref = get_reference('compute','whetstone_vm','single_cpu')
    whetstone_single_vm_index= get_index(whetstone_dict,'whetstone_vm',whetstone_single_vm_ref,'4  Whetstone result','2.Single CPU test','2.Index score')
    
    whetstone_multi_vm_ref = get_reference('compute','whetstone_vm','multi_cpu')
    whetstone_multi_vm_index= get_index(whetstone_dict,'whetstone_vm',whetstone_multi_vm_ref,'4  Whetstone result','3.Multi CPU test','2.Index score')
    
    whetstone_vm_index=(whetstone_single_vm_index+whetstone_multi_vm_index)/2
      
    whetstone_index=(whetstone_bm_index+whetstone_vm_index)/2
    whetstone_dict_i={};
    whetstone_dict_i['1. Index']=whetstone_index
    whetstone_dict_i['2. Results']=whetstone_dict
    return whetstone_dict_i

def ramspeed_index ():

    ramspeed_dict=concat('../../results/ramspeed/')
    ramspeed_int_bm_ref=get_reference('compute','ramspeed_bm','INTmem','Average (MB/s)')
    ramspeed_int_bm_index=get_index(ramspeed_dict, 'ramspeed_bm', ramspeed_int_bm_ref,'4  RamSpeed result','1. INTmem bandwidth','5. Average (MB/s)')
    
    ramspeed_float_bm_ref=get_reference('compute','ramspeed_bm','FLOATmem','Average (MB/s)')
    ramspeed_float_bm_index=get_index(ramspeed_dict, 'ramspeed_bm', ramspeed_float_bm_ref,'4  RamSpeed result','1. FLOATmem bandwidth','5. Average (MB/s)')
    
    ramspeed_bm_index=(ramspeed_int_bm_index+ramspeed_float_bm_index)/2
    
    ramspeed_int_vm_ref=get_reference('compute','ramspeed_vm','INTmem','Average (MB/s)')
    ramspeed_int_vm_index=get_index(ramspeed_dict, 'ramspeed_vm', ramspeed_int_vm_ref,'4  RamSpeed result','1. INTmem bandwidth','5. Average (MB/s)')
    
    ramspeed_float_vm_ref=get_reference('compute','ramspeed_vm','FLOATmem','Average (MB/s)')
    ramspeed_float_vm_index=get_index(ramspeed_dict, 'ramspeed_vm', ramspeed_float_vm_ref,'4  RamSpeed result','1. FLOATmem bandwidth','5. Average (MB/s)')
    
    ramspeed_vm_index=(ramspeed_int_vm_index+ramspeed_float_vm_index)/2
    
    ramspeed_index=(ramspeed_vm_index+ramspeed_bm_index)/2
    
    ramspeed_dict_i={};
    ramspeed_dict_i['1. Index']=ramspeed_index
    ramspeed_dict_i['2. Results']=ramspeed_dict
    return ramspeed_dict_i


def ssl_index ():

    ssl_dict=concat('../../results/ssl/')
    
    ssl_RSA512b_bm_ref=get_reference('compute','ssl_bm','RSA','512b')
    ssl_RSA1024b_bm_ref=get_reference('compute','ssl_bm','RSA','1024b')
    ssl_RSA2048b_bm_ref=get_reference('compute','ssl_bm','RSA','2048b')
    ssl_RSA4096b_bm_ref=get_reference('compute','ssl_bm','RSA','4096b')
    
    
    ssl_AES16B_bm_ref=get_reference('compute','ssl_bm','AES','16B')
    ssl_AES64B_bm_ref=get_reference('compute','ssl_bm','AES','64B')
    ssl_AES256B_bm_ref=get_reference('compute','ssl_bm','AES','256B')
    ssl_AES1024B_bm_ref=get_reference('compute','ssl_bm','AES','1024B')
    ssl_AES8192B_bm_ref=get_reference('compute','ssl_bm','AES','8192B')
    
    ssl_RSA512b_bm_index=get_index(ssl_dict, "ssl_bm", ssl_RSA512b_bm_ref,'4  SSL result','2. RSA signatures','1. 512 bits (sign/s)')
    ssl_RSA1024b_bm_index=get_index(ssl_dict, "ssl_bm", ssl_RSA1024b_bm_ref,'4  SSL result','2. RSA signatures','2. 1024 bits (sign/s)')
    ssl_RSA2048b_bm_index=get_index(ssl_dict, "ssl_bm", ssl_RSA2048b_bm_ref,'4  SSL result','2. RSA signatures','3. 2048 bits (sign/s)')
    ssl_RSA4096b_bm_index=get_index(ssl_dict, "ssl_bm", ssl_RSA4096b_bm_ref,'4  SSL result','2. RSA signatures','4. 4096 bits (sign/s)')
    ssl_RSA_bm_index=(ssl_RSA512b_bm_index+ssl_RSA1024b_bm_index+ssl_RSA2048b_bm_index+ssl_RSA4096b_bm_index)/4
    
    
    ssl_AES16B_bm_index=get_index(ssl_dict, "ssl_bm", ssl_AES16B_bm_ref,'4  SSL result','3. AES-128-cbc throughput','1. 16 Bytes block (B/sec)')
    ssl_AES64B_bm_index=get_index(ssl_dict, "ssl_bm", ssl_AES64B_bm_ref,'4  SSL result','3. AES-128-cbc throughput','2. 64 Bytes block (B/sec)')
    ssl_AES256B_bm_index=get_index(ssl_dict, "ssl_bm", ssl_AES256B_bm_ref,'4  SSL result','3. AES-128-cbc throughput','3. 256 Bytes block (B/sec)') 
    ssl_AES1024B_bm_index=get_index(ssl_dict, "ssl_bm", ssl_AES1024B_bm_ref,'4  SSL result','3. AES-128-cbc throughput','4. 1024 Bytes block (B/sec)')
    ssl_AES8192B_bm_index=get_index(ssl_dict, "ssl_bm", ssl_AES8192B_bm_ref,'4  SSL result','3. AES-128-cbc throughput','5. 8192 Bytes block (B/sec)')
    ssl_AES_bm_index=(ssl_AES16B_bm_index+ssl_AES64B_bm_index+ssl_AES256B_bm_index+ssl_AES1024B_bm_index+ssl_AES8192B_bm_index)/5
    
    ssl_bm_index=(ssl_RSA_bm_index+ssl_AES_bm_index)/2
    
    ssl_RSA512b_vm_ref=get_reference('compute','ssl_vm','RSA','512b')
    ssl_RSA1024b_vm_ref=get_reference('compute','ssl_vm','RSA','1024b')
    ssl_RSA2048b_vm_ref=get_reference('compute','ssl_vm','RSA','2048b')
    ssl_RSA4096b_vm_ref=get_reference('compute','ssl_vm','RSA','4096b')
    
    
    ssl_AES16B_vm_ref=get_reference('compute','ssl_vm','AES','16B')
    ssl_AES64B_vm_ref=get_reference('compute','ssl_vm','AES','64B')
    ssl_AES256B_vm_ref=get_reference('compute','ssl_vm','AES','256B')
    ssl_AES1024B_vm_ref=get_reference('compute','ssl_vm','AES','1024B')
    ssl_AES8192B_vm_ref=get_reference('compute','ssl_vm','AES','8192B')
    
    ssl_RSA512b_vm_index=get_index(ssl_dict, "ssl_vm", ssl_RSA512b_vm_ref,'4  SSL result','2. RSA signatures','1. 512 bits (sign/s)')
    ssl_RSA1024b_vm_index=get_index(ssl_dict, "ssl_vm", ssl_RSA1024b_vm_ref,'4  SSL result','2. RSA signatures','2. 1024 bits (sign/s)')
    ssl_RSA2048b_vm_index=get_index(ssl_dict, "ssl_vm", ssl_RSA2048b_vm_ref,'4  SSL result','2. RSA signatures','3. 2048 bits (sign/s)')
    ssl_RSA4096b_vm_index=get_index(ssl_dict, "ssl_vm", ssl_RSA4096b_vm_ref,'4  SSL result','2. RSA signatures','4. 4096 bits (sign/s)')
    ssl_RSA_vm_index=(ssl_RSA512b_vm_index+ssl_RSA1024b_vm_index+ssl_RSA2048b_vm_index+ssl_RSA4096b_vm_index)/4
    
    
    ssl_AES16B_vm_index=get_index(ssl_dict, "ssl_vm", ssl_AES16B_vm_ref,'4  SSL result','3. AES-128-cbc throughput','1. 16 Bytes block (B/sec)')
    ssl_AES64B_vm_index=get_index(ssl_dict, "ssl_vm", ssl_AES64B_vm_ref,'4  SSL result','3. AES-128-cbc throughput','2. 64 Bytes block (B/sec)')
    ssl_AES256B_vm_index=get_index(ssl_dict, "ssl_vm", ssl_AES256B_vm_ref,'4  SSL result','3. AES-128-cbc throughput','3. 256 Bytes block (B/sec)') 
    ssl_AES1024B_vm_index=get_index(ssl_dict, "ssl_vm", ssl_AES1024B_vm_ref,'4  SSL result','3. AES-128-cbc throughput','4. 1024 Bytes block (B/sec)')
    ssl_AES8192B_vm_index=get_index(ssl_dict, "ssl_vm", ssl_AES8192B_vm_ref,'4  SSL result','3. AES-128-cbc throughput','5. 8192 Bytes block (B/sec)')
    ssl_AES_vm_index=(ssl_AES16B_vm_index+ssl_AES64B_vm_index+ssl_AES256B_vm_index+ssl_AES1024B_vm_index+ssl_AES8192B_vm_index)/5
    
    ssl_vm_index=(ssl_RSA_vm_index+ssl_AES_vm_index)/2
    
    ssl_index=(ssl_bm_index+ssl_vm_index)/2
    
   
    ssl_dict_i={};
    ssl_dict_i['1. Index']=ssl_index
    ssl_dict_i['2. Results']=ssl_dict
    return ssl_dict_i
