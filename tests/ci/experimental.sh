#!/usr/bin/env bash

export DOCKER_TAG=${DOCKER_TAG:-latest}
export DEPLOY_SCENARIO=${DEPLOY_SCENARIO:-generic}

# See https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$script_dir/periodic.sh
