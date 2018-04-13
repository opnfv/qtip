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


def result_concat(targ_dir):
    list_vm = []
    list_bm = []
    diction = {}

    for file in os.listdir(targ_dir):
        if file.endswith(".json"):
            if file.startswith("instance"):
                print str(file)
                list_vm.append(file)
            else:
                list_bm.append(file)
    l = len(list_bm)
    k = len(list_vm)

    for x in range(0, l):
        file_t = list_bm[x]
        with open(targ_dir + file_t) as result_file:
            result_djson = json.load(result_file)
            diction['Baremetal' + str(int(x + 1))] = result_djson

    for x in range(0, k):
        file_t = list_vm[x]
        with open(targ_dir + file_t) as result_file:
            result_djson = json.load(result_file)
            diction['Virtual Machine ' + str(x + 1)] = result_djson
    return diction
