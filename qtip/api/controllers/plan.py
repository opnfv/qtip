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
from qtip.loader import plan


def list_plans():
    plan_list = list(plan.Plan.list_all())
    return plan_list, httplib.OK


def get_plan(name):
    try:
        plan_spec = plan.Plan(name)
        return {'name': plan_spec.name,
                'abspath': plan_spec.abspath,
                'content': plan_spec.content}, httplib.OK
    except error.NotFoundError:
        return connexion.problem(httplib.NOT_FOUND,
                                 'Plan Not Found',
                                 'requested plan `'+name+'` not found.')


def run_plan(name, action="run"):
    return connexion.problem(httplib.NOT_IMPLEMENTED,
                             'Run a plan',
                             'Plan runner not implemented')
