import pickle
import json
import datetime
import os
import sys

home_dir = str((os.popen("echo $HOME").read().rstrip()))

with open('./sys_info_temp', 'r') as sys_info_f:
    sys_info_dict = pickle.load(sys_info_f)
with open('./result_temp', 'r') as result_f:
    result_dict = pickle.load(result_f)

host_name = (os.popen("hostname").read().rstrip())
benchmark_name = str(sys.argv[1])
report_time_stamp = str(datetime.datetime.utcnow().isoformat())
final_dict = {}
final_dict['1  Time of Report'] = report_time_stamp
final_dict['2  System Information'] = sys_info_dict
final_dict['3  ' + benchmark_name + ' result'] = result_dict

with open('./' + host_name + '-' + report_time_stamp + '.json', 'w+') as result_json:
    json.dump(final_dict, result_json, indent=4, sort_keys=True)
