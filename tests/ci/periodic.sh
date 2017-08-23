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

export DOCKER_TAG=${DOCKER_TAG:-latest}
export ENV_FILE=$WORKSPACE/env_file
QTIP_REPO=/home/opnfv/repos/qtip

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $script_dir/launch_containers_by_testsuite.sh

container_id=$(docker ps | grep "opnfv/qtip:${DOCKER_TAG}" | awk '{print $1}' | head -1)

if [[ -z "$container_id" ]]; then
    echo "QTIP: The container opnfv/qtip has not been properly started. Exiting..."
    exit 1
else
    echo "QTIP: The container ID is: ${container_id}"
    docker exec -t ${container_id} bash -c "bash ${QTIP_REPO}/tests/ci/run_${TEST_SUITE}_qpi.sh"
fi

echo "${TEST_SUITE} QPI done!"
exit 0