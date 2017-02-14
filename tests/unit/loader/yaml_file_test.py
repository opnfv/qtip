##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import pytest

from qtip.loader.yaml_file import YamlFileLoader


@pytest.fixture
def yaml_root(data_root):
    return os.path.join(data_root, 'yaml')


def test_init(data_root):
    loader = YamlFileLoader('with_name.yaml', [yaml_root])
    assert loader.name =