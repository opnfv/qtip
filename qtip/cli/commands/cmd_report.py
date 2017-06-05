##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import click
from prettytable import PrettyTable

from qtip.reporter.console import ConsoleReporter


def get_val(param, metric):
    result = []
    for section in param['sections']:
        if section['name'] == metric:
            for metric in section['metrics']:
                result.append(metric['workloads'])
    return result


def get_result(param, metric, node):
    for child in param['children']:
        if child['name'] == node:
            for child_metric in child['children']:
                if child_metric['name'] == metric:
                    return child_metric['children']


@click.group()
def cli():
    """ View QTIP results"""
    pass


@cli.command('show')
@click.argument('metric')
@click.argument('node')
def show(metric, node):
    reporter = ConsoleReporter({})
    report = reporter.render()
    table_workload = PrettyTable(['workload', 'Description', 'Baseline', 'Results', 'Score'])
    table_workload.align = 'l'

    spec = get_val(report[0], metric)
    baseline = get_val(report[1], metric)
    qpi = get_result(report[2], metric, node)

    for i in range(0, len(spec)):
        for j in range(0, len(spec[i])):
            table_workload.add_row([spec[i][j]['name'], spec[i][j]['description'], baseline[i][j]['baseline'],
                                   1, qpi[0]['children'][j]['score']])
    click.echo(table_workload)
