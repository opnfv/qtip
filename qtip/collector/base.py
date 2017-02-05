##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from qtip.base.constant import BaseProp


class BaseCollector(object):
    """performance metrics collector"""
    def __init__(self, config, parent=None):
        self._config = config
        self._parent = parent


class CollectorProp(BaseProp):
    TYPE = 'type'
    LOGS = 'logs'
    FILENAME = 'filename'
    PARSERS = 'parsers'
    REGEX = 'regex'
    GROUP = 'group'
    PATHS = 'paths'
