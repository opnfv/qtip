##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import json


def get_index(suite):
    with open('../../results/' + suite + '.json') as result_file:
        result_djson = json.load(result_file)
        index = result_djson['index']
    return index
