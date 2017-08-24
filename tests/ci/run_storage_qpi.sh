#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd /home/opnfv

qtip create --project-template storage --pod-name ${NODE_NAME} --installer-type ${INSTALLER_TYPE} \
--installer-host ${INSTALLER_IP} --scenario ${SCENARIO} workspace

cd /home/opnfv/workspace/

qtip setup
eval `ssh-agent`
if [[ -z $testapi_url ]];then
    qtip run -vv
else
    qtip run --extra-vars "testapi_url=${TESTAPI_URL}"
fi
qtip teardown
