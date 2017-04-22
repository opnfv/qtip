###############################################################
# Copyright (c) 2017 ZTE Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


def _justify_pair(pair, width=80, padding_with='.'):
    """align first element along the left margin, second along the right, padding spaces"""
    n = width - len(pair[0])
    return '{key}{value:{c}>{n}}'.format(key=pair[0], value=pair[1], c=padding_with, n=n)


def justify(content, width=80, padding_with='.'):
    if isinstance(content, list):
        return '\n'.join([justify(item, width, padding_with) for item in content])
    elif isinstance(content, dict):
        return '\n'.join([justify(item, width, padding_with) for item in content.items()])
    else:
        return _justify_pair(content, width, padding_with)
