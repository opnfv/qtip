import os
import json
from result_accum import result_concat as concat

def fio_index ():
    total_r=0
    total_w=0
    fio_dict=concat('../../results/fio/')
    for k,v in fio_dict.iteritems():
        for i,j in fio_dict[k].iteritems():
            if i=="3  FIO result":
               for a,b in fio_dict[k][i].iteritems():
                   for c,d in fio_dict[k][i][a].iteritems():
                        if c=='read':
                            raw_num=float(fio_dict[k][i][a][c]["IO/sec"])                   
                            total_r=total_r+raw_num
                        elif c=='write':
                            raw_num=float(fio_dict[k][i][a][c]["IO/sec"])
                            total_w=total_w+raw_num

    l= len(fio_dict)

    with open ('./reference.json') as reference_file:
        reference_djson=json.load(reference_file)
        fio_ref_r=reference_djson['storage']['read']['IOPS']
        fio_ref_w=reference_djson['storage']['write']['IOPS']

    fio_index_r=float((total_r/l)/fio_ref_r)
    fio_index_w=float((total_w/l)/fio_ref_w)
    fio_index=float((fio_index_r+fio_index_w)/2)
    fio_dict_i={};
    fio_dict_i['1. Index']=fio_index
    fio_dict_i['2. Results']=fio_dict
    return fio_dict_i

