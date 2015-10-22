import os
import json
import pickle
import datetime

total_cpu = os.popen(
    "cat /root/tempT/UnixBench/results/* | grep 'of tests' | awk '{print $1;}' | awk 'NR==1'").read().rstrip()

cpu_1 = os.popen(
    "cat /root/tempT/UnixBench/results/* | grep 'of tests' | awk '{print $6;}' | awk 'NR==1'").read().rstrip()


cpu_2 = os.popen(
    "cat /root/tempT/UnixBench/results/* | grep 'of tests' | awk '{print $6;}' | awk 'NR==2'").read().rstrip()


Index_1 = os.popen(
    "cat /root/tempT/UnixBench/results/* | grep 'Index Score (Partial Only)  ' | awk '{print $7;}' | awk 'NR==1'").read().rstrip()
Index_2 = os.popen(
    "cat /root/tempT/UnixBench/results/* | grep 'Index Score (Partial Only)  ' | awk '{print $7;}' | awk 'NR==2'").read().rstrip()


result = {}
result['1.Number of CPU(s) in system'] = total_cpu
result['2.Single CPU test'] = {}
result['2.Single CPU test']['1.Number of parallell test(s)'] = cpu_1
result['2.Single CPU test']['2.Index score'] = Index_1
result['3.Multi CPU test'] = {}
result['3.Multi CPU test']['1.Number of parallell test(s)'] = cpu_2
result['3.Multi CPU test']['2.Index score'] = Index_2

with open('/root/qtip_result/result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)
print json.dumps(result, indent=4, sort_keys=True)
# print result.items()
