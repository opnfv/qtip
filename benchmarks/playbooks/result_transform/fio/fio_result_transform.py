import json
import pickle
import os
import datetime

with open("fio_result.json") as fio_raw:
    FIO_result_dict = json.load(fio_raw)

host_name = (os.popen("hostname").read().rstrip())
report_time = str(datetime.datetime.utcnow().isoformat())
os.system("mv fio_result.json " + str(host_name) + "-" + report_time + ".log")
with open('./result_temp', 'w + ')as out_fio_result:
    pickle.dump(FIO_result_dict, out_fio_result)
