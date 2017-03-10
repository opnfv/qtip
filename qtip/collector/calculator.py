##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from operator import add

from qtip.util.logger import QtipLogger

logger = QtipLogger('calculator').get


def dpi_calculator(samples):
    try:
        float_pps = map(lambda x: float(x), samples['pps'])
        float_bps = map(lambda x: float(x), samples['bps'])
        sum_dpi_pps = reduce(add,
                             map(lambda x: x / 1000 if x > 100 else x, float_pps))
        sum_dpi_bps = reduce(add,
                             map(lambda x: x / 1000 if x > 100 else x, float_bps))

        return {'pps': round(sum_dpi_pps / 10, 3), 'bps': round(sum_dpi_bps / 10, 3)}
    except Exception as error:
        logger.error(error)
        return {'pps': None, 'bps': None}


def calculate_cpu_usage(cpu_idle):
    try:
        cpu_usage = round((100.0 - float(cpu_idle)), 3)
        return '{0}%'.format(str(cpu_usage))
    except Exception, error:
        logger.error(error)
        return None
