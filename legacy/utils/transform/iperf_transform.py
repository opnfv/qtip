##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
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

time_stamp = str(datetime.datetime.utcnow().isoformat())

result = {'version': raw_iperf_data['start']['version'],
          'bandwidth': {'sender_throughput': bits_sent,
                        'received_throughput': bits_received},
          'cpu': {'cpu_host': cpu_host_total_percent,
                  'cpu_remote': cpu_remote_total_percent}
          }

with open('iperf_raw-' + time_stamp + '.log', 'w+') as ofile:
    ofile.write(json.dumps(raw_iperf_data))

with open('./result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)
