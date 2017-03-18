##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import pytest

from qtip.api import __main__


@pytest.fixture(scope="session")
def app():
    return __main__.get_app().app


@pytest.fixture(scope="session")
def app_client(app):
    return app.test_client()
