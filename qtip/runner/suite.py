##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class Suite:
    """A suite is consist of one or several perf tests and produces one QPI"""

    def __init__(self):
        pass

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
