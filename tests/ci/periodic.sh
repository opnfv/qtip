#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
set -e
set -x

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source ${script_dir}/utils/start_services.sh

docker exec ${TEST_SUITE}_qtip bash -x /home/opnfv/repos/qtip/qtip/scripts/quickstart.sh

echo "${TEST_SUITE} QPI done!"

exit 0
