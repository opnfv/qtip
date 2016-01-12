import os
import json
from result_accum import result_concat as concat


def dpi_index ():
    total=0
    dpi_dict=concat('../../results/dpi/')
    for k,v in dpi_dict.iteritems():
        for i,j in dpi_dict[k].iteritems():
            if i=="3  DPI result": 
                raw_num=float(dpi_dict[k][i]["DPI_benchmark(Gb/s)"])
                total=total+raw_num
    
    l=len(dpi_dict)
    with open ('./reference.json') as reference_file:
        reference_djson=json.load(reference_file)
        dpi_ref=reference_djson['compute']['dpi']
    dpi_index= float((total/l)/dpi_ref)
    dpi_dict_i={};
    dpi_dict_i['1. Index']=dpi_index
    dpi_dict_i['2. Results']=dpi_dict
    return dpi_dict_i

def dwstone_index (file_dir,benchmark):
    total=0
    dwstone_dict=concat('../../results/'+file_dir+'/')
    for k,v in dwstone_dict.iteritems():
        for i,j in dwstone_dict[k].iteritems():
            if i=="3  "+benchmark+" result":
               for a,b in dwstone_dict[k][i].iteritems():
                   if a=="2.Single CPU test":
                       raw_num=float(dwstone_dict[k][i][a]["2.Index score"])
                       total=total+raw_num
   
    l= len(dwstone_dict)
    
    with open ('./reference.json') as reference_file:
        reference_djson=json.load(reference_file)
        dwstone_ref=reference_djson['compute'][file_dir]
    
    dwstone_index=float((total/l)/dwstone_ref)
    dwstone_dict_i={};
    dwstone_dict_i['1. Index']=dwstone_index
    dwstone_dict_i['2. Results']=dwstone_dict
    return dwstone_dict_i


def ramspeed_index ():
    total_int=0
    total_float=0
    ramspeed_dict=concat('../../results/ramspeed/')
    for k,v in ramspeed_dict.iteritems():
        for i,j in ramspeed_dict[k].iteritems():
            if i=="3  RamSpeed result":
                for a,b in ramspeed_dict[k][i].iteritems():
                    if a=="1. INTmem bandwidth":
                        raw_int=ramspeed_dict[k][i][a]["5. Average (MB/s)"]
                        total_int=total_int+float(raw_int)
                    elif a=="2. FLOATmem bandwidth":
                        raw_float=ramspeed_dict[k][i][a]["5. Average (MB/s)"]
                        total_float=total_float+float(raw_float)

    l=len(ramspeed_dict)
    with open ('./reference.json') as reference_file:
        reference_djson=json.load(reference_file)
        int_mem_ref=reference_djson['compute']['ramspeed']['INTmem']['Average (MB/s)']
        float_mem_ref=reference_djson['compute']['ramspeed']['FLOATmem']['Average (MB/s)']
        
    int_mem_index= float((total_int/l)/int_mem_ref)
    float_mem_index=float((total_float/l)/float_mem_ref)
    ramspeed_index=float((int_mem_index+float_mem_index)/2)
    ramspeed_dict_i={};
    ramspeed_dict_i['1. Index']=ramspeed_index
    ramspeed_dict_i['2. Results']=ramspeed_dict
    return ramspeed_dict_i


def ssl_index ():
    total_512rsa=0
    total_1024rsa=0
    total_2048rsa=0
    total_4096rsa=0

    total_16aes=0
    total_64aes=0
    total_256aes=0
    total_1024aes=0
    total_8192aes=0

    ssl_dict=concat('../../results/ssl/')
    for k,v in ssl_dict.iteritems():
        for i,j in ssl_dict[k].iteritems():
            if i=="3  SSL result":
               for a,b in ssl_dict[k][i].iteritems():
                   if a=="2. RSA signatures":
                       raw_num_512rsa=float(ssl_dict[k][i][a]["1. 512 bits (sign/s)"])
                       raw_num_1024rsa=float(ssl_dict[k][i][a]["2. 1024 bits (sign/s)"])
                       raw_num_2048rsa=float(ssl_dict[k][i][a]["3. 2048 bits (sign/s)"])
                       raw_num_4096rsa=float(ssl_dict[k][i][a]["4. 4096 bits (sign/s)"])
                       total_512rsa=total_512rsa+raw_num_512rsa
                       total_1024rsa=total_512rsa+raw_num_1024rsa
                       total_2048rsa=total_2048rsa+raw_num_2048rsa
                       total_4096rsa=total_4096rsa+raw_num_4096rsa
                   elif a=="3. AES-128-cbc throughput":
                       raw_num_16aes=float(ssl_dict[k][i][a]["1. 16 Bytes block (B/sec)"][:-1])*1000
                       raw_num_64aes=float(ssl_dict[k][i][a]["2. 64 Bytes block (B/sec)"][:-1])*1000
                       raw_num_256aes=float(ssl_dict[k][i][a]["3. 256 Bytes block (B/sec)"][:-1])*1000
                       raw_num_1024aes=float(ssl_dict[k][i][a]["4. 1024 Bytes block (B/sec)"][:-1])*1000
                       raw_num_8192aes=float(ssl_dict[k][i][a]["5. 8192 Bytes block (B/sec)"][:-1])*1000
                       total_16aes=raw_num_16aes+total_16aes
                       total_64aes=raw_num_64aes+total_64aes
                       total_256aes=raw_num_256aes+total_256aes
                       total_1024aes=raw_num_1024aes+total_1024aes
                       total_8192aes=raw_num_8192aes+total_8192aes

    with open ('./reference.json') as reference_file:
        reference_djson=json.load(reference_file)
        ssl_ref512rsa=reference_djson['compute']['ssl']['RSA']['512b']
        ssl_ref1024rsa=reference_djson['compute']['ssl']['RSA']['1024b']                
        ssl_ref2048rsa=reference_djson['compute']['ssl']['RSA']['2048b']
        ssl_ref4096rsa=reference_djson['compute']['ssl']['RSA']['4096b']
          
     
        ssl_ref16aes=reference_djson['compute']['ssl']['AES']['16B']
        ssl_ref64aes=reference_djson['compute']['ssl']['AES']['64B']
        ssl_ref256aes=reference_djson['compute']['ssl']['AES']['256B']
        ssl_ref1024aes=reference_djson['compute']['ssl']['AES']['1024B']
        ssl_ref8192aes=reference_djson['compute']['ssl']['AES']['8192B']


    l=len(ssl_dict)    
    index_512rsa=float((total_512rsa/l)/ssl_ref512rsa)
    index_1024rsa= float((total_1024rsa/l)/ssl_ref1024rsa)
    index_2048= float((total_2048rsa/l)/ssl_ref2048rsa)
    index_4096= float((total_4096rsa/l)/ssl_ref4096rsa)
    
    index_16aes=float((total_16aes/l)/ssl_ref16aes)
    index_64aes=float((total_64aes/l)/ssl_ref64aes)
    index_256aes=float((total_256aes/l)/ssl_ref256aes)
    index_1024aes=float((total_1024aes/l)/ssl_ref1024aes)
    index_8192aes=float((total_8192aes/l)/ssl_ref8192aes)
      
    index_sum= (index_512rsa+index_1024rsa+index_2048+index_4096+index_16aes+index_64aes+index_256aes+index_1024aes+index_8192aes)
    ssl_index=float(index_sum/9)
    ssl_dict_i={};
    ssl_dict_i['1. Index']=ssl_index
    ssl_dict_i['2. Results']=ssl_dict
    return ssl_dict_i

  





















    
