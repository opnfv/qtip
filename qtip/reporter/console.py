##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import os
from os import path

from qtip.base import BaseActor


ROOT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir)


class ConsoleReporter(BaseActor):
    """ report benchmark result to console """

    @staticmethod
    def load_result():
        result_path = path.join(os.getcwd(), 'results', 'current', 'qpi.json')
        with open(result_path) as qpi:
            result = json.load(qpi)
        return result
