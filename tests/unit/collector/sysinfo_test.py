##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from os import path

from qtip.collector.sysinfo import SysInfo


def test_parser_sysinfo():
    log_path = path.join(path.dirname(__file__), path.pardir, path.pardir,
                         'data', 'external', 'sysinfo')
    sysinfo = SysInfo()
    sysinfo.parser_sysinfo(log_path)
    assert path.isfile(log_path + '/sysinfo.json')
