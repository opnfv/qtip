##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import httplib
import json


from qtip.loader.plan import PlanProp


def test_invalid_url(app_client):
    response_url_not_found = app_client.get("/v1.0/fakeresource")
    assert response_url_not_found.status_code == httplib.NOT_FOUND


def test_get_list_plans(app_client):
    response_success = app_client.get("/v1.0/plans")
    assert response_success.status_code == httplib.OK
    plan_list = json.loads(response_success.data)['plans']
    assert len(plan_list) > 0
    assert plan_list[0].endswith('.yaml')


def test_get_plan(app_client):
    response_success = app_client.get("/v1.0/plans/sample.yaml")
    assert response_success.status_code == httplib.OK
    plan_data = json.loads(response_success.data)
    assert PlanProp.NAME in plan_data
    assert PlanProp.DESCRIPTION in plan_data
    assert PlanProp.CONFIG in plan_data
    assert PlanProp.QPIS in plan_data


def test_get_plan_not_found(app_client):
    response_not_found = app_client.get("/v1.0/plans/fake.yaml")
    response_data = json.loads(response_not_found.data)
    assert response_not_found.status_code == httplib.NOT_FOUND
    assert response_data['title'] == "Plan not found"


def test_runner_not_implemented(app_client):
    response_error = app_client.post("/v1.0/plans/fake.yaml?action=run", follow_redirects=False)
    assert response_error.status_code == httplib.NOT_IMPLEMENTED
