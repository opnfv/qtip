##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from asq.initiators import query
import click
from prettytable import PrettyTable

from qtip.reporter.console import ConsoleReporter


def extract_workload(sections, section_name):
    """ Extract information related to SPEC and BASELINE """
    wl = query(sections).where(lambda section: section['name'] == section_name) \
                        .select(lambda section: section['metrics']) \
                        .to_list()
    return wl


def extract_score(sections, section_name, node):
    """ Extract information related to QPI """
    qpi = query(sections).where(lambda child: child['name'] == node) \
                         .select_many(lambda child: child['sections']) \
                         .where(lambda child: child['name'] == section_name) \
                         .to_list()
    return qpi


def display_report(report, section_name, node):
    table_workload = PrettyTable(['Workload', 'Description', 'Baseline',
                                  'Result', 'Score'])
    table_workload.align = 'l'

    spec = extract_workload(report['spec']['sections'], section_name)
    baseline = extract_workload(report['baseline']['sections'], section_name)
    scores = extract_score(report['qpi']['nodes'], section_name, node)

    if section_name == 'memory' or section_name == 'arithmetic':
        for sp, bl, sc in zip(spec[0],
                              baseline[0],
                              scores[0]['metrics'][0]['workloads']):
            for s, b in zip(sp['workloads'],
                            bl['workloads']):
                table_workload.add_row([s['name'],
                                        s['description'],
                                        b['baseline'],
                                        sc['result'],
                                        sc['score']])
    else:
        for sp, bl, sc in zip(spec[0],
                              baseline[0],
                              scores[0]['metrics']):
            for s, b, c in zip(sp['workloads'],
                               bl['workloads'],
                               sc['workloads']):
                table_workload.add_row([s['name'],
                                        s['description'],
                                        b['baseline'],
                                        c['result'],
                                        c['score']])

    click.echo("Node Score: {}".format(report['qpi']['score']))
    click.echo("Section Score: {}".format(scores[0]['score']))
    click.echo("Description: {}".format(scores[0]['description']))
    click.echo(table_workload)


@click.group()
def cli():
    """ View QTIP results"""
    pass


@cli.command('show')
@click.option('-n', '--node', help="Compute node in OPNFV cluster")
@click.argument('section-name')
def show(node, section_name):
    reporter = ConsoleReporter({})
    report = reporter.render()
    display_report(report, section_name, node)
