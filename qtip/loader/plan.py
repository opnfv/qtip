##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from qtip.base.constant import PlanProp
from qtip.collector.logfile import LogfileCollector
from qtip.loader.yaml_file import YamlFileLoader
from qtip.loader.qpi import QPISpec


class Plan(YamlFileLoader):
    """
    a benchmark plan is consist of configuration and a QPI list
    """

    RELATIVE_PATH = 'plan'

    def __init__(self, name, paths=None):
        super(Plan, self).__init__(name, paths)

        self.qpis = [QPISpec(qpi, paths=paths)
                     for qpi in self.content[PlanProp.QPIS]]
        _config = self.content[PlanProp.CONFIG]

        # TODO(yujunz) create collector by name
        self.collector = LogfileCollector(_config[PlanProp.COLLECTOR], paths)
