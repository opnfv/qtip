##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class BaseActor(object):
    """abstract actor class"""

    def __init__(self, config, parent=None):
        self._config = config
        self._parent = parent

    def get_config(self, key, default=None):
        return self._config.get(key, default)
