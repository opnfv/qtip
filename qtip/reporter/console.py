##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import os
from os import path
import yaml

from qtip.base import BaseActor


ROOT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir)


class ConsoleReporter(BaseActor):
    """ report benchmark result to console """

    def load_result(self):
        result_path = path.join(os.getcwd(), 'results', 'current', 'qpi.json')
        with open(result_path) as sample:
            result = json.load(sample)
        return result

    def load_spec(self):
        spec_file = path.join(ROOT_DIR, 'resources', 'QPI', 'compute.yaml')
        with open(spec_file) as specs:
            spec = yaml.safe_load(specs)
        return spec

    def load_baseline(self):
        baseline = path.join(ROOT_DIR, 'resources', 'QPI', 'compute-baseline.json')
        with open(baseline) as base:
            bl = json.load(base)
        return bl

    def render(self):
        report = {}
        report['spec'] = self.load_spec()
        report['baseline'] = self.load_baseline()
        report['qpi'] = self.load_result()
        return report
