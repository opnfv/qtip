from index_calculation import generic_index as get_index
from index_calculation import get_reference 
from result_accum import result_concat as concat


def fio_index ():
    fio_dict=concat('../../results/fio/')
    #print _perf_dict    
    fio_r_bm_ref = get_reference('storage','fio_bm','read','IOPS')
    fio_r_bm_index= get_index(fio_dict,'fio_bm',fio_r_bm_ref,'4  FIO result', 'Job_0','read','IO/sec')
    
    fio_w_bm_ref = get_reference('storage','fio_bm','write','IOPS')
    fio_w_bm_index= get_index(fio_dict,'fio_bm',fio_w_bm_ref,'4  FIO result', 'Job_0','write','IO/sec')
   
    fio_bm_index= (fio_r_bm_index+fio_w_bm_index)/2



    fio_r_vm_ref = get_reference('storage','fio_vm','read','IOPS')
    fio_r_vm_index= get_index(fio_dict,'fio_vm',fio_r_vm_ref,'4  FIO result', 'Job_0','read','IO/sec')
    
    fio_w_vm_ref = get_reference('storage','fio_vm','write','IOPS')
    fio_w_vm_index= get_index(fio_dict,'fio_vm',fio_w_vm_ref,'4  FIO result', 'Job_0','write','IO/sec')
   
    fio_vm_index= (fio_r_vm_index+fio_w_vm_index)/2
    
    fio_index=(fio_bm_index+fio_vm_index)/2
    print fio_index
        
    fio_dict_i={};
    fio_dict_i['1. Index']=fio_index
    fio_dict_i['2. Results']=fio_dict
    return fio_dict_i
    
