##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################



import yaml
import os


class Validate_Yaml():

    def __init__(self, doc):

        print 'Validating YAML CONFIG FILE'

        if not doc['Scenario']:
            print '\nScenario Field missing\n'
        if not doc['Scenario']['benchmark']:
            print '\nBenchmark field missing'
        if not doc['Scenario']['pointless']:
            print '\nBabyeating anumal'
        if not doc['Context']:
            print '\nEntire Context is missing'
        if not doc['Context']['Host_Machine']:
            print '\nNo Host Machine'
        if not doc['Context']['Host_Machine']['machine_1']
