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
                         .select_many(lambda child: child['children']) \
                         .where(lambda child: child['name'] == section_name) \
                         .to_list()
    return qpi


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
    table_workload = PrettyTable(['workload', 'Description', 'Baseline',
                                  'Results', 'Score'])
    table_workload.align = 'l'

    spec = extract_workload(report['spec']['sections'], section_name)
    baseline = extract_workload(report['baseline']['sections'], section_name)
    scores = extract_score(report['qpi']['children'], section_name, node)

    for sp, bl, score in zip(spec[0][0]['workloads'],
                             baseline[0][0]['workloads'],
                             scores[0]['children'][0]['children']):
        table_workload.add_row([sp['name'],
                               sp['description'],
                               bl['baseline'], 1, score['score']])
    click.echo(table_workload)
