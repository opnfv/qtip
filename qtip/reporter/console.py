##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json

from jinja2 import Environment
from jinja2 import FileSystemLoader
from os import path
from qtip.base import BaseActor

ROOT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir)


class ConsoleReporter(BaseActor):
    """
    report benchmark result to console
    """
    def __init__(self, config, parent=None):
        super(ConsoleReporter, self).__init__(config, parent=parent)

        # TODO (taseer) load template from config
        tpl_path = path.join(path.dirname(__file__), 'templates')
        tpl_loader = FileSystemLoader(tpl_path)
        self._env = Environment(loader=tpl_loader)

        self.result_path = path.join(ROOT_DIR, 'collector')

    def load_result(self, name):
        with open(path.join(self.result_path, name)) as sample:
            result = json.load(sample)
        return result

    def render(self, name):
        template = self._env.get_template(name[0:-5] + '.j2')
        var_dict = self.load_result(name)
        out = template.render(var_dict)
        return out
