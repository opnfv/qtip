#!/usr/bin/python

###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from collections import defaultdict
import json
import re

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get('skipped', False):
            return result

        string = self._task.args.get('string')
        patterns = self._task.args.get('patterns')
        export_to = self._task.args.get('export_to')

        return collect(patterns, string, export_to)


def collect(patterns, string, export_to=None):
    """collect all named subgroups of the match into a list keyed by subgroup name
    """
    captured = defaultdict(list)

    if not isinstance(patterns, list):
        patterns = [patterns]

    for p in patterns:
        for match_obj in re.finditer(p, string, re.MULTILINE):
            for (key, value) in match_obj.groupdict().items():
                captured[key].append(value)

    if export_to is not None:
        with open(export_to, 'w+') as f:
            f.write(json.dumps(captured, indent=2))
    return captured
