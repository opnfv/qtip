##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.constant import FormulaName, SpecProp
from qtip.loader.qpi import QPISpec

QPI_SPEC = 'fake-qpi.yaml'


@pytest.fixture()
def qpi_spec(opt_root):
    return QPISpec(QPI_SPEC, paths=[opt_root])


def test_init(qpi_spec):
    assert qpi_spec.name == 'Fake QPI'

    with pytest.raises(TypeError) as excinfo:
        QPISpec()
    assert '__init__() takes at least 2 arguments (1 given)' \
        in str(excinfo.value)


def test_list_all(opt_root):
    qpi_spec_list = QPISpec.list_all(paths=[opt_root])
    assert len(list(qpi_spec_list)) is 1
    for item in qpi_spec_list:
        assert SpecProp.NAME in item
        assert SpecProp.CONTENT in item
        assert SpecProp.ABSPATH in item
        assert SpecProp.ABSPATH is not None


def test_content(qpi_spec):
    content = qpi_spec.content
    assert SpecProp.DESCRIPTION in content
    assert SpecProp.FORMULA in content
    assert SpecProp.SECTIONS in content

    assert content[SpecProp.FORMULA] in FormulaName.__dict__.values()
    sections = content[SpecProp.SECTIONS]
    assert isinstance(sections, list)
    for section in sections:
        assert SpecProp.NAME in section
