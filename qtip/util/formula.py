##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import numpy

from qtip.util.dev import create_to_be_done
from qtip.base.constant import FormulaName


MAPPING = {
    FormulaName.ARITHMETIC_MEAN: numpy.mean,
    FormulaName.WEIGHTED_ARITHMETIC_MEAN: numpy.average,
    # TODO(yujunz) find or implement the method
    FormulaName.GEOMETRIC_MEAN: create_to_be_done(FormulaName.GEOMETRIC_MEAN, __name__),
    # TODO(yujunz) find or implement the method
    FormulaName.WEIGHTED_GEOMETRIC_MEAN:
        create_to_be_done(FormulaName.GEOMETRIC_MEAN, __name__)}


class Formula:
    """calculate a score from give data"""
    def __init__(self, name):
        self.calculate = MAPPING[name]
