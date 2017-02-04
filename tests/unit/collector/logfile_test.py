##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import yaml

from qtip.collector.logfile import SysLogfileCollector


def test_syslogfilecollector_collect(benchmarks_root, external_root):
    plan_config = \
        yaml.safe_load(file(benchmarks_root + "/plan/compute.yaml"))
    collector_config = plan_config['config']['collector'][0]
    log_path = external_root + '/sysinfo'
    sysinfo = \
        SysLogfileCollector(collector_config, log_path).collect()
    assert len(sysinfo) is 14
