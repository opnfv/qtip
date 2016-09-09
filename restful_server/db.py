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
threads = {}


def create_job(args):
    if len(filter(lambda x: jobs[x]['state'] == 'processing', jobs.keys())) > 0:
        return None
    else:
        job = {'job_id': str(uuid.uuid4()),
               'installer_type': args["installer_type"],
               'installer_ip': args["installer_ip"],
               'pod_name': args["pod_name"],
               'suite_name': args["suite_name"],
               'max-minutes': args["max-minutes"],
               'type': args["type"],
               'start_time': str(datetime.now()),
               'end_time': None,
               'state': 'processing',
               'state_detail': [],
               'result': []}
        jobs[job['job_id']] = job
        return job['job_id']


def delete_job(job_id):
    if job_id in threads:
        stop_thread(job_id)
    if job_id in jobs:
        jobs[job_id]['end_time'] = str(datetime.now())
        jobs[job_id]['state'] = 'terminated'
        return True
    else:
        return False


def get_job_info(job_id):
    if job_id in jobs:
        return jobs[job_id]
    else:
        return None


def finish_job(job_id):
    jobs[job_id]['end_time'] = str(datetime.now())
    jobs[job_id]['state'] = 'finished'
    del threads[job_id]


def update_job_state_detail(job_id, state_detail):
    jobs[job_id]['state_detail'] = state_detail


def update_job_result(job_id, result):
    jobs[job_id]['result'] = result


def is_job_timeout(job_id):
    period = datetime.now() - datetime.strptime(jobs[job_id]['start_time'],
                                                "%Y-%m-%d %H:%M:%S.%f")
    return True if jobs[job_id]['max-minutes'] * 60 < period.total_seconds()\
        else False


def start_thread(job_id, thread, thread_stop):
    threads[job_id] = {'thread': thread,
                       'thread_stop': thread_stop}
    thread.start()


def stop_thread(job_id):
    if threads[job_id]['thread'].isAlive():
        threads[job_id]['thread_stop'].set()
        threads[job_id]['thread'].join()
    if job_id in threads:
        del threads[job_id]


def update_benmark_state_in_state_detail(job_id, benchmark, benchmark_state):
    filter(lambda x: x["benchmark"] == benchmark,
           get_job_info(job_id)["state_detail"])[0]['state'] = benchmark_state
