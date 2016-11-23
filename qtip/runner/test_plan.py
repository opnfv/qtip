##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class TestPlan:
    """A test plan is consist of test configuration and selected test suites"""

    def __init__(self):
        pass

    @staticmethod
    def list_all():
        """list all available test plans"""
        pass

    def desc(self):
        """description of the test plan"""
        pass

    def run(self):
        """run included suites"""
        pass
