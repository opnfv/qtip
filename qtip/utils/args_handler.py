##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
from operator import add
import simplejson as json
from env_setup import Env_setup
from spawn_vm import SpawnVM
from driver import Driver


def get_files_in_suite(suite_name, case_type='all'):
    benchmark_list = json.load(file('benchmarks/suite/{0}'.format(suite_name)))
    return reduce(add, benchmark_list.values()) \
        if case_type == 'all' else benchmark_list[case_type]


def get_files_in_test_plan(lab, suite_name, case_type='all'):
    test_case_all = os.listdir('./test_plan/{0}/{1}'.format(lab, suite_name))
    return test_case_all if case_type == 'all' else \
        filter(lambda x: case_type in x, test_case_all)


def get_benchmark_path(lab, suit, benchmark):
    return './test_plan/{0}/{1}/{2}'.format(lab, suit, benchmark)


def check_suite(suite_name):
    return True if os.path.isfile('benchmarks/suite/' + suite_name) else False


def check_lab_name(lab_name):
    return True if os.path.isdir('test_plan/' + lab_name) else False


def check_benchmark_name(lab, file, benchmark):
    return os.path.isfile('test_plan/' + lab + '/' + file + '/' + benchmark)


def _get_f_name(test_case_path):
    return test_case_path.split('/')[-1]


def prepare_ansible_env(benchmark_test_case):
    env_setup = Env_setup()
    [benchmark, vm_info, benchmark_details, proxy_info] = env_setup.parse(benchmark_test_case)
    SpawnVM(vm_info) if len(vm_info) else None
    env_setup.call_ping_test()
    env_setup.call_ssh_test()
    env_setup.update_ansible()
    return benchmark, benchmark_details, proxy_info, env_setup


def run_benchmark(installer_type, pwd, benchmark, benchmark_details,
                  proxy_info, env_setup, benchmark_test_case):
    driver = Driver()
    result = driver.drive_bench(installer_type, pwd, benchmark,
                                env_setup.roles_dict.items(),
                                _get_f_name(benchmark_test_case),
                                benchmark_details, env_setup.ip_pw_dict.items(), proxy_info)
    env_setup.cleanup_authorized_keys()
    return result


def prepare_and_run_benchmark(installer_type, pwd, benchmark_test_case):
    benchmark, benchmark_details, proxy_info, env_setup = prepare_ansible_env(benchmark_test_case)
    return run_benchmark(installer_type, pwd, benchmark, benchmark_details,
                         proxy_info, env_setup, benchmark_test_case)
