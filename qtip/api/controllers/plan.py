##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import connexion


def list_plans():
    return connexion.problem(501,
                             'List plans',
                             'Plans listing not implemented')


def get_plan(plan_name):
    return connexion.problem(501,
                             'Get a plan',
                             'Plan retrieval not implemented')


def run_plan(plan_name, action="run"):
    return connexion.problem(501,
                             'Run a plan',
                             'Plan runner not implemented')