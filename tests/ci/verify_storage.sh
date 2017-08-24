#! /bin/bash -x
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

TEST_SUITE=storage
QTIP_REPO=/home/opnfv/repos/qtip

export DOCKER_TAG=${DOCKER_TAG:-latest}
export ENV_FILE=$WORKSPACE/env_file

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $script_dir/launch_containers_by_testsuite.sh

container_id=$(docker ps | grep "opnfv/qtip:${DOCKER_TAG}" | awk '{print $1}' | head -1)

if [[ -z "$container_id" ]]; then
    echo "QTIP: The container opnfv/qtip has not been properly started. Exiting..."
    exit 1
else
    echo "QTIP: Copying current submit patch to the container ${container_id}"
    cd $WORKSPACE
    docker cp . ${container_id}:${QTIP_REPO}
    docker exec ${container_id} bash -c "cd ${QTIP_REPO} && pip install -U -e ."
    docker exec -t ${container_id} bash -x ${QTIP_REPO}/tests/ci/run_${TEST_SUITE}_qpi.sh
    echo "QTIP: Verify ${TEST_SUITE} done!"
    exit 0
fi


