##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import json
import pickle
import os
import datetime


def get_fio_job_result(fio_job_data):
    return {'read': {'io_bytes': fio_job_data["read"]["io_bytes"],
                     'io_ps': fio_job_data["read"]["iops"],
                     'io_runtime_millisec': fio_job_data["read"]["runtime"],
                     'mean_io_latenchy_microsec': fio_job_data["read"]["lat"]["mean"]},
            'write': {'io_bytes': fio_job_data["write"]["io_bytes"],
                      'io_ps': fio_job_data["write"]["iops"],
                      'io_runtime_millisec': fio_job_data["write"]["runtime"],
                      'mean_io_latenchy_microsec': fio_job_data["write"]["lat"]["mean"]}}


with open("fio_result.json") as fio_raw:
    fio_data = json.load(fio_raw)

fio_result_dict = {}
for x, result in enumerate(map(get_fio_job_result, fio_data["jobs"])):
    fio_result_dict['job_{0}'.format(x)] = result

host_name = (os.popen("hostname").read().rstrip())
report_time = str(datetime.datetime.utcnow().isoformat())
os.system("mv fio_result.json " + str(host_name) + "-" + report_time + ".log")
with open('./result_temp', 'w + ')as out_fio_result:
    pickle.dump(fio_result_dict, out_fio_result)
