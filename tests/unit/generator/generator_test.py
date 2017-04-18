##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.generator.generator import QtipGenerator


@pytest.fixture
def qtip_generator():
    return QtipGenerator()


def test_constructor(qtip_generator):
    assert isinstance(qtip_generator, QtipGenerator)
