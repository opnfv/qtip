import json
import compute_benchmarks_indices as benchmark_indices


compute_dict = {}
try:
    compute_dict['DPI'] = benchmark_indices.dpi_index()
except OSError:
    pass

try:
    compute_dict['Dhrystone'] = benchmark_indices.dhrystone_index()
except OSError:
    pass

try:
    compute_dict['Whetstone'] = benchmark_indices.whetstone_index()
except OSError:
    pass

try:
    compute_dict['SSL'] = benchmark_indices.ssl_index()
except OSError:
    pass

try:
    compute_dict['RamSpeed'] = benchmark_indices.ramspeed_index()
except OSError:
    pass

compute_bench_list = ['DPI', 'Dhrystone', 'Whetstone', 'SSL', 'RamSpeed']
l = len(compute_bench_list)

temp = 0
for benchmark in compute_bench_list:
    try:
        temp = temp + float(compute_dict[benchmark]['1. Index'])
    except KeyError:
        l = l - 1
        pass

if l == 0:
    print "No compute suite results found"
else:
    compute_suite_index = temp / l
    compute_dict_f = {}
    compute_dict_f['index'] = compute_suite_index
    compute_dict_f['suite results'] = compute_dict
    with open('../../results/compute_result.json', 'w+') as result_json:
        json.dump(compute_dict_f, result_json, indent=4, sort_keys=True)
