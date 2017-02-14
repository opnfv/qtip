##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class BaseError(Exception):
    pass


class InvalidContent(BaseError):
    def __init__(self, filename, excinfo=None):
        self.filename = filename
        self.excinfo = excinfo


class NotFound(BaseError):
    def __init__(self, module, package='qtip'):
        self.package = package
        self.module = module


class ToBeDoneError(BaseError):
    """something still to be done"""
    def __init__(self, method, module):
        self.method = method
        self.module = module


def make_tbd(method, module='qtip'):
    def tbd():
        raise ToBeDoneError(method, module)
    return tbd
