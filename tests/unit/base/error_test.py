###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.error import InvalidContent
from qtip.base.error import NotFound
from qtip.base.error import ToBeDone
from qtip.base.error import make_tbd


def test_invalid_content(faker):
    filename = faker.file_name()
    error = InvalidContent(filename)
    assert error.filename == filename


def test_not_found(faker):
    package = faker.pystr()
    module = faker.pystr()
    error = NotFound(module)
    assert error.module == module
    assert error.package == 'qtip'

    error = NotFound(module, package)
    assert error.module == module
    assert error.package == package


@pytest.fixture
def method(faker):
    return faker.pystr()


@pytest.fixture
def module(faker):
    return faker.pystr()


def test_to_be_done(method, module):
    error = ToBeDone(method, module)
    assert error.method == method
    assert error.module == module


def test_make_tbd(method, module):
    tbd = make_tbd(method)
    assert callable(tbd)
    with pytest.raises(ToBeDone) as excinfo:
        tbd()
    assert excinfo.value.method == method
    assert excinfo.value.module == 'qtip'

    tbd = make_tbd(method, module)
    assert callable(tbd)
    with pytest.raises(ToBeDone) as excinfo:
        tbd()
    assert excinfo.value.method == method
    assert excinfo.value.module == module
