import json
import datetime
import pickle
with open('iperf_raw.json', 'r') as ifile:
    raw_iperf_data = json.loads(ifile.read().rstrip())

bits_sent = raw_iperf_data['end']['sum_sent']['bits_per_second']
bits_received = raw_iperf_data['end']['sum_received']['bits_per_second']
total_byte_sent = raw_iperf_data['end']['sum_sent']['bytes']
total_byte_received = raw_iperf_data['end']['sum_received']['bytes']
cpu_host_total_percent = raw_iperf_data['end']['cpu_utilization_percent']['host_total']
cpu_remote_total_percent = raw_iperf_data['end']['cpu_utilization_percent']['remote_total']

result = {}
time_stamp = str(datetime.datetime.utcnow().isoformat())

result['1. Version'] = raw_iperf_data['start']['version']
result['2. Bandwidth'] = {}
result['2. Bandwidth']['1. throughput Sender (b/s)'] = bits_sent
result['2. Bandwidth']['2. throughput Received (b/s)'] = bits_received
result['3. CPU'] = {}
result['3. CPU']['1. CPU host total (%)'] = cpu_host_total_percent
result['3. CPU']['2. CPU remote total (%)'] = cpu_remote_total_percent

with open('iperf_raw-' + time_stamp + '.log', 'w+') as ofile:
    ofile.write(json.dumps(raw_iperf_data))

with open('./result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)
