##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import yaml
import sys
from func.baremetal_setup import Baremetal
from func.virtual_setup import Virtual
from func.driver import Driver


def get_files_in_test_list(suit_name):
    with open('test_list/' + suit_name, 'r') as fin_put:
        benchmark_list = fin_put.readlines()
        return map(lambda x: x.rstrip(), benchmark_list)


def get_files_in_test_case(lab, suit_name):
    return os.listdir('./test_cases/{0}/{1}'.format(lab, suit_name))


def get_benchmark_path(lab, suit, benchmark):
    return './test_cases/{0}/{1}/{2}'.format(lab, suit, benchmark)


def check_suit_in_test_list(suit_name):
    return True if os.path.isfile('test_list/' + suit_name) else False


def check_lab_name(lab_name):
    return True if os.path.isdir('test_cases/' + lab_name) else False


def _get_f_name(test_case_path):
    return test_case_path.split('/')[-1]


def setup_test_env(config_file):
    try:
        f_name = open(config_file, 'r+')
        doc = yaml.load(f_name)
        f_name.close()
    except KeyboardInterrupt:
        print 'ConfigFile Closed: exiting!'
        sys.exit(0)
    if doc['Context']['Virtual_Machines']:
        virtual_env = Virtual(doc)
        return virtual_env
    elif doc['Context']['Host_Machines']:
        bare_env = Baremetal(doc)
        return bare_env
    else:
        raise RuntimeError("%s miss Keyword Virtual_Machines or Host_Machines" % config_file)


def prepare_ansible_env(benchmark_test_case):
    env = setup_test_env(benchmark_test_case)
    env.setup()
    [benchmark, benchmark_details, proxy_info] = env.handle_args()
    env.call_ping_test()
    env.call_ssh_test()
    env.update_ansible()
    return benchmark, benchmark_details, proxy_info, env


def run_benchmark(benchmark, benchmark_details, proxy_info, env_setup, benchmark_test_case):
    driver = Driver()
    driver.drive_bench(benchmark, env_setup.roles_dict.items(), _get_f_name(benchmark_test_case),
                       benchmark_details, env_setup.ip_pw_dict.items(), proxy_info)


def prepare_and_run_benchmark(benchmark_test_case):
    print "-----------------------------------------------"
    print "benchmark_test_case: %s" % benchmark_test_case
    benchmark, benchmark_details, proxy_info, env_setup = prepare_ansible_env(benchmark_test_case)
    run_benchmark(benchmark, benchmark_details, proxy_info, env_setup, benchmark_test_case)
    cleanup_env(env_setup)


def cleanup_env(env):
    env.cleanup()
