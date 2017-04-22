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
import os
import re

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get('skipped', False):
            return result

        string = self._task.args.get('string')
        patterns = self._task.args.get('patterns')

        dump = self._task.args.get('dump')
        if dump is not None:
            root = task_vars.get('qtip_results', 'results')
            base = task_vars.get('dump_base', 'dump')
            dump_facts([{'name': dump, 'content': string}], root, base)

        return collect(patterns, string)


def collect(patterns, string):
    """collect all named subgroups of the match into a list keyed by subgroup name
    """
    captured = defaultdict(list)

    if not isinstance(patterns, list):
        patterns = [patterns]

    for p in patterns:
        for match_obj in re.finditer(p, string, re.MULTILINE):
            for (key, value) in match_obj.groupdict().items():
                captured[key].append(value)

    return captured


def dump_facts(facts, root, base):
    dest = os.path.join(root, base)
    if not os.path.exists(dest):
        os.makedirs(dest)
    return [{'name': fact['name'], 'result': open(os.path.join(dest, fact['name']), 'w+').write(fact['content'])}
            for fact in facts]
