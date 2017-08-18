#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

#TODO: These will be replaced by qtip cli
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$script_dir/storperf/prepare.sh
$script_dir/storperf/start_job.sh