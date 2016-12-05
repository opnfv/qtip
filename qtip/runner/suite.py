##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path


class Suite:
    """A suite is consist of one or several perf tests and produces one QPI"""
    root = path.join(path.dirname(__file__), path.pardir, path.pardir,
                     'benchmarks')

    def __init__(self, root=None):
        if root is not None:
            self.root = root

    @staticmethod
    def list_all():
        """list all available suites"""
        pass

    def desc(self):
        """description of the suite"""
        pass

    def run(self):
        """run included perftests in the suite"""
        pass
