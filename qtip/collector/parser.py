##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import re


class Parser(object):
    @staticmethod
    def grep(filename, regex=None, group='group'):
        # TODO(yujunz) extend to multiple groups
        with open(filename) as f:
            for line in f:
                match = re.search(regex, line)
                if match:
                    return {group: match.group(1)}


class ParserType(object):
    GREP = 'grep'
