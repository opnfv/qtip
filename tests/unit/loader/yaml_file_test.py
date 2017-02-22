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

from qtip.base.error import InvalidContentError
from qtip.loader.yaml_file import YamlFileLoader


@pytest.fixture
def yaml_root(data_root):
    return os.path.join(data_root, 'yaml')


@pytest.mark.parametrize('filename, expected', [
    ('with_name.yaml', 'name in content'),
    ('without_name.yaml', 'without_name')])
def test_init(yaml_root, filename, expected):
    loader = YamlFileLoader(filename, [yaml_root])
    assert loader.name == expected


def test_invalid_content(yaml_root):
    with pytest.raises(InvalidContentError) as excinfo:
        YamlFileLoader('invalid.yaml', [yaml_root])
    assert 'invalid.yaml' in excinfo.value.filename
