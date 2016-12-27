##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.constant import AlgoName, PropName
from qtip.spec.qpi import QPISpec

QPI_SPEC = 'compute.yaml'


@pytest.fixture()
def qpi_spec(benchmarks_root):
    return QPISpec('compute.yaml', paths=[benchmarks_root])


def test_init(qpi_spec):
    assert qpi_spec.name == 'compute'

    with pytest.raises(TypeError) as excinfo:
        QPISpec()
    assert '__init__() takes at least 2 arguments (1 given)' \
        in str(excinfo.value)


def test_list_all(benchmarks_root):
    qpi_spec_list = QPISpec.list_all(paths=[benchmarks_root])
    assert len(list(qpi_spec_list)) is 2
    for item in qpi_spec_list:
        assert PropName.NAME in item
        assert PropName.CONTENT in item
        assert PropName.ABSPATH in item
        assert PropName.ABSPATH is not None


def test_content(qpi_spec):
    content = qpi_spec.content
    assert PropName.DESCRIPTION in content
    assert PropName.ALGORITHM in content
    assert PropName.SECTIONS in content

    assert content[PropName.ALGORITHM] in AlgoName.__dict__.values()
    sections = content[PropName.SECTIONS]
    assert isinstance(sections, list)
    for section in sections:
        assert PropName.NAME in section
