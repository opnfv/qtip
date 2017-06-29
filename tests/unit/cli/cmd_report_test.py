###############################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from qtip.cli.commands import cmd_report as report


def test_dhrystone(aggregated_report):
    """Test report"""

    result = report.display_report(aggregated_report, 'ssl', 'compute')
    assert result['ss'] == 1.0
    assert result['desc'] == 'cryptography and SSL/TLS performance'
