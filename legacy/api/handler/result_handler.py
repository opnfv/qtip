##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import importlib
import json
from os.path import expanduser

import qtip.utils.dashboard.pushtoDB as push_to_db
from qtip.utils import logger_utils

logger = logger_utils.QtipLogger('suite_result').get


def get_benchmark_result(benchmark_name, suite_name):
    benchmark_indices = importlib.import_module('scripts.ref_results'
                                                '.{0}_benchmarks_indices'.format(suite_name))
    methodToCall = getattr(benchmark_indices, '{0}_index'.format(benchmark_name))
    return methodToCall()


def dump_suite_result(suite_name):
    suite_dict = {}
    suite_bench_list = {'compute': ['DPI', 'Dhrystone', 'Whetstone', 'SSL', 'RamSpeed'],
                        'storage': ['FIO'],
                        'network': ['IPERF']}
    temp = 0
    l = len(suite_bench_list[suite_name])
    for benchmark in suite_bench_list[suite_name]:
        try:
            suite_dict[benchmark] = get_benchmark_result(benchmark.lower(), suite_name)
            temp = temp + float(suite_dict[benchmark]['index'])
        except OSError:
            l = l - 1
            pass

    if l == 0:
        logger.info("No {0} suite results found".format(suite_name))
        return False
    else:
        suite_index = temp / l
        suite_dict_f = {'index': suite_index,
                        'suite_results': suite_dict}
        result_path = expanduser('~') + '/qtip/results'
        with open('{0}/{1}_result.json'.format(result_path, suite_name), 'w+') as result_json:
            json.dump(suite_dict_f, result_json, indent=4, sort_keys=True)
        return True


def push_suite_result_to_db(suite_name, test_db_url, installer_type, node_name):
    with open('results/{0}_result.json'.format(suite_name), 'r') as result_file:
        j = json.load(result_file)
        push_to_db.push_results_to_db(test_db_url, '{0}_test_suite'.format(suite_name),
                                      j, installer_type, node_name)
