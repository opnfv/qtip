##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class JobModel:
    resource_fields = {
        'installer_type': fields.String,
        'installer_ip': fields.String,
        'max_minutes': fields.Integer,
        'pod_name': fields.String,
        'suite_name': fields.String,
        'type': fields.String,
        'benchmark_name': fields.String,
        'testdb_url': fields.String,
        'node_name': fields.String
    }
    required = ['installer_type', 'installer_ip']


@swagger.model
class JobResponseModel:
    resource_fields = {
        'job_id': fields.String
    }
