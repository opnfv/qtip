from flask.ext.restful import fields
from flask.ext.restful_swagger import swagger


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
