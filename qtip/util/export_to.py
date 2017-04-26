##############################################################################
# Copyright (c) 2017 ZTE and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json


def export_to_file(func):
    def func_wrapper(*args, **kwargs):
        dest = kwargs.pop('dest', None)
        content = func(*args, **kwargs)
        if dest is not None:
            with open(dest, 'w+') as f:
                f.write(json.dumps(content, indent=2))
        return content
    return func_wrapper
