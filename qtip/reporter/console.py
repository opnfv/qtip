##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from jinja2 import Environment
from jinja2 import FileSystemLoader
from os import path
from qtip.base import BaseActor


class ConsoleReporter(BaseActor):
    """
    report benchmark result to console
    """
    def __init__(self, config, parent=None):
        super(ConsoleReporter, self).__init__(config, parent=parent)

        # TODO (taseer) load template from config
        tpl_loader = FileSystemLoader(path.join(path.dirname(__file__), 'templates'))
        env = Environment(loader=tpl_loader)
        self._template = env.get_template('timeline.j2')

    def render(self, var_dict):
        out = self._template.render(var_dict)
        return out
