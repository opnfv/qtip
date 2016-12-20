##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.runner.suite import Suite
from qtip.runner.case import Case
from qtip.spec.qpi import QPISpec


def init_test(suite):
    assert isinstance(suite.qpi, QPISpec)
    assert isinstance(suite.condition, dict)
    assert isinstance(suite.cases, list)
    for case in suite.cases:
        assert isinstance(case, Case)

    with pytest.raises(TypeError) as excinfo:
        Suite()
    assert '__init__() takes exactly 2 arguments (1 given)' \
           in str(excinfo.value)
