##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from datetime import datetime
import uuid

jobs = {}


def create_job(args):
    if len(filter(lambda x: jobs[x]['state'] == 'processing', jobs.keys())) > 0:
        return None
    else:
        job = {'job_id': str(uuid.uuid4()),
               'installer_type': args["installer_type"],
               'installer_ip': args["installer_ip"],
               'pod_name': args["pod_name"],
               'suite_name': args["suite_name"],
               'deadline': args["deadline"],
               'type': args["type"],
               'start-time': str(datetime.now()),
               'end-time': None,
               'state': 'processing',
               'state_detail': [],
               'result': []}
        jobs[job['job_id']] = job
        return job['job_id']


def delete_job(job_id):
    if job_id in jobs.keys():
        jobs[job_id]['end_time'] = datetime.now()
        jobs[job_id]['state'] = 'terminated'
        return True
    else:
        return False


def get_job_info(job_id):
    if job_id in jobs.keys():
        return jobs[job_id]
    else:
        return None
