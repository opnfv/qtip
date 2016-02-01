import json
from cinderclient.utils import arg
from result_accum import result_concat as concat
from cliff.tests.test_formatters_table import args

def compute_index(total_measured,ref_result,count):
    try:
        average=float(total_measured/count)
        
    except ZeroDivisionError:
        average=0
    
    index=average/ref_result
    return index

def get_reference (*args):
    
    with open ('./reference.json') as reference_file:
        reference_djson=json.load(reference_file)
        temp=list(args)
        for arg in args:
            ref_n=reference_djson.get(str(arg))
            reference_djson=reference_djson.get(str(arg))

          
    return ref_n

def generic_index(dict_gen,testcase,reference_num,*args):
    c=len(args)
    count=0
    total=0
    result=0
    for k,v in dict_gen.iteritems():           
        dict_temp=dict_gen[k]
        if dict_gen[k]['1  Testcase Name'] == str(testcase):
            count=count+1
            for arg in args:
                if arg == args[c-1]:
                    result=float(dict_temp.get(str(arg)))
                dict_temp=dict_temp.get(str(arg))
            total=total+result
    return compute_index(total, reference_num, count)
    
    