#!/usr/bin/python

###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import humanfriendly
import json
import numbers
from numpy import mean
import yaml

from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

from qtip.util.export_to import export_to_file


display = Display()


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get('skipped', False):
            return result

        with open(self._task.args.get('spec')) as stream:
            spec = yaml.safe_load(stream)

        metrics_files = self._task.args.get('metrics')
        metrics = {}
        for metric, filename in metrics_files.items():
            with open(filename) as f:
                metrics[metric] = json.load(f)
        dest = self._task.args.get('dest')

        return calc_qpi(spec, metrics, dest=dest)


@export_to_file
def calc_qpi(qpi_spec, metrics):

    display.vv("calculate QPI {}".format(qpi_spec['name']))
    display.vvv("spec: {}".format(qpi_spec))
    display.vvv("metrics: {}".format(metrics))

    section_results = [calc_section(s, metrics)
                       for s in qpi_spec['sections']]

    # TODO(yujunz): use formula in spec
    standard_score = 2048
    qpi_score = int(mean([r['score'] for r in section_results]) * standard_score)

    results = {
        'score': qpi_score,
        'name': qpi_spec['name'],
        'description': qpi_spec['description'],
        'children': section_results,
        'details': {
            'metrics': metrics,
            'spec': "https://git.opnfv.org/qtip/tree/resources/QPI/compute.yaml"
        }
    }

    return results


def calc_section(section_spec, metrics):

    display.vv("calculate section {}".format(section_spec['name']))
    display.vvv("spec: {}".format(section_spec))
    display.vvv("metrics: {}".format(metrics))

    metric_results = [calc_metric(m, metrics[m['name']])
                      for m in section_spec['metrics']]
    # TODO(yujunz): use formula in spec
    section_score = mean([r['score'] for r in metric_results])
    return {
        'score': section_score,
        'name': section_spec['name'],
        'description': section_spec.get('description', 'section'),
        'children': metric_results
    }


def calc_metric(metric_spec, metrics):

    display.vv("calculate metric {}".format(metric_spec['name']))
    display.vvv("spec: {}".format(metric_spec))
    display.vvv("metrics: {}".format(metrics))

    # TODO(yujunz): use formula in spec
    workload_results = [{'name': w['name'],
                         'description': 'workload',
                         'score': calc_score(metrics[w['name']], w['baseline'])}
                        for w in metric_spec['workloads']]
    metric_score = mean([r['score'] for r in workload_results])
    return {
        'score': metric_score,
        'name': metric_spec['name'],
        'description': metric_spec.get('description', 'metric'),
        'children': workload_results
    }


def calc_score(metrics, baseline):
    if not isinstance(baseline, numbers.Number):
        baseline = humanfriendly.parse_size(baseline)

    return mean([m if isinstance(m, numbers.Number) else humanfriendly.parse_size(m)
                 for m in metrics]) / baseline
