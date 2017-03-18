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

from qtip.base.constant import FormulaName
from qtip.base.constant import SpecProp


def test_invalid_url(app_client):
    response_url_not_found = app_client.get("/v1.0/qpis/")
    assert response_url_not_found.status_code == httplib.NOT_FOUND


def test__get_list_qpis(app_client):
    response_success = app_client.get("/v1.0/qpis")
    assert response_success.status_code == httplib.OK
    qpi_spec_list = json.loads(response_success.data)
    assert len(qpi_spec_list) > 0
    for desc in qpi_spec_list:
        assert SpecProp.NAME in desc
        assert SpecProp.ABSPATH in desc


def test_get_qpi(app_client):
    response_success = app_client.get("/v1.0/qpis/compute.yaml")
    assert response_success.status_code == httplib.OK
    qpi_data = json.loads(response_success.data)
    assert SpecProp.NAME in qpi_data
    assert SpecProp.ABSPATH in qpi_data
    assert SpecProp.DESCRIPTION in qpi_data['content']
    assert SpecProp.FORMULA in qpi_data['content']
    assert SpecProp.SECTIONS in qpi_data['content']
    assert qpi_data['content'][SpecProp.FORMULA] in FormulaName.__dict__.values()
    sections = qpi_data['content'][SpecProp.SECTIONS]
    assert isinstance(sections, list)
    for section in sections:
        assert SpecProp.NAME in section
    response_not_found = app_client.get("/v1.0/qpis/fake.yaml")
    response_data = json.loads(response_not_found.data)
    assert response_not_found.status_code == httplib.NOT_FOUND
    assert response_data['title'] == "QPI Not Found"
