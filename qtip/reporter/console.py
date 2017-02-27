##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from qtip.base import BaseActor


class ConsoleReporter(BaseActor):
    """
    report benchmark result to console
    """
    def __init__(self, config, parent=None):
        super(ConsoleReporter, self).__init__(config, parent=parent)
        # TODO(yujunz) remove PoC code
        self._fmt = "{title}: {description}"

    def render(self, var_dict):
        return self._fmt.format(**var_dict)
