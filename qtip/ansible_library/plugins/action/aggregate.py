#!/usr/bin/python

###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from numpy import mean

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get('skipped', False):
            return result

        return aggregate(self._task.args.get('group'), task_vars)


# aggregate QPI results
def aggregate(group, task_vars):
    qpi_results = [task_vars['hostvars'][host]['qpi_result'] for host in task_vars['groups'][group]]
    return {
        'score': int(mean([r['score'] for r in qpi_results])),
        'aggregated': qpi_results
    }
