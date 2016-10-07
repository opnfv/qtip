##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from func.cli import cli
import os


def main():
    os.system('./data/file_permission.sh')
    cli()

if __name__ == "__main__":
    main()
