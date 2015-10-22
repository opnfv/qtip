##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################



import os


class Driver:

    def __init__(self):
        print "Class driver initialized\n"

    def drive_bench(self, benchmark, roles):
        result_dir = '$PWD/results'
        benchmark_name = benchmark + '.yaml'
        print roles
        for k, v in roles:
            print k
            run_play = 'ansible-playbook -s $PWD/benchmarks/playbooks/{0} --extra-vars "Dest_dir={1} role={2}" -vvv'.format(
                benchmark_name, result_dir, k)

            status = os.system(run_play)
