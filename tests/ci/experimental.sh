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

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export DEPLOY_SCENARIO='generic'
export DOCKER_TAG='latest'
export CI_DEBUG='false'
export TEST_SUITE='storage'
export TESTAPI_URL=''
export SSH_CREDENTIALS='/root/.ssh'

export WORKSPACE=${WORKSPACE:-$(pwd)}

source ${script_dir}/utils/start_services.sh

cd ${WORKSPACE}

qtip_repo='/home/opnfv/repos/qtip'
docker cp . ${TEST_SUITE}_qtip:${qtip_repo}
docker exec ${TEST_SUITE}_qtip bash -c "cd ${qtip_repo} && pip install -U -e ."

docker exec ${TEST_SUITE}_qtip bash -x ${qtip_repo}/qtip/scripts/quickstart.sh
echo "QTIP: Verify ${TEST_SUITE} done!"

exit 0
