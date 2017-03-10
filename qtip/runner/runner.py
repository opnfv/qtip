##############################################################################
# Copyright (c) 2017 ZTE corp. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import argparse
import json
import os
from os import path
import sys
import time

from qtip.collector.parser import grep
from qtip.driver.ansible_driver import AnsibleDriver
from qtip.util.logger import QtipLogger

logger = QtipLogger('runner').get


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dest', required=True,
                        help='the destination where results will be stored.')

    return parser.parse_args(args)


def run(result_dir, benchmarks):
    if not path.isdir(result_dir):
        os.makedirs(result_dir)
    driver = AnsibleDriver({'args': {'result_dir': result_dir}})
    driver.pre_run()
    return driver.run(benchmarks)


def generate_report_data(result_dir):
    sut_template = {'sut': []}
    nodes_list = os.listdir(result_dir)
    for node in nodes_list:
        node_output_template = {
            'name': node,
            'type': 'baremetal',
            'qpis': [
                {
                    'name': 'compute_qpi',
                    'benchmarks': []
                }
            ]
        }
        node_dirpath = '{0}/{1}'.format(result_dir, node)
        benchmarks = os.listdir(node_dirpath)
        for benchmark in benchmarks:
            benchmark_dirpath = '{0}/{1}'.format(node_dirpath, benchmark)
            benchmark_data = grep.parse_benchmark_result(benchmark_dirpath)
            node_output_template['qpis'][0]['benchmarks'].append(benchmark_data)
        sut_template['sut'].append(node_output_template)
    print sut_template
    return sut_template


def main(args=sys.argv[1:]):
    args = parse_args(args)
    if not path.isdir(str(args.dest)):
        logger.error("The destination {0} you give doesn't exist. "
                     "Please check!".format(args.dest))
        sys.exit(1)
    benchmarks = ['dpi', 'ramspeed', 'ssl', 'dhrystone', 'whetstone']
    logger.info("Start to run compute QPI which include {0}.".format(benchmarks))
    start_time = time.strftime("%Y-%m-%d-%H-%M")
    logger.info("start_time: {0}".format(start_time))
    output = {
        "plan_name": "compute_qpi",
        "start_time": start_time,
        "sut": []
    }
    result_dir = args.dest + start_time
    ansible_result = run(result_dir, benchmarks)
    stop_time = time.strftime("%Y-%m-%d-%H-%M")
    logger.info("stop_time: {0}".format(stop_time))
    if ansible_result:
        output.update(generate_report_data(result_dir))
    else:
        logger.error("The execution of this paln is failed. "
                     "Cann't generate any report.")
        sys.exit(1)
    output.update({'stop_time': stop_time})
    with open('{0}/report.json'.format(result_dir), 'w+') as f:
        json.dump(output, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
