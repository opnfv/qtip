##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import httplib

import connexion

from qtip.base import error


def check_resource(resource):
    def _decorator(func):
        def _execute(name):
            try:
                return func(name), httplib.OK
            except error.NotFoundError:
                return connexion.problem(
                    httplib.NOT_FOUND,
                    '{} not found'.format(resource),
                    'Requested {} `{}` not found.'.format(resource.lower(), name))
        return _execute
    return _decorator


def check_implemented(resource):
    def _decorator(func):
        def _execute(name):
            try:
                return func(name), httplib.OK
            except error.NotFoundError:
                return connexion.problem(
                    httplib.NOT_FOUND,
                    '{} not found'.format(resource),
                    'Requested {} `{}` not found.'.format(resource.lower(), name))
        return _execute
    return _decorator