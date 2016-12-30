##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from qtip.base.constant import PropName
from qtip.loader.base import BaseLoader
from qtip.loader.qpi import QPISpec


class Plan(BaseLoader):
    """
    a benchmark plan is consist of configuration and a QPI list
    """

    RELATIVE_PATH = 'plan'

    def __init__(self, name, paths=None):
        super(Plan, self).__init__(name, paths)

        self.qpis = [QPISpec(qpi, paths=paths)
                     for qpi in self.content[PropName.QPIS]]
