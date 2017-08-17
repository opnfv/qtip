#!/usr/bin/env bash

set -o xtrace

export DOCKER_TAG=${DOCKER_TAG:-latest}
export DEPLOY_SCENARIO=${DEPLOY_SCENARIO:-generic}
export TEST_SUITE='compute'

# See https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $script_dir/periodic.sh
