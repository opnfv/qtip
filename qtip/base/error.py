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


class InvalidContentError(BaseError):
    def __init__(self, filename, excinfo=None):
        self.filename = filename
        self.excinfo = excinfo
        self.message = "Invalid content in {0}".format(filename)


class NotFoundError(BaseError):
    def __init__(self, needle, heystack='qtip'):
        self.needle = needle
        self.heystack = heystack
        self.message = "{0} not found in {1}".format(needle[0:-5], heystack)


class ToBeDoneError(BaseError):
    """something still to be done"""
    def __init__(self, method, module):
        self.method = method
        self.module = module
