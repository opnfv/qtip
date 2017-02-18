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


def report_concat(targ_dir, testcase):
    machine_temp = []
    machines = []

    for file in os.listdir(targ_dir):
        if file.endswith(".json"):
            machine_temp.append(file)

    l = len(machine_temp)

    for x in range(0, l):
        file_t = machine_temp[x]
        with open(targ_dir + file_t) as result_file:
            result_djson = json.load(result_file)
            if result_djson['1  Testcase Name'] == str(testcase):
                machines.append(result_djson)
    return machines


def space_count(l):
    spc = ''
    for x in range(l):
        spc = spc + ' '
    return spc


def custom_dict(list1, list2, k):
    string_1 = ''
    for num_1 in range(0, len(list1)):
        string_1 = string_1 + space_count(k) + str(list1[num_1][0]) + "=" + str(list2[num_1]) + "\n"
    return string_1


def generate_result(dict_a, k):
    list_1 = []
    list_2 = []
    count = 0
    for i, j in sorted(dict_a.iteritems()):
        list_1.append([])
        list_1[count].append(i)
        if (str(type(dict_a.get(i)))) == "<type 'dict'>":
            list_2.append(str("\n" + generate_result(dict_a.get(i), int(k + 1))))
        else:
            list_2.append(dict_a.get(i))
        count = count + 1
    return custom_dict(list_1, list_2, k)
