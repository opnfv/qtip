##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.base.constant import PkgName, BaseProp
from qtip.base.error import NotFoundError
from qtip.collector.stdout import StdoutCollector
from qtip.driver.random import RandomDriver
from qtip.reporter.console import ConsoleReporter


class Runner(object):
    def __init__(self, spec, config=None):
        if config is None:
            config = spec[BaseProp.CONFIG]

        driver_name = config[BaseProp.DRIVER]
        collector_name = config[BaseProp.COLLECTOR]
        reporter_name = config[BaseProp.REPORTER]

        # TODO(yujunz) dynamically load modules by name

        if driver_name == 'random':
            self.driver = RandomDriver()
        else:
            raise NotFoundError(driver_name, heystack=PkgName.DRIVER)

        if collector_name == 'stdout':
            self.collector = StdoutCollector()
        else:
            raise NotFoundError(collector_name,
                                heystack=PkgName.COLLECTOR)

        if reporter_name == 'console':
            self.reporter = ConsoleReporter()
        else:
            raise NotFoundError(reporter_name,
                                heystack=PkgName.REPORTER)
