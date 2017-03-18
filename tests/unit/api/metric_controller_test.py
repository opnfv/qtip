###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import httplib
import json

from qtip.base.constant import BaseProp


def test_invalid_url(app_client):
    response_url_not_found = app_client.get("/v1.0/metrics/")
    assert response_url_not_found.status_code == httplib.NOT_FOUND


def test__get_list_plans(app_client):
    response_success = app_client.get("/v1.0/metrics")
    assert response_success.status_code == httplib.OK
    metric_list = json.loads(response_success.data)
    assert len(metric_list) > 0
    for desc in metric_list:
        assert BaseProp.NAME in desc
        assert BaseProp.ABSPATH in desc


def test_get_metric(app_client):
    response_success = app_client.get("/v1.0/metrics/dpi.yaml")
    assert response_success.status_code == httplib.OK
    metric_data = json.loads(response_success.data)
    assert BaseProp.NAME in metric_data
    assert BaseProp.ABSPATH in metric_data
    assert BaseProp.NAME in metric_data['content']
    assert BaseProp.WORKLOADS in metric_data['content']
    assert isinstance(metric_data['content'][BaseProp.WORKLOADS], list)
    response_not_found = app_client.get("/v1.0/metrics/fake.yaml")
    response_data = json.loads(response_not_found.data)
    assert response_not_found.status_code == httplib.NOT_FOUND
    assert response_data['title'] == "Metric Not Found"
