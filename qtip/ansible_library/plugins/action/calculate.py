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

        spec = self._task.args.get('spec')
        metrics = self._task.args.get('metrics')

        return calc_qpi(spec, metrics)


def calc_qpi(qpi_spec, metrics):
    section_results = [{'name': s['name'], 'result': calc_section(s, metrics)}
                       for s in qpi_spec['sections']]
    # TODO(yujunz): use formula in spec
    qpi_score = mean([r['result']['score'] for r in section_results])
    return {
        'spec': qpi_spec,
        'score': qpi_score,
        'section_results': section_results,
        'metrics': metrics
    }


def calc_section(section_spec, metrics):
    metric_results = [{'name': m['name'], 'result': calc_metric(m, metrics[m['name']])}
                      for m in section_spec['metrics']]
    # TODO(yujunz): use formula in spec
    section_score = mean([r['result']['score'] for r in metric_results])
    return {
        'score': section_score,
        'metric_results': metric_results
    }


def calc_metric(metric_spec, metrics):
    # TODO(yujunz): use formula in spec
    workload_results = [{'name': w['name'], 'score': mean(metrics[w['name']]) / w['baseline']}
                        for w in metric_spec['workloads']]
    metric_score = mean([r['score'] for r in workload_results])
    return {
        'score': metric_score,
        'workload_results': workload_results
    }
