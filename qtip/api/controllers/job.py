##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import connexion


def list_jobs():
    return connexion.problem(501,
                             'List jobs',
                             'jobs listing not implemented')


def get_job(job_id):
    return connexion.problem(501,
                             'Get a job',
                             'Job retrieval not implemented')


def job():
    return connexion.problem(501,
                             'start a Job',
                             'Job launch not implemented')
