##############################################################################
# Copyright (c) 2017 ZTE corp. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os


def convert(vals):
    if vals:
        return " ".join(vals)


ARGS = 'ansible-playbook {}.yml {}'
NO_ARGS = 'ansible-playbook {}.yml'


def setup(extra_val):
    if extra_val:
        os.system(ARGS.format('setup', convert(extra_val)))
    else:
        os.system(NO_ARGS.format('setup'))


def run(extra_val):
    if extra_val:
        os.system(ARGS.format('run', convert(extra_val)))
    else:
        os.system(NO_ARGS.format('run'))


def teardown(extra_val):
    if extra_val:
        os.system(ARGS.format('teardown', convert(extra_val)))
    else:
        os.system(NO_ARGS.format('teardown'))
