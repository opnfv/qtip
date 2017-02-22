###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.base.error import ToBeDoneError
from qtip.util.dev import create_to_be_done


def test_create_to_be_done(faker):
    method = faker.pystr()
    module = faker.pystr()

    tbd = create_to_be_done(method)
    assert callable(tbd)
    with pytest.raises(ToBeDoneError) as excinfo:
        tbd()
    assert excinfo.value.method == method
    assert excinfo.value.module == 'qtip'

    tbd = create_to_be_done(method, module)
    assert callable(tbd)
    with pytest.raises(ToBeDoneError) as excinfo:
        tbd()
    assert excinfo.value.method == method
    assert excinfo.value.module == module
