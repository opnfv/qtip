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
    section_scores = {section['name']: calc_section_score(section, metrics) for section in qpi_spec['sections']}
    # TODO(yujunz): use formula in spec
    qpi_score = mean(section_scores)
    return {
        'spec': qpi_spec,
        'score': qpi_score,
        'section_scores': section_scores,
        'metrics': metrics
    }


def calc_section_score(section_spec, metrics):
    metric_scores = {metric_spec['name']: calc_metric_score(metric_spec, metrics[metric_spec['name']])
                     for metric_spec in section_spec['metrics']}
    # TODO(yujunz): use formula in spec
    section_score = mean(metric_scores)
    return {
        'spec': section_spec,
        'score': section_score,
        'metric_scores': metric_scores
    }


def calc_metric_score(metric_spec, metrics):
    # TODO(yujunz): use formula in spec
    workload_scores = {name: mean(metrics[name]) / baseline for (name, baseline) in metric_spec['workloads'].items()}
    metric_score = mean(workload_scores.values())
    return {
        'spec': metric_spec,
        'score': metric_score,
        'workload_scores': workload_scores
    }
