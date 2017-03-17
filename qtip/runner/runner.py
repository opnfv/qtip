##############################################################################
# Copyright (c) 2017 ZTE corp. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import os
from os import path
import sys
import time

from qtip.collector.parser import grep
from qtip.driver.ansible_driver import AnsibleDriver
from qtip.util.logger import QtipLogger

logger = QtipLogger('runner').get

ALL_BENCHMARKS = ['dpi', 'ramspeed', 'ssl', 'dhrystone', 'whetstone']


def run_benchmark(result_dir, benchmarks):
    if not path.isdir(result_dir):
        os.makedirs(result_dir)
    driver = AnsibleDriver({'args': {'result_dir': result_dir}})
    driver.pre_run()
    result = driver.run(benchmarks)
    driver.cleanup()
    return result


def generate_report(result_dir, start_time, stop_time):
    output = {
        "plan_name": "compute_qpi",
        "start_time": start_time,
        "stop_time": stop_time,
        "sut": []
    }
    output.update(parse_result(result_dir))
    output.update({'stop_time': stop_time})
    with open('{0}/result.json'.format(result_dir), 'w+') as f:
        json.dump(output, f, indent=4, sort_keys=True)


def parse_result(result_dir):
    sut_template = {'sut': []}
    nodes_list = os.listdir(result_dir)
    for node in nodes_list:
        node_output_template = {
            'name': node,
            'type': 'baremetal',
            'qpis': []
        }
        qpi_result = {'name': 'compute_qpi', 'benchmarks': []}
        for benchmark in os.listdir('{0}/{1}'.format(result_dir, node)):
            benchmark_result = \
                grep.parse_benchmark_result(
                    '{0}/{1}/{2}'.format(result_dir, node, benchmark))
            qpi_result['benchmarks'].append(benchmark_result)
        node_output_template['qpis'].append(qpi_result)
        sut_template['sut'].append(node_output_template)
    return sut_template


def execute(benchmark):

    dest = path.join(path.dirname(__file__), path.pardir, path.pardir,
                     'collector')

    if not path.isdir(str(dest)):
        logger.error("The destination {0} you give doesn't exist. "
                     "Please check!".format(dest))
        sys.exit(1)

    if benchmark == 'all':
        benchmark = ALL_BENCHMARKS
    elif benchmark not in ALL_BENCHMARKS:
        logger.error("Please check benchmarks name. The supported benchmarks are"
                     "{0}".format(ALL_BENCHMARKS))
    logger.info("Start to run benchmark test: {0}.".format(benchmark))

    benchmark = [benchmark]
    start_time = time.strftime("%Y-%m-%d-%H-%M")
    logger.info("start_time: {0}".format(start_time))
    if not dest.endswith('/'):
        dest += '/'
    result_dir = dest + start_time
    ansible_result = run_benchmark(result_dir, benchmark)
    stop_time = time.strftime("%Y-%m-%d-%H-%M")
    logger.info("stop_time: {0}".format(stop_time))
    if not ansible_result:
        logger.error("Bechmarks run failed. Cann't generate any report.")
        sys.exit(1)
    generate_report(result_dir, start_time, stop_time)
