##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


class QtipError(Exception):
    pass


class InvalidFormat(QtipError):
    def __init__(self, filename):
        self.filename = filename


class NotFound(QtipError):
    def __init__(self, needle, heystack='qtip'):
        self.heystack = heystack
        self.needle = needle

    def __str__(self):
        return self.__dict__


class ToBeDoneError(QtipError):
    """something still to be done"""
    def __init__(self, method, module):
        self.method = method
        self.module = module


def make_tbd(method, module='qtip'):
    def tbd():
        raise ToBeDoneError(method, module)
    return tbd
