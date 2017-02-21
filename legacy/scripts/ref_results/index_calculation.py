##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import json


def compute_index(total_measured, ref_result, count):
    try:
        average = float(total_measured / count)

    except ZeroDivisionError:
        average = 0
    index = average / ref_result
    return index


def get_reference(*args):

    with open('scripts/ref_results/reference.json') as reference_file:
        reference_djson = json.load(reference_file)
        for arg in args:
            ref_n = reference_djson.get(str(arg))
            reference_djson = reference_djson.get(str(arg))
    return ref_n


def generic_index(dict_gen, testcase, reference_num, *args):
    c = len(args)
    count = 0
    total = 0
    result = 0
    for k, v in dict_gen.iteritems():
        dict_temp = dict_gen[k]
        if dict_gen[k]['name'] == '{0}.yaml'.format(testcase):
            count = count + 1
            for arg in args:
                if arg == args[c - 1]:
                    try:
                        result = float(dict_temp.get(str(arg)))
                    except ValueError:
                        result = float(dict_temp.get(str(arg))[:-1]) * 1000
                dict_temp = dict_temp.get(str(arg))
            total = total + result
    return compute_index(total, reference_num, count)
