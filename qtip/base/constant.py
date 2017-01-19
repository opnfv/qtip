##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from os import path
from os.path import expanduser


class FormulaName(object):
    """formula names"""
    ARITHMETIC_MEAN = 'arithmetic mean'
    WEIGHTED_ARITHMETIC_MEAN = 'weighted arithmetic mean'
    GEOMETRIC_MEAN = 'geometric mean'
    WEIGHTED_GEOMETRIC_MEAN = 'weighted geometric mean'


class PkgName(object):
    """QTIP package names"""
    COLLECTOR = 'collector'
    DRIVER = 'driver'
    REPORTER = 'reporter'
    RUNNER = 'runner'
    SPEC = 'spec'


class PropName(object):
    """property names"""
    # list
    NAME = 'name'
    CONTENT = 'content'
    ABSPATH = 'abspath'
    # content
    name = 'name'
    DESCRIPTION = 'description'
    # spec
    SECTIONS = 'sections'
    WEIGHT = 'weight'
    FORMULA = 'formula'
    METRICS = 'metrics'
    WORKLOADS = 'workloads'
    # plan
    CONFIG = 'config'
    FACILITY = 'facility'
    ENGINEER = 'engineer'
    DRIVER = 'driver'
    COLLECTOR = 'collector'
    REPORTER = 'reporter'
    QPIS = 'QPIs'


class FileName(object):
    SCRIPT_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir,
                           'scripts')
    CONFIG_DIR = path.join(path.dirname(__file__), path.pardir, path.pardir,
                           'config')
    PRIVATE_KEY = CONFIG_DIR + '/QtipKey'
    PUBLIC_KEY = CONFIG_DIR + '/QtipKey.pub'
    IPS_FILE = expanduser('~') + "/qtip/ips.log"
    HOST_FILE = CONFIG_DIR + "/host"
