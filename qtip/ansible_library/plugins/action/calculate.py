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

        with open(self._task.args.get('sysinfo')) as f:
            data = json.load(f)
            sysinfo = dict([(k['name'], data[k['name']][0]) for k in spec['system_info']])

        dest = self._task.args.get('dest')

        baseline_file = self._task.args.get('baseline')
        if baseline_file is not None:
            with open(baseline_file) as f:
                baseline = json.load(f)
                return calc_qpi(spec, metrics, sysinfo, baseline, dest=dest)
        else:
            return calc_qpi(spec, metrics, sysinfo, None, dest=dest)


@export_to_file
def calc_qpi(qpi_spec, metrics, sysinfo, qpi_baseline):
    display.vv("calculate QPI {}".format(qpi_spec['name']))
    display.vvv("spec: {}".format(qpi_spec))
    display.vvv("metrics: {}".format(metrics))
    display.vvv("baseline: {}".format(qpi_baseline))

    section_results = []
    qpi_score = 0
    if qpi_baseline:
        for s in qpi_spec['sections']:
            s_baseline = query(qpi_baseline['sections']).first(
                lambda section: section['name'] == s['name'])
            section_results.append(calc_section(s, metrics, s_baseline))

        # TODO(yujunz): use formula in spec
        qpi_score = int(
            mean([r['score'] for r in section_results]) * qpi_baseline['score'])
    else:
        for s in qpi_spec['sections']:
            section_results.append(calc_section(s, metrics))

    results = {
        'score': qpi_score,
        'name': qpi_spec['name'],
        'description': qpi_spec['description'],
        'system_info': sysinfo,
        'sections': section_results,
        'spec': "https://git.opnfv.org/qtip/tree/resources/QPI/compute.yaml",
        'baseline': "https://git.opnfv.org/qtip/tree/resources/baselines/compute.json"
    }

    return results


def calc_section(section_spec, metrics, section_baseline=None):
    display.vv("calculate section {}".format(section_spec['name']))
    display.vvv("spec: {}".format(section_spec))
    display.vvv("metrics: {}".format(metrics))
    display.vvv("baseline: {}".format(section_baseline))

    metric_results = []
    section_score = 0
    if section_baseline:
        for m in section_spec['metrics']:
            m_baseline = query(section_baseline['metrics']).first(
                lambda metric: metric['name'] == m['name'])
            metric_results.append(calc_metric(m, metrics[m['name']], m_baseline))
        section_score = mean([r['score'] for r in metric_results])
    else:
        for m in section_spec['metrics']:
            metric_results.append(calc_metric(m, metrics[m['name']]))

    # TODO(yujunz): use formula in spec
    return {
        'score': section_score,
        'name': section_spec['name'],
        'description': section_spec.get('description', 'section'),
        'metrics': metric_results
    }


def calc_metric(metric_spec, metrics, metric_baseline=None):
    display.vv("calculate metric {}".format(metric_spec['name']))
    display.vvv("spec: {}".format(metric_spec))
    display.vvv("metrics: {}".format(metrics))
    display.vvv("baseline: {}".format(metric_baseline))

    # TODO(yujunz): use formula in spec
    workload_results = []
    metric_score = 0
    if metric_baseline:
        for w in metric_spec['workloads']:
            w_baseline = query(metric_baseline['workloads']).first(
                lambda workload: workload['name'] == w['name'])
            workload_results.append({
                'name': w['name'],
                'description': 'workload',
                'score': calc_score(metrics[w['name']], w_baseline['baseline']),
                'result': metrics[w['name']][0]
                })
        metric_score = mean([r['score'] for r in workload_results])
    else:
        for w in metric_spec['workloads']:
            workload_results.append({
                'name': w['name'],
                'baseline': metrics[w['name']][0]
            })

    return {
        'score': metric_score,
        'name': metric_spec['name'],
        'description': metric_spec.get('description', 'metric'),
        'workloads': workload_results
    }


def calc_score(metrics, baseline):
    if not isinstance(baseline, numbers.Number):
        baseline = humanfriendly.parse_size(baseline)

    return mean(
        [m if isinstance(m, numbers.Number) else humanfriendly.parse_size(m)
         for m in metrics]) / baseline
