##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from flask import Flask, abort
from flask_restful import Api, Resource, fields, reqparse
from flask_restful_swagger import swagger
import threading
from copy import copy
import db
import func.args_handler as args_handler


app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1')


@swagger.model
class JobModel:
    resource_fields = {
        'installer_type': fields.String,
        'installer_ip': fields.String,
        'max-minutes': fields.Integer,
        'pod_name': fields.String,
        'suite_name': fields.String,
        'type': fields.String
    }
    required = ['installer_type', 'install_ip']


@swagger.model
class JobResponseModel:
    resource_fields = {
        'job_id': fields.String
    }


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

"max-minutes": If specified, the maximum duration in minutes
for any single test iteration, default is '60',

"pod_name": If specified, the Pod name, default is 'default',

"suite_name": If specified, Test suite name, for example 'compute', 'network', 'storage',
default is 'compute'
"type": BM or VM,default is 'BM'
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
        parser.add_argument('installer_type', type=str, required=True, help='Installer_type is required')
        parser.add_argument('installer_ip', type=str, required=True, help='Installer_ip is required')
        parser.add_argument('max-minutes', type=int, required=False, default=60, help='max-minutes should be integer')
        parser.add_argument('pod_name', type=str, required=False, default='default', help='pod_name should be string')
        parser.add_argument('suite_name', type=str, required=False, default='compute', help='suite_name should be string')
        parser.add_argument('type', type=str, required=False, default='BM', help='type should be BM, VM and ALL')
        args = parser.parse_args()
        if not args_handler.check_suit_in_test_list(args["suite_name"]):
            return abort(404, 'message:Test Suit {0} does not exist in test_list'.format(args["suite_name"]))
        if not args_handler.check_lab_name(args["pod_name"]):
            return abort(404, 'message: You have specified a lab {0}\
                               that is not present in test_cases'.format(args['pod_name']))

        job_id = db.create_job(args)
        if not job_id:
            return abort(409, 'message:It already has one job running now!')

        benchmarks = args_handler.get_files_in_test_list(args["suite_name"],
                                                         args["type"].lower())
        test_cases = args_handler.get_files_in_test_case(args["pod_name"],
                                                         args["suite_name"],
                                                         args["type"].lower())
        benchmarks_list = filter(lambda x: x in test_cases, benchmarks)
        state_detail = map(lambda x: {'benchmark': x, 'state': 'idle'}, benchmarks_list)
        db.update_job_state_detail(job_id, copy(state_detail))
        thread_stop = threading.Event()
        post_thread = threading.Thread(target=self.thread_post, args=(args["installer_type"],
                                                                      benchmarks_list,
                                                                      args["pod_name"],
                                                                      args["suite_name"],
                                                                      job_id,
                                                                      thread_stop))
        db.start_thread(job_id, post_thread, thread_stop)
        return {'job_id': str(job_id)}

    def thread_post(self, installer_type, benchmarks_list, pod_name, suite_name, job_id, stop_event):
        for benchmark in benchmarks_list:
            if db.is_job_timeout(job_id) or stop_event.is_set():
                break
            db.update_benmark_state_in_state_detail(job_id, benchmark, 'processing')
            args_handler.prepare_and_run_benchmark(installer_type, '/home',
                                                   args_handler.get_benchmark_path(pod_name, suite_name, benchmark))
            db.update_benmark_state_in_state_detail(job_id, benchmark, 'finished')
        db.finish_job(job_id)


api.add_resource(JobList, '/api/v1.0/jobs')
api.add_resource(Job, '/api/v1.0/jobs/<string:id>')

if __name__ == "__main__":
    app.run(debug=True)
