##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
from os import path
import re
import yaml


RESOURCE_ROOT = path.join(path.dirname(__file__), '..', 'resources')


def normalize(score, base=2048):
    """ Use 2048 as base score if the performance equals baseline  """
    return int(base * score)


def storperf(report_file, qpi_spec=None, baseline_file=None):
    if qpi_spec is None:
        qpi_spec = path.join(RESOURCE_ROOT, 'QPI', 'storage.yaml')

    with open(qpi_spec) as f:
        # load QPI spec as base template for report
        qpi_report = yaml.safe_load(f.read())

    if baseline_file is None:
        baseline_file = path.join(RESOURCE_ROOT, 'baselines', 'storage.json')

    with open(baseline_file) as f:
        baseline_report = json.load(f)
        baseline_metrics = baseline_report['report']['metrics']

    with open(report_file) as f:
        storperf_report = json.load(f)
        reported_metrics = storperf_report['report']['metrics']

    sections = qpi_report['sections']
    for section in sections:
        section_regex = re.compile(section['regex'])
        ignored_regex = re.compile('^_')  # ignore metrics starting with '_"
        valid_metrics = [k for k in reported_metrics
                         if section_regex.search(k) and not ignored_regex.search(k) and k in baseline_metrics and
                         reported_metrics[k] != 0 and baseline_metrics[k] != 0]
        if len(valid_metrics) == 0:
            raise Exception('No valid metrics found')

        section['score'] = sum([reported_metrics[k] / baseline_metrics[k]
                                if not section.get('use_reciprocal', False)
                                else baseline_metrics[k] / reported_metrics[k]
                                for k in valid_metrics]) / len(valid_metrics)
    qpi_report['score'] = normalize(sum([section['score'] for section in sections]) / len(sections))

    return qpi_report
