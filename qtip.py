##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from func.cli import Cli
import os


def main():
    os.system('./data/file_permission.sh')
    Cli()
#    os.system('cd data/ref_results && python compute_suite.py')
#    os.system('cd data/ref_results && python storage_suite.py')
#    os.system('cd data/ref_results && python network_suite.py')
#   os.system('cd data/report && python Qtip_Report.py')

if __name__ == "__main__":
    main()
