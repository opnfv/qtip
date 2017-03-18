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

from qtip.base.constant import FormulaName
from qtip.base.constant import SpecProp


def test_get_list_qpis(app_client):
    response_success = app_client.get("/v1.0/qpis")
    assert response_success.status_code == httplib.OK
    qpi_spec_list = json.loads(response_success.data)['qpis']
    assert len(qpi_spec_list) > 0
    assert qpi_spec_list[0].endswith('.yaml')


def test_get_qpi(app_client):
    response_success = app_client.get("/v1.0/qpis/compute.yaml")
    assert response_success.status_code == httplib.OK
    qpi_data = json.loads(response_success.data)
    assert SpecProp.DESCRIPTION in qpi_data
    assert SpecProp.FORMULA in qpi_data
    assert SpecProp.SECTIONS in qpi_data
    assert qpi_data[SpecProp.FORMULA] in FormulaName.__dict__.values()
    sections = qpi_data[SpecProp.SECTIONS]
    assert isinstance(sections, list)
    for section in sections:
        assert SpecProp.NAME in section


def test_get_qpi_not_found(app_client):
    response_not_found = app_client.get("/v1.0/qpis/fake.yaml")
    response_data = json.loads(response_not_found.data)
    assert response_not_found.status_code == httplib.NOT_FOUND
    assert response_data['title'] == "QPI not found"
