import json
import compute_benchmarks_indices as benchmark_indices


compute_dict={};
compute_dict['DPI']=benchmark_indices.dpi_index()
compute_dict['Dhrystone']=benchmark_indices.dwstone_index('dhrystone','Dhrystone')
compute_dict['Whetstone']=benchmark_indices.dwstone_index('whetstone','Whetstone') 
compute_dict['SSL']=benchmark_indices.ssl_index()

compute_bench_list=['DPI','Dhrystone','Whetstone','SSL']
temp=0
for benchmark in compute_bench_list:
    temp=temp+float(compute_dict[benchmark]['1. Index'])
compute_suite_index=temp/len(compute_bench_list)

compute_dict_f={};
compute_dict_f['1. Compute Index']=compute_suite_index
compute_dict_f['2. Compute suite results']=compute_dict
with open('../../results/compute_result.json', 'w+') as result_json:
    json.dump(compute_dict_f, result_json, indent=4, sort_keys=True)

