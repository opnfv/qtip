##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import glob
import json
from os import path

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template
from qtip.base import BaseActor

ROOT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir)


def justify(pair, width=80):
    """align the beginning along the left margin, ending along the right, padding with space"""
    padding = width - len(pair[0])
    return '{1}{2:>{0}}'.format(padding, pair[0], pair[1])


class ConsoleReporter(BaseActor):
    """ report benchmark result to console """

    def __init__(self, config, parent=None):
        super(ConsoleReporter, self).__init__(config, parent=parent)

        # TODO (taseer) load template from config
        tpl_path = path.join(path.dirname(__file__), 'templates')
        tpl_loader = FileSystemLoader(tpl_path)
        self._env = Environment(loader=tpl_loader)

    def load_result(self, result_path):
        result_dirs = glob.glob('{}/qtip-*'.format(result_path))
        # select the last (latest) directory for rendering report, result_dirs[-1]
        with open(path.join(result_path, result_dirs[-1], 'result.json')) as sample:
            result = json.load(sample)
        return result

    def render(self, metric, result_path):
        template = self._env.get_template('base.j2')
        var_dict = self.load_result(result_path)
        var_dict['metric_name'] = metric
        out = template.render(var_dict)
        return out

    def jinja2_filter_sample(self):
        self._env.filters['justify'] = justify
        template = self._env.from_string('{{ kvpair|justify(width=20) }}')
        return template.render(kvpair=('key', 'value'))
