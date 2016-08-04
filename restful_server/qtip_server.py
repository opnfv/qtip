##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from flask import Flask, abort
from flask_restful import Api, Resource, fields, reqparse
from flask_restful_swagger import swagger
import db


app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1')


@swagger.model
class JobModel:
    resource_fields = {
        'installer_type': fields.String,
        'installer_ip': fields.String,
        'deadline': fields.Integer,
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

"deadline": If specified, the maximum duration in minutes
for any single test iteration, default is '10',

"pod_name": If specified, the Pod name, default is 'default',

"suite_name": If specified, Test suite name, for example 'compute', 'network', 'storage', 'all',
default is 'all'
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
        parser.add_argument('deadline', type=int, required=False, default=10, help='dealine should be integer')
        parser.add_argument('pod_name', type=str, required=False, default='default', help='pod_name should be string')
        parser.add_argument('suite_name', type=str, required=False, default='all', help='suite_name should be string')
        parser.add_argument('type', type=str, required=False, default='BM', help='type should be BM, VM and ALL')
        args = parser.parse_args()
        ret = db.create_job(args)
        return {'job_id': str(ret)} if ret else abort(409, 'message:It already has one job running now!')


api.add_resource(JobList, '/api/v1.0/jobs')
api.add_resource(Job, '/api/v1.0/jobs/<string:id>')

if __name__ == "__main__":
    app.run(debug=True)
