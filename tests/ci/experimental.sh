#!/usr/bin/env bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -o errexit
set -o pipefail
set -o nounset
set -x

export DEPLOY_SCENARIO='generic'
export DOCKER_TAG='latest'
export CI_DEBUG='false'
export TEST_SUITE='storage'
export TESTAPI_URL=''

export WORKSPACE=${WORKSPACE:-$(pwd)}

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
qtip_repo='/home/opnfv/repos/qtip'

source $script_dir/launch_containers_by_testsuite.sh

container_id=$(docker ps | grep "opnfv/qtip:${DOCKER_TAG}" | awk '{print $1}' | head -1)

echo "QTIP: Copying current submit patch to the container ${container_id}"
cd $WORKSPACE
docker cp . ${container_id}:${qtip_repo}
docker exec ${container_id} bash -c "cd ${qtip_repo} && pip install -U -e ."
docker exec -t ${container_id} bash -x ${qtip_repo}/tests/ci/run_${TEST_SUITE}_qpi.sh
echo "QTIP: Verify ${TEST_SUITE} done!"
exit 0
