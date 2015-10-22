import os
import json
import pickle
import datetime

sum_dpi_pps = float(0)
sum_dpi_bps = float(0)

for x in range(1, 11):
    dpi_result_pps = float(
        os.popen(
            "cat $HOME/qtip_result/dpi_dump.txt | grep 'nDPI throughput:' | awk 'NR=='" +
            str(x) +
            " | awk '{print $3}'").read().lstrip())
    dpi_result_bps = float(
        os.popen(
            "cat $HOME/qtip_result/dpi_dump.txt | grep 'nDPI throughput:' | awk 'NR=='" +
            str(x) +
            " | awk '{print $7}'").read().rstrip())

    if (dpi_result_pps > 100):
        dpi_result_pps = dpi_result_pps / 1000

    if (dpi_result_bps > 100):
        dpi_result_bps = dpi_result_bps / 1000

    sum_dpi_pps += dpi_result_pps
    sum_dpi_bps += dpi_result_bps

dpi_result_pps = sum_dpi_pps / 10
dpi_result_bps = sum_dpi_bps / 10

host = os.popen("hostname").read().rstrip()
log_time_stamp = str(datetime.datetime.utcnow().isoformat())

os.popen(
    "cat $HOME/qtip_result/dpi_dump.txt > $HOME/qtip_result/" +
    host +
    "-" +
    log_time_stamp +
    ".log")

home_dir = str(os.popen("echo $HOME").read().rstrip())
host = os.popen("echo $HOSTNAME")
result = {}
result['DPI_benchmark(M pps)'] = round(dpi_result_pps, 3)
result['DPI_benchmark(Gb/s)'] = round(dpi_result_bps, 3)
with open('./result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)
print json.dumps(result, indent=4, sort_keys=True)
