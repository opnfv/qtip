##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from qtip.collector.logfile import LogfileCollector


# TODO(yujunz) more elegant way to load module dynamically
def load_collector(type_name):
    if type_name == LogfileCollector.TYPE:
        return LogfileCollector
    else:
        raise Exception("Invalid collector type: {}".format(type_name))
