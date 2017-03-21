##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import httplib

import connexion

from qtip.base import error


def get_one_exceptions(resource):
    def _decorator(func):
        def _execute(name):
            try:
                return func(name), httplib.OK
            except error.NotFoundError:
                return connexion.problem(
                    httplib.NOT_FOUND,
                    '{} Not Found'.format(resource),
                    'Requested {} `{}` not found.'.format(resource, name))
        return _execute
    return _decorator
