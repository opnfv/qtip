###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.error import InvalidContentError
from qtip.base.error import NotFoundError
from qtip.base.error import ToBeDoneError


def test_invalid_content(faker):
    filename = faker.file_name()
    error = InvalidContentError(filename)
    assert error.filename == filename


def test_not_found(faker):
    package = faker.pystr()
    module = faker.pystr()
    error = NotFoundError(module)
    assert error.needle == module
    assert error.heystack == 'qtip'

    error = NotFoundError(module, package)
    assert error.needle == module
    assert error.heystack == package


@pytest.fixture
def method(faker):
    return faker.pystr()


@pytest.fixture
def module(faker):
    return faker.pystr()


def test_to_be_done(method, module):
    error = ToBeDoneError(method, module)
    assert error.method == method
    assert error.module == module
