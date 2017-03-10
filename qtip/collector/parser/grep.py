##############################################################################
# Copyright (c) 2017 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from collections import defaultdict
from os import path
import re

import yaml

from qtip.base import BaseActor
from qtip.base.constant import BaseProp
from qtip.collector import calculator
from qtip.util.logger import QtipLogger

logger = QtipLogger('grep').get

REGEX_FILE = path.join(path.dirname(__file__), 'regex.yaml')


class GrepProp(BaseProp):
    FILENAME = 'filename'
    REGEX = 'regex'


class GrepParser(BaseActor):
    TYPE = 'grep'

    def run(self):
        filename = self._parent.get_config(GrepProp.FILENAME)
        return grep_in_file(self._parent.find(filename), self._config[GrepProp.REGEX])


def grep_in_file(filename, regex):
    with open(filename, 'r') as f:
        return filter(lambda x: x is not None,
                      re.finditer(regex, f.read(), re.MULTILINE))


def parse_benchmark_result(result_dir):
    regex_config = yaml.safe_load(file(REGEX_FILE))
    benchmark = result_dir.split('/')[-1]
    result = {'name': benchmark}
    samples = parse_logfile(regex_config[benchmark], result_dir)
    result['results'] = format_samples(benchmark, samples)
    result['sysinfo'] = parse_logfile(regex_config['sysinfo'], result_dir)
    return result


def format_samples(benchmark, samples):
    if benchmark == 'dpi':
        return calculator.dpi_calculator(samples)
    if benchmark == 'dhrystone' or benchmark == 'whetstone':
        return {'total_cpus': samples['total_cpus'],
                'single_cpu': {'num': samples['single_cpu'],
                               'score': samples['score'][0]},
                'multi_cpus': {'num': samples['multi_cpus'],
                               'score': samples['score'][1]}}
    else:
        return samples.copy()


def parse_logfile(config, paths):
    captured = {}
    for regex_rules_by_file in config:
        filename = \
            '{0}/{1}'.format(paths, regex_rules_by_file[GrepProp.FILENAME])
        for regex in regex_rules_by_file['grep']:
            matches = grep_in_file(filename, regex)
            for item in matches:
                print item.groupdict()
            if len(matches) > 1:
                temp_dict = defaultdict(list)
                for item in [match.groupdict() for match in matches]:
                    for key in item:
                        temp_dict[key].append(item[key])
                captured.update(temp_dict)
            elif len(matches) == 1:
                captured.update(matches[0].groupdict())
            else:
                logger.error("Nothing is matched from {0}".format(filename))
    return captured