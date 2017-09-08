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
source $script_dir/utils.sh

export DEPLOY_SCENARIO='generic'
export DOCKER_TAG='latest'
export CI_DEBUG='false'
export TEST_SUITE='storage'
export TESTAPI_URL=''
export SSH_CREDENTIALS='/root/.ssh'

export WORKSPACE=${WORKSPACE:-$(pwd)}

start_services

cd ${WORKSPACE}

qtip_repo='/home/opnfv/repos/qtip'
docker cp . qtip:${qtip_repo}
docker exec qtip bash -c "cd ${qtip_repo} && pip install -U -e ."
docker exec -t qtip bash -x ${qtip_repo}/qtip/scripts/quickstart.sh ${TEST_SUITE}
echo "QTIP: Verify ${TEST_SUITE} done!"

exit 0
