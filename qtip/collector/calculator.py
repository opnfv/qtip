##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from operator import add

import yaml
from os import path

from qtip.util.logger import QtipLogger

logger = QtipLogger('calculator').get

BASELINE = yaml.safe_load(file(path.join(path.dirname(__file__), 'baseline.yaml')))


def dpi_calculator(samples):
    try:
        float_pps = map(lambda x: float(x), samples['pps'])
        float_bps = map(lambda x: float(x), samples['bps'])
        sum_dpi_pps = reduce(add,
                             map(lambda x: x / 1000 if x > 100 else x, float_pps))
        sum_dpi_bps = reduce(add,
                             map(lambda x: x / 1000 if x > 100 else x, float_bps))

        return {'pps': round(sum_dpi_pps / 10, 3), 'bps': round(sum_dpi_bps / 10, 3)}
    except Exception, error:
        logger.error(error)
        return {'pps': None, 'bps': None}


def calculate_cpu_usage(cpu_idle):
    try:
        cpu_usage = round((100.0 - float(cpu_idle)), 3)
        return '{0}%'.format(str(cpu_usage))
    except Exception as error:
        logger.error(error)
        return None


def calculate_compute_benchmark_index(benchmark, results):
    index = 0
    item_index = []

    if benchmark == 'dhrystone' or benchmark == 'whetstone':
        formated = {'multi_cpus': results['multi_cpus']['score'],
                    'single_cpu': results['single_cpu']['score']}
    else:
        formated = results.copy()

    for item in formated:
        if item in BASELINE['compute'][benchmark]:
            item_index.append(
                float(formated[item]) / BASELINE['compute'][benchmark][item])
    if item_index:
        index = reduce(lambda x, y: x + y, item_index) / float(len(item_index))

    return round(index * 100, 2)
