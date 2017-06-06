##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from jinja2 import Environment
from jinja2 import FileSystemLoader
import os
from os import path
from prettytable import PrettyTable


QTIP_PACKAGE = path.join(path.dirname(__file__), os.pardir, os.pardir)
QTIP_ANSIBLE_ROLES = path.join(QTIP_PACKAGE, 'resources', 'ansible_roles')


def join_vars(**kwargs):
    return " ".join(["{}={}".format(variable, value) for variable, value in kwargs.items() if value is not None])


def table(name, components):
    """ Return a PrettyTable for component listing """
    table = PrettyTable([name])
    table.align[name] = 'l'
    [table.add_row([component['name'][0:-5]]) for component in components]
    return table


def render(name, var_dict):
    """ Get the templates to render for specific component """
    tmpl_path = path.join(path.dirname(__file__), 'templates')
    tmpl_loader = FileSystemLoader(tmpl_path)
    env = Environment(loader=tmpl_loader)
    template = env.get_template('{}.j2'.format(name))
    result = template.render(var_dict)
    return result
