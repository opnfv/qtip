##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.base.constant import PkgName, PropName
from qtip.base.error import NotFound
from qtip.collector.stdout import StdoutCollector
from qtip.driver.random import RandomDriver
from qtip.loader.base import BaseLoader
from qtip.reporter.console import ConsoleReporter


class BaseRunner(BaseLoader):
    def __init__(self, name, paths=None, config=None):
        super(BaseRunner, self).__init__(name, paths=paths)
        if config is None:
            config = self.content[PropName.CONFIG]

        driver_name = config[PropName.DRIVER]
        collector_name = config[PropName.COLLECTOR]
        reporter_name = config[PropName.REPORTER]

        # TODO(yujunz) dynamically load modules by name

        if driver_name == 'random':
            self.driver = RandomDriver()
        else:
            raise NotFound(driver_name, package=PkgName.DRIVER)

        if collector_name == 'stdout':
            self.collector = StdoutCollector()
        else:
            raise NotFound(collector_name,
                           package=PkgName.COLLECTOR)

        if reporter_name == 'console':
            self.reporter = ConsoleReporter()
        else:
            raise NotFound(reporter_name,
                           package=PkgName.REPORTER)
