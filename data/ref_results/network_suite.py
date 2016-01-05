import json
import network_benchmarks_indices as benchmark_indices


network_dict={};
network_dict['IPERF']=benchmark_indices.iperf_index()




network_bench_list=['IPERF']
temp=0
for benchmark in network_bench_list:
    temp=temp+float(network_dict[benchmark]['1. Index'])
network_suite_index=temp/len(network_bench_list)

network_dict_f={};
network_dict_f['1. Network Index']=network_suite_index
network_dict_f['2. Network suite results']=network_dict
with open('../../results/network_result.json', 'w+') as result_json:
    json.dump(network_dict_f, result_json, indent=4, sort_keys=True)

