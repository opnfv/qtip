##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from qtip.base.constant import BaseProp
from qtip.collector import CollectorProp as CProp
from qtip.collector.logfile import LogfileCollector
from qtip.loader.yaml_file import YamlFileLoader
from qtip.loader.qpi import QPISpec


# TODO(yujunz) more elegant way to load module dynamically
def load_collector(type_name):
    if type_name == LogfileCollector.TYPE:
        return LogfileCollector
    else:
        raise Exception("Invalid collector type: {}".format(type_name))


class Plan(YamlFileLoader):
    """
    a benchmark plan is consist of configuration and a QPI list
    """

    RELATIVE_PATH = 'plan'

    def __init__(self, name, paths=None):
        super(Plan, self).__init__(name, paths)

        _config = self.content[PlanProp.CONFIG]

        self.collectors = [load_collector(c[CProp.TYPE])(c, self)
                           for c in _config[PlanProp.COLLECTORS]]

        self.qpis = [QPISpec(qpi, paths=paths)
                     for qpi in self.content[PlanProp.QPIS]]


class PlanProp(BaseProp):
    # plan
    INFO = 'info'

    FACILITY = 'facility'
    ENGINEER = 'engineer'

    CONFIG = 'config'

    DRIVER = 'driver'
    COLLECTORS = 'collectors'
    REPORTER = 'reporter'

    QPIS = 'QPIs'
