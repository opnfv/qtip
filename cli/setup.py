##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from setuptools import setup

setup(
    name='qtip',
    py_modules=['entry'],
    include_package_data=True,
    install_requires=[
        'click', 'prettytable',
    ],
    entry_points='''
        [console_scripts]
        qtip=entry:cli
    ''',
)
