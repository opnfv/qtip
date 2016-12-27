##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class BaseDriver(object):
    """performance testing tool driver"""
    def pre_run(self):
        pass

    def run(self):
        pass

    def post_run(self):
        pass
