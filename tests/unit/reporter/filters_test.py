##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from jinja2 import Environment
import pytest

from qtip.reporter import filters


@pytest.mark.parametrize('template, content, output', [
    ('{{ content|justify(width=6) }}', [('k1', 'v1'), ('k2', 'v2')], 'k1..v1\nk2..v2'),
    ('{{ content|justify(width=6) }}', ('k1', 'v1'), 'k1..v1'),
    ('{{ content|justify(width=6) }}', {'k1': 'v1'}, 'k1..v1')
])
def test_justify(template, content, output):
    env = Environment()
    env.filters['justify'] = filters.justify
    template = env.from_string(template)
    assert template.render(content=content) == output
