import json
import storage_benchmarks_indices as benchmark_indices


storage_dict={};
storage_dict['FIO']=benchmark_indices.fio_index()




storage_bench_list=['FIO']
temp=0
for benchmark in storage_bench_list:
    temp=temp+float(storage_dict[benchmark]['1. Index'])
storage_suite_index=temp/len(storage_bench_list)

storage_dict_f={};
storage_dict_f['1. Storage Index']=storage_suite_index
storage_dict_f['2. Storage suite results']=storage_dict
with open('../../results/storage_result.json', 'w+') as result_json:
    json.dump(storage_dict_f, result_json, indent=4, sort_keys=True)

