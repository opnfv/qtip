#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

if [[ -e $ENV_FILE ]];then
    rm $ENV_FILE
fi

echo "INSTALLER_TYPE=$INSTALLER_TYPE" >> $ENV_FILE
echo "INSTALLER_IP=$INSTALLER_IP" >> $ENV_FILE
echo "NODE_NAME=$NODE_NAME" >> $ENV_FILE
echo "SCENARIO=$DEPLOY_SCENARIO" >> $ENV_FILE
echo "TESTAPI_URL=$TESTAPI_URL" >> $ENV_FILE

if [[ "$TEST_SUITE" == 'compute' ]];then

    echo "--------------------------------------------------------"
    cat $ENV_FILE
    echo "--------------------------------------------------------"

    if [[ ! -z $(docker ps -a | grep "opnfv/qtip:$DOCKER_TAG") ]]; then
        echo "Removing existing opnfv/qtip containers..."
        container_id=$(docker ps -a | grep "opnfv/qtip:$DOCKER_TAG" | awk '{print $1}')
        docker stop $container_id
        docker rm $container_id
    fi

    if [[ $(docker images opnfv/qtip:${DOCKER_TAG} | wc -l) -gt 1 ]]; then
        echo "Removing docker image opnfv/qtip:$DOCKER_TAG..."
        docker rmi opnfv/qtip:$DOCKER_TAG
    fi

    echo "Qtip: Pulling docker image: opnfv/qtip:${DOCKER_TAG}"
    docker pull opnfv/qtip:$DOCKER_TAG >/dev/null

    envs="--env-file $ENV_FILE"
    vols=""
    if [[ "$INSTALLER_TYPE" == "apex" ]];then     vols="-v /root/.ssh:/root/.ssh"
    fi

    cmd="sudo docker run -id ${envs} ${vols} opnfv/qtip:${DOCKER_TAG} /bin/bash"
    echo "Qtip: Running docker command: ${cmd}"
    ${cmd}

elif [[ "$TEST_SUITE" == 'storage' ]];then
    script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    git clone --depth 1 https://gerrit.opnfv.org/gerrit/releng $WORKSPACE/releng
    $WORKSPACE/releng/utils/fetch_os_creds.sh -i $INSTALLER_TYPE -a $INSTALLER_IP -d $WORKSPACE/openrc

    grep "export" $WORKSPACE/openrc | sed "s/export //" >> $ENV_FILE
    echo "DOCKER_TAG=$DOCKER_TAG" >> $ENV_FILE

    echo "--------------------ENV_FILE----------------------------"
    cat $ENV_FILE
    echo "--------------------------------------------------------"

    source $script_dir/storperf/containers.sh
    cd $script_dir/storperf
    clean_containers
    launch_containers
else
    echo "Sorry, not support test suite $TEST_SUITE!"
    exit 1
fi
