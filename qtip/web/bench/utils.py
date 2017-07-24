##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
from subprocess import Popen, PIPE, STDOUT
import shutil


def run(repo):
    if os.path.exists(repo.name):
        shutil.rmtree(repo.name)
    os.mkdir(repo.name)
    os.chdir(repo.name)
    output = Popen(("git clone %s ." % repo.git_link).split(), stdout=PIPE, stderr=STDOUT)
    for line in output.stdout:
        yield line
    output.wait()
    output = Popen("ansible-playbook run.yml".split(), stdout=PIPE, stderr=STDOUT)
    for line in output.stdout:
        yield line
    os.chdir("../")
