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


def setup(extra_val=None):
    os.system('ansible-playbook setup.yml {}'.format(convert(extra_val)))


def run(extra_val=None):
    os.system('ansible-playbook run.yml {}'.format(convert(extra_val)))


def teardown(extra_val=None):
    os.system('ansible-playbook teardown.yml {}'.format(convert(extra_val)))
