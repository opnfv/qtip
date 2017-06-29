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


def extract_score(sections, section_name, node):
    """ Extract information related to QPI """
    qpi = query(sections).where(lambda child: child['name'] == node) \
                         .select_many(lambda child: child['sections']) \
                         .where(lambda child: child['name'] == section_name) \
                         .to_list()
    return qpi


def display_report(report, section_name, node):
    table_workload = PrettyTable(['Workload', 'Description',
                                  'Result', 'Score'])
    table_workload.align = 'l'

    scores = extract_score(report['nodes'], section_name, node)

    for sp in scores[0]['metrics'][0]['workloads']:
        table_workload.add_row([sp['name'],
                                sp['description'],
                                sp['result'],
                                sp['score']])
    return {
        "ss": scores[0]['score'],
        "desc": scores[0]['description'],
        "table": table_workload
    }


@click.group()
def cli():
    """ View QTIP results"""
    pass


@cli.command('show')
@click.option('-n', '--node', help="Compute node in OPNFV cluster")
@click.argument('section-name')
def show(node, section_name):
    qpi = ConsoleReporter.load_result()
    result = display_report(qpi, section_name, node)

    click.echo("Node Score: {}".format(qpi['score']))
    click.echo("Section Score: {}".format(result['ss']))
    click.echo("Description: {}".format(result['desc']))
    click.echo(result['table'])
