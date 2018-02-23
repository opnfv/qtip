##############################################################################
# Copyright (c) 2018 Spirent Communications and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource, fields
from flask_restful_swagger import swagger

from nettest import NetTestMaster

app = Flask(__name__)
CORS(app)
api = swagger.docs(Api(app), apiVersion="1.0")

stcv_master = NetTestMaster()


@swagger.model
class StackRequestModel:
    resource_fields = {
        'stack_name': fields.String,
        'stack_type': fields.String,
        'public_network': fields.String,
        "stack_params": fields.Nested,
    }


@swagger.model
class StackResponseModel:
    resource_fields = {
        'stack_name': fields.String,
        'stack_created': fields.Boolean,
        "stack_id": fields.String
    }


class Stack(Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @swagger.operation(
        notes='Fetch the stack configuration',
        parameters=[
            {
                "name": "id",
                "description": "The UUID of the stack in the format "
                               "NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN",
                "required": True,
                "type": "string",
                "allowMultiple": False,
                "paramType": "query"
            },
        ],
        type=StackResponseModel.__name__
    )
    def get(self):
        stack_id = request.args.get('id')
        stack = stcv_master.get_stack_by_id(stack_id)

        if not stack:
            abort(404)

        return jsonify({
            'stack_name': stack.name,
            'stack_created': True,
            "stack_id": stack_id})

    @swagger.operation(
        notes='''set the current agent configuration and create a stack in
              the controller. Returns once the stack create is completed.''',
        parameters=[
            {
                "name": "stack",
                "description": '''Configuration to be set. All parameters are
            necessory.
            ''',
                "required": True,
                "type": "StackRequestModel",
                "paramType": "body"
            }
        ],
        type=StackResponseModel.__name__
    )
    def post(self):
        if not request.json:
            abort(400, "ERROR: No data specified")

        self.logger.info(request.json)

        try:
            params = {
                'lab_server_ip': request.json['stack_params'].get('lab_server_ip'),
                'license_server_ip': request.json['stack_params'].get('license_server_ip'),
                'stcv_image': request.json['stack_params'].get('stcv_image'),
                'stcv_flavor': request.json['stack_params'].get('stcv_flavor'),
                'stcv_affinity': request.json['stack_params'].get('stcv_affinity')
            }

            stack = stcv_master.create_stack(name=request.json['stack_name'],
                                             stack_type=request.json['stack_type'],
                                             pub_net_name=request.json['public_network'],
                                             **params)
            if stack is None:
                abort(400, "ERROR: create stack fail")

            return jsonify({'stack_name': request.json['stack_name'],
                            'stack_created': True,
                            'stack_id': stack.stack_id})

        except Exception as e:
            abort(400, str(e))

    @swagger.operation(
        notes='delete deployed stack',
        parameters=[
            {
                "name": "id",
                "description": "The UUID of the stack in the format "
                "NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN",
                "required": True,
                "type": "string",
                "allowMultiple": False,
                "paramType": "query"
            },
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Stack ID found, response in JSON format"
            },
            {
                "code": 404,
                "message": "Stack ID not found"
            }
        ]
    )
    def delete(self):
        try:
            stack_id = request.args.get('id')
            stcv_master.delete_stack(stack_id)
        except Exception as e:
            abort(400, str(e))


@swagger.model
class TestcaseRequestModel:
    resource_fields = {
        'name': fields.String,
        'category': fields.String,
        'stack_id': fields.String,
        'params': fields.Nested
    }


@swagger.model
class TestcaseResponseModel:
    resource_fields = {
        'name': fields.String,
        'category': fields.String,
        'stack_id': fields.String,
        'tc_id': fields.String
    }


class TestCase(Resource):

    """TestCase API"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @swagger.operation(
        notes='Fetch the metrics of the specified testcase',
        parameters=[
            {
                "name": "id",
                "description": "The UUID of the testcase in the format "
                "NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN",
                "required": True,
                "type": "string",
                "allowMultiple": False,
                "paramType": "query"
            },
            {
                "name": "type",
                "description": "The type of metrics to report. May be "
                "metrics (default), metadata, or status",
                "required": True,
                "type": "string",
                "allowMultiple": False,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Workload ID found, response in JSON format"
            },
            {
                "code": 404,
                "message": "Workload ID not found"
            }
        ]
    )
    def get(self):
        tc_id = request.args.get('id')
        query_type = request.args.get('type')
        ret = {}

        try:
            tc = stcv_master.get_tc_by_id(tc_id)
            if query_type == "result":
                ret = tc.get_result()

            if query_type == "status":
                status = tc.get_status()
                ret['status'] = status
                if 'error' == status:
                    reason = tc.get_err_reason()
                    ret['reason'] = reason

            return jsonify(ret)

        except Exception as err:
            abort(400, str(err))

    @swagger.operation(
        parameters=[
            {
                "name": "body",
                "description": """Start execution of a testcase with the
parameters, only support rfc25cc test
                """,
                "required": True,
                "type": "TestcaseRequestModel",
                "paramType": "body"
            }
        ],
        type=TestcaseResponseModel.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "TestCase submitted"
            },
            {
                "code": 400,
                "message": "Missing configuration data"
            }
        ]
    )
    def post(self):
        if not request.json:
            abort(400, "ERROR: Missing configuration data")

        self.logger.info(request.json)

        try:
            name = request.json['name']
            category = request.json['category']
            stack_id = request.json['stack_id']
            tc_id = stcv_master.execute_testcase(name=request.json['name'],
                                                 category=request.json['category'],
                                                 stack_id=request.json['stack_id'],
                                                 **request.json['params'])

            return jsonify({'name': name,
                            'category': category,
                            'stack_id': stack_id,
                            'tc_id': tc_id})

        except Exception as e:
            abort(400, str(e))

    @swagger.operation(
        notes='Cancels the currently running testcase or delete testcase result',
        parameters=[
            {
                "name": "id",
                "description": "The UUID of the testcase in the format "
                               "NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN",
                "required": True,
                "type": "string",
                "allowMultiple": False,
                "paramType": "query"
            },
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Wordload ID found, response in JSON format"
            },
        ]
    )
    def delete(self):
        try:
            tc_id = request.args.get("id")
            self.logger.info("receive delete testcase msg. tc_id = %s", tc_id)

            stcv_master.delete_testcase(tc_id)

        except Exception as e:
            abort(400, str(e))


api.add_resource(Stack, "/api/v1.0/stack")
api.add_resource(TestCase, "/api/v1.0/testcase")

'''
@app.route("/")
def hello_world():
    return 'hello world'

@app.route("/testcases")
def get_testcases():
    return []


@app.route("/testcases/<int: tc_id>")
def query_testcase(tc_id):
    return []

@app.route("/stctest/api/v1.0/testcase/<string: tc_name>", methods = ['GET'])
def query_tc_result(tc_name):
    return []

@app.route("/stctest/api/v1.0/testcase", methods = ['POST'])
def execut_testcase():
    return []
'''


if __name__ == "__main__":
    logger = logging.getLogger("nettest").setLevel(logging.DEBUG)

    app.run(host="0.0.0.0", debug=True, threaded=True)
