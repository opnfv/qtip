##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from prettytable import PrettyTable
import os
import args_handler


class CliSuite:

    def __init__(self):
        self.path = '/home/taseer/qtip/test_list'
        self.table = PrettyTable()

    def list(self):
        self.table = args_handler.suite_list(self.path, self.table)
        print(self.table)

    def run(self):
        print("Run a Suite")
