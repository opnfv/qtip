##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import threading
from copy import copy

from flask_restful import Resource, reqparse
from flask_restful_swagger import swagger
from qtip.api.model.job_model import JobResponseModel
from qtip.utils import args_handler as args_handler
from werkzeug.exceptions import abort

from legacy.api.handler import db, result_handler


class Job(Resource):
    @swagger.operation(
        notes='get a job by ID',
        nickname='get',
        parameters=[],
        responseMessages=[
            {
                "code": 200,
                "message": "Job detail info."
            },
            {
                "code": 404,
                "message": "Can't not find the job id XXXXXXX"
            }
        ]
    )
    def get(self, id):
        ret = db.get_job_info(id)
        return ret if ret else abort(404, " Can't not find the job id %s" % id)

    @swagger.operation(
        notes='delete a job by ID',
        nickname='delete',
        parameters=[],
        responseMessages=[
            {
                "code": 200,
                "message": "Delete successfully"
            },
            {
                "code": 404,
                "message": "Can not find job_id XXXXXXXXX"
            }
        ]
    )
    def delete(self, id):
        ret = db.delete_job(id)
        return {'result': "Delete successfully"} if ret else abort(404, "Can not find job_id %s" % id)


class JobList(Resource):
    @swagger.operation(
        note='create a job with parameters',
        nickname='create',
        parameters=[
            {
                "name": "body",
                "description": """
"installer_type": The installer type, for example fuel, compass..,

"installer_ip": The installer ip of the pod,

"max_minutes": If specified, the maximum duration in minutes
for any single test iteration, default is '60',

"pod_name": If specified, the Pod name, default is 'default',

"suite_name": If specified, Test suite name, for example 'compute', 'network', 'storage',
default is 'compute',

"type": BM or VM,default is 'BM',

"benchmark_name": If specified, benchmark name in suite, for example 'dhrystone_bm.yaml',
default is all benchmarks in suite with specified type,

"testdb_url": test db http url, for example 'http://testresults.opnfv.org/test/api/v1',

"node_name": node name reported to test db
                """,
                "required": True,
                "type": "JobModel",
                "paramType": "body"
            }
        ],
        type=JobResponseModel.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "Job submitted"
            },
            {
                "code": 400,
                "message": "Missing configuration data"
            },
            {
                "code": 409,
                "message": "It already has one job running now!"
            }
        ]
    )
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('installer_type', type=str, required=True, help='installer_type is required')
        parser.add_argument('installer_ip', type=str, required=True, help='installer_ip is required')
        parser.add_argument('max_minutes', type=int, required=False, default=60, help='max_minutes should be integer')
        parser.add_argument('pod_name', type=str, required=False, default='default', help='pod_name should be string')
        parser.add_argument('suite_name', type=str, required=False, default='compute', help='suite_name should be string')
        parser.add_argument('type', type=str, required=False, default='BM', help='type should be BM, VM and ALL')
        parser.add_argument('benchmark_name', type=str, required=False, default='all', help='benchmark_name should be string')
        parser.add_argument('testdb_url', type=str, required=False, default=None,
                            help='testdb_url should be test db http url,for example http://testresults.opnfv.org/test/api/v1')
        parser.add_argument('node_name', type=str, required=False, default=None, help='node_name should be string')
        args = parser.parse_args()
        if not args_handler.check_suite(args["suite_name"]):
            return abort(404, 'message:Test suite {0} does not exist under benchmarks/suite'.format(args["suite_name"]))
        if not args_handler.check_lab_name(args["pod_name"]):
            return abort(404, 'message: You have specified a lab {0}\
                               that is not present in test_cases'.format(args['pod_name']))

        job_id = db.create_job(args)
        if not job_id:
            return abort(409, 'message:It already has one job running now!')

        benchmarks = args_handler.get_files_in_suite(args["suite_name"],
                                                     args["type"].lower())
        test_cases = args_handler.get_files_in_test_plan(args["pod_name"],
                                                         args["suite_name"],
                                                         args["type"].lower())
        benchmarks_list = filter(lambda x: x in test_cases, benchmarks)
        if args["benchmark_name"] in benchmarks_list:
            benchmarks_list = [args["benchmark_name"]]
        if (args["benchmark_name"] is not 'all') and args["benchmark_name"] not in benchmarks_list:
            return abort(404, 'message: Benchmark name {0} does not exist in suit {1}'.format(args["benchmark_name"],
                                                                                              args["suite_name"]))
        state_detail = map(lambda x: {'benchmark': x, 'state': 'idle'}, benchmarks_list)
        db.update_job_state_detail(job_id, copy(state_detail))
        thread_stop = threading.Event()
        post_thread = threading.Thread(target=self.thread_post, args=(args["installer_type"],
                                                                      benchmarks_list,
                                                                      args["pod_name"],
                                                                      args["suite_name"],
                                                                      job_id,
                                                                      args["testdb_url"],
                                                                      args["node_name"],
                                                                      thread_stop))
        db.start_thread(job_id, post_thread, thread_stop)
        return {'job_id': str(job_id)}

    def thread_post(self, installer_type, benchmarks_list, pod_name, suite_name,
                    job_id, testdb_url, node_name, stop_event):
        for benchmark in benchmarks_list:
            if db.is_job_timeout(job_id) or stop_event.is_set():
                break
            db.update_benchmark_state(job_id, benchmark, 'processing')
            result = args_handler.prepare_and_run_benchmark(installer_type,
                                                            '/home',
                                                            args_handler.get_benchmark_path(pod_name,
                                                                                            suite_name,
                                                                                            benchmark))
            db.update_job_result_detail(job_id, benchmark, copy(result))
            db.update_benchmark_state(job_id, benchmark, 'finished')
        if (result_handler.dump_suite_result(suite_name) and testdb_url):
            result_handler.push_suite_result_to_db(suite_name, testdb_url, installer_type, node_name)
        db.finish_job(job_id)
