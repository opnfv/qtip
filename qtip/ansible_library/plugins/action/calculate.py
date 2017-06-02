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
import numbers

from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from asq.initiators import query
import humanfriendly
from numpy import mean
import yaml

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

        baseline_file = self._task.args.get('baseline')
        if baseline_file is not None:
            with open(baseline_file) as f:
                baseline = json.load(f)
                return calc_qpi(spec, metrics, baseline, dest=dest)
        else:
            return save_as_baseline(spec, metrics, dest=dest)


# TODO(wuzhihui): It is more reasonable to put this function into collect.py.
# For now metrics data is not easy to be collected from collect.py.
@export_to_file
def save_as_baseline(qpi_spec, metrics):
    display.vv("save {} metrics as baseline".format(qpi_spec['name']))
    display.vvv("spec: {}".format(qpi_spec))
    display.vvv("metrics: {}".format(metrics))

    return {
        'name': qpi_spec['name'],
        'score': 2048,
        'description': qpi_spec['description'],
        'details': {
            'metrics': metrics,
            'spec': "https://git.opnfv.org/qtip/tree/resources/QPI/compute.yaml",
            'baseline': ""
        }
    }


@export_to_file
def calc_qpi(qpi_spec, metrics, qpi_baseline):
    display.vv("calculate QPI {}".format(qpi_spec['name']))
    display.vvv("spec: {}".format(qpi_spec))
    display.vvv("metrics: {}".format(metrics))
    display.vvv("baseline: {}".format(qpi_baseline))

    section_results = []
    for s in qpi_spec['sections']:
        s_baseline = query(qpi_baseline['sections']).first(
            lambda section: section['name'] == s['name'])
        section_results.append(calc_section(s, metrics, s_baseline))

    # TODO(yujunz): use formula in spec
    qpi_score = int(
        mean([r['score'] for r in section_results]) * qpi_baseline['score'])

    results = {
        'score': qpi_score,
        'name': qpi_spec['name'],
        'description': qpi_spec['description'],
        'children': section_results,
        'details': {
            'metrics': metrics,
            'spec': "https://git.opnfv.org/qtip/tree/resources/QPI/compute.yaml",
            'baseline': "https://git.opnfv.org/qtip/tree/resources/QPI/compute-baseline.json"
        }
    }

    return results


def calc_section(section_spec, metrics, section_baseline):
    display.vv("calculate section {}".format(section_spec['name']))
    display.vvv("spec: {}".format(section_spec))
    display.vvv("metrics: {}".format(metrics))
    display.vvv("baseline: {}".format(section_baseline))

    metric_results = []
    for m in section_spec['metrics']:
        m_baseline = query(section_baseline['metrics']).first(
            lambda metric: metric['name'] == m['name'])
        metric_results.append(calc_metric(m, metrics[m['name']], m_baseline))

    # TODO(yujunz): use formula in spec
    section_score = mean([r['score'] for r in metric_results])
    return {
        'score': section_score,
        'name': section_spec['name'],
        'description': section_spec.get('description', 'section'),
        'children': metric_results
    }


def calc_metric(metric_spec, metrics, metric_basline):
    display.vv("calculate metric {}".format(metric_spec['name']))
    display.vvv("spec: {}".format(metric_spec))
    display.vvv("metrics: {}".format(metrics))
    display.vvv("baseline: {}".format(metric_basline))

    # TODO(yujunz): use formula in spec
    workload_results = []
    for w in metric_spec['workloads']:
        w_baseline = query(metric_basline['workloads']).first(
            lambda workload: workload['name'] == w['name'])
        workload_results.append({
            'name': w['name'],
            'description': 'workload',
            'score': calc_score(metrics[w['name']], w_baseline['baseline'])
        })

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

    return mean(
        [m if isinstance(m, numbers.Number) else humanfriendly.parse_size(m)
         for m in metrics]) / baseline
