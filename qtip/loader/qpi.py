##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from base import BaseLoader
from metric import MetricSpec

from qtip.base.constant import PropName
from qtip.util.formula import Formula


class QPISpec(BaseLoader):
    """
    a QPI specification defines how to calculate a performance index from
     collected metrics.
    """
    RELATIVE_PATH = 'QPI'

    def __init__(self, name, paths=None):
        super(QPISpec, self).__init__(name, paths=paths)
        content = self.content
        self.formula = Formula(content[PropName.FORMULA])
        self.sections = [Section(record, paths=paths)
                         for record in content[PropName.SECTIONS]]


class Section(object):
    def __init__(self, content, paths=None):
        self.name = content[PropName.NAME]
        self.weight = content[PropName.WEIGHT]
        self.formula = Formula(content[PropName.FORMULA])
        self.metrics = [MetricSpec(record, paths=paths)
                        for record in content[PropName.METRICS]]
