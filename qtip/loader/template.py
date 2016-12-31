##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from jinja2 import Environment, FileSystemLoader

from base import BaseLoader


class Template(BaseLoader):
    RELATIVE_PATH = 'template'

    def __init__(self, name, paths=None):
        super(Template, self).__init__(name, paths=paths)
        self._env = Environment(loader=FileSystemLoader(self._abspath))
        self.get_template = self._env.get_template
