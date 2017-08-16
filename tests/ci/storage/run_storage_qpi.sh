#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $script_dir/prepare.sh
source $script_dir/launch_storperf_container.sh
source $script_dir/start_job.sh