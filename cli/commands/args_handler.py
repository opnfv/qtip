##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import json
from prettytable import PrettyTable


def suite_list(path, table):
    table.field_names = ["Suite"]
    group = os.listdir(path)
    for filename in group:
        table.add_row([filename])
    return table


def perftest_list(path, table):
    table.field_names = ["Perftest"]
    group = os.listdir(path)
    for filename in group:
        with open(path + "/" + filename) as result:
            line = result.read()
            bm = json.loads(line)['bm']
            vm = json.loads(line)['vm']
            for points in bm:
                table.add_row([points])
            for points in vm:
                table.add_row([points])
    return table
