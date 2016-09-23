import json
import network_benchmarks_indices as benchmark_indices


network_dict = {}
try:
    network_dict['IPERF'] = benchmark_indices.iperf_index()
except:
    pass

network_bench_list = ['IPERF']
temp = 0
l = len(network_bench_list)

for benchmark in network_bench_list:
    try:
        temp = temp + float(network_dict[benchmark]['1. Index'])
    except:
        l = l - 1
        pass

if l == 0:
    print "No network results found"
else:
    network_suite_index = temp / len(network_bench_list)
    network_dict_f = {}
    network_dict_f['index'] = network_suite_index
    network_dict_f['suite_results'] = network_dict
    with open('../../results/network_result.json', 'w+') as result_json:
        json.dump(network_dict_f, result_json, indent=4, sort_keys=True)
