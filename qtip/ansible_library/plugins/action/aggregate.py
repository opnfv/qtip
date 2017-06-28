#!/usr/bin/python

###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
from numpy import mean
import os

from ansible.plugins.action import ActionBase

from qtip.util.export_to import export_to_file


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get('skipped', False):
            return result

        basepath = self._task.args.get('basepath')

        return aggregate(
            hosts=task_vars['groups'][self._task.args.get('group')],
            basepath=basepath,
            src=self._task.args.get('src'),
            dest=os.path.join(basepath, self._task.args.get('dest'))
        )


# aggregate QPI results
@export_to_file
def aggregate(hosts, basepath, src):
    host_results = []
    for host in hosts:
        host_result = json.load(open(os.path.join(basepath, host, src)))
        host_result['name'] = host
        host_results.append(host_result)
    score = int(mean([r['score'] for r in host_results]))
    return {
        'score': score,
        'name': 'compute',
        'description': 'POD Compute QPI',
        'nodes': host_results
    }
