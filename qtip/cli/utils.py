##############################################################################
# Copyright (c) 2017 taseer94@gmail.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from prettytable import PrettyTable


def table(name, components):
    """ Return a PrettyTable for component listing """
    table = PrettyTable([name])
    table.align[name] = 'l'
    [table.add_row([component['name'][0:-5]]) for component in components]
    return table
