##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import json
import data.ref_results.suite_result as suite_result
import dashboard.pushtoDB as push_to_db


def dump_suite_result(suite_name):
    return suite_result.get_suite_result(suite_name)


def push_suite_result_to_db(suite_name, test_db_url, installer_type, node_name):
    with open('results/{0}_result.json'.format(suite_name), 'r') as result_file:
        j = json.load(result_file)
        push_to_db.push_results_to_db(test_db_url, '{0}_test_suite'.format(suite_name),
                                      j, installer_type, node_name)
