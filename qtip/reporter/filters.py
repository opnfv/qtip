###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


def justify(pair, width=100, padding_with='.'):
    """align first element along the left margin, second along the right, padding spaces"""
    n = width - len(pair[0])
    return '{key}{value:{c}>{n}}'.format(key=pair[0], value=pair[1], c=padding_with, n=n)
