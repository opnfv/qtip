##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path


class Fixture(object):
    PATH = path.abspath(path.join(path.dirname(__file__), 'data'))

    @classmethod
    def abspath(cls, name):
        return path.join(cls.PATH, name)
