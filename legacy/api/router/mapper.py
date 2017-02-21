##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from legacy.api.handler.job_handler import Job, JobList


mappers = [
    (JobList, '/api/v1.0/jobs'),
    (Job, '/api/v1.0/jobs/<string:id>'),
]
