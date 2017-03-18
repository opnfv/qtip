##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import httplib

from qtip.api.controllers import common
from qtip.base import error
from qtip.loader import plan


def list_plans():
    plans = list(plan.Plan.list_all())
    plans_by_name = [p['name'] for p in plans]
    return {'plans': plans_by_name}, httplib.OK


@common.check_endpoint_for_error(resource='Plan')
def get_plan(name):
    plan_spec = plan.Plan(name)
    return plan_spec.content


@common.check_endpoint_for_error(resource='Plan', operation='Run')
def run_plan(name, action="run"):
    raise error.ToBeDoneError('run_plan', 'plan')
