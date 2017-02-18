##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import json
import pickle

total_cpu = os.popen(
    "cat $HOME/tempT/UnixBench/results/* | grep 'of tests' | awk '{print $1;}' | awk 'NR==1'").read().rstrip()

cpu_1 = os.popen(
    "cat $HOME/tempT/UnixBench/results/* | grep 'of tests' | awk '{print $6;}' | awk 'NR==1'").read().rstrip()


cpu_2 = os.popen(
    "cat $HOME/tempT/UnixBench/results/* | grep 'of tests' | awk '{print $6;}' | awk 'NR==2'").read().rstrip()


index_1 = os.popen(
    "cat $HOME/tempT/UnixBench/results/* | grep 'Index Score (Partial Only)  ' | awk '{print $7;}' | awk 'NR==1'").read().rstrip()
index_2 = os.popen(
    "cat $HOME/tempT/UnixBench/results/* | grep 'Index Score (Partial Only)  ' | awk '{print $7;}' | awk 'NR==2'").read().rstrip()


result = {"n_cpu": total_cpu,
          "single": {"n_para_test": cpu_1,
                     "score": index_1},
          "multi": {"n_para_test": cpu_2,
                    "score": index_2}
          }

with open('result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)
print json.dumps(result, indent=4, sort_keys=True)
# print result.items()
