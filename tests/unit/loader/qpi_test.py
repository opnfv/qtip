##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.benchmark import Algorithm, Property
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
    assert len(list(qpi_spec_list)) is 1
    for item in qpi_spec_list:
        assert Property.NAME in item
        assert Property.CONTENT in item
        assert Property.ABSPATH in item
        assert Property.ABSPATH is not None


def test_content(qpi_spec):
    content = qpi_spec.content()
    assert Property.DESCRIPTION in content
    assert Property.ALGORITHM in content
    assert Property.SECTIONS in content

    assert content[Property.ALGORITHM] in Algorithm.__dict__.values()
    sections = content[Property.SECTIONS]
    assert isinstance(sections, list)
    for section in sections:
        assert Property.NAME in section
