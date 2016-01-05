import os
import json
from result_accum import result_concat as concat

def iperf_index ():
    total_r=0
    iperf_dict=concat('../../results/iperf/')
    for k,v in iperf_dict.iteritems():
        for i,j in iperf_dict[k].iteritems():
            if i=="3  IPERF result":
               for a,b in iperf_dict[k][i].iteritems():        
                   if a=="2. Bandwidth":
                      raw_num=iperf_dict[k][i][a]['2. throughput Received (b/s)']
                      total_r=total_r+raw_num

    l= len(iperf_dict)

    with open ('./reference.json') as reference_file:
        reference_djson=json.load(reference_file)
        iperf_ref_r=reference_djson['network']['iperf']['throughput received(b/s)']
       

    iperf_index_r=float((total_r/l)/iperf_ref_r)
    iperf_dict_i={};
    iperf_dict_i['1. Index']=iperf_index_r
    iperf_dict_i['2. Results']=iperf_dict
    return iperf_dict_i

