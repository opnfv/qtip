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
source $script_dir/utils.sh

export DOCKER_TAG=${DOCKER_TAG:-latest}

qtip_repo=/home/opnfv/repos/qtip

docker-compose -f $script_dir/${TEST_SUITE}/docker-compose.yaml pull
docker exec -t qtip bash -x ${qtip_repo}/qtip/scripts/quickstart.sh -q ${TEST_SUITE}

echo "${TEST_SUITE} QPI done!"

exit 0