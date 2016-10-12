import json
import storage_benchmarks_indices as benchmark_indices


storage_dict = {}
try:
    storage_dict['FIO'] = benchmark_indices.fio_index()
except OSError:
    pass

storage_bench_list = ['FIO']
l = len(storage_bench_list)
temp = 0
for benchmark in storage_bench_list:
    try:
        temp = temp + float(storage_dict[benchmark]['index'])
    except KeyError:
        l -= 1
if l == 0:
    print "No Storage results found"
else:
    storage_suite_index = temp / l
    storage_dict_f = {}
    storage_dict_f['index'] = storage_suite_index
    storage_dict_f['storage_suite'] = storage_dict
    with open('../../results/storage_result.json', 'w+') as result_json:
        json.dump(storage_dict_f, result_json, indent=4, sort_keys=True)
