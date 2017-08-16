#! /bin/bash -x
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

WORKSPACE=${WORKSPACE:=`pwd`}

export DOCKER_TAG=${DOCKER_TAG:-latest}
export ENV_FILE=$WORKSPACE/env_file

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

case $INSTALLER_TYPE in
    apex)
        INSTALLER_IP=`sudo virsh domifaddr undercloud | grep ipv4 | awk '{print $4}' | cut -d/ -f1`
        ;;
esac

git clone --depth 1 https://gerrit.opnfv.org/gerrit/releng $WORKSPACE/releng
$WORKSPACE/releng/utils/fetch_os_creds.sh -i $INSTALLER_TYPE -a $INSTALLER_IP -d $WORKSPACE/openrc

grep "export" $WORKSPACE/openrc | sed "s/export //"  > $WORKSPACE/env_file
echo "INSTALLER_TYPE=$INSTALLER_TYPE" >> $WORKSPACE/env_file
echo "INSTALLER_IP=$INSTALLER_IP" >> $WORKSPACE/env_file
echo "NODE_NAME=$NODE_NAME" >> $WORKSPACE/env_file
echo "SCENARIO=$DEPLOY_SCENARIO" >> $WORKSPACE/env_file
echo "TESTAPI_URL=$TESTAPI_URL" >> $WORKSPACE/env_file
echo "DOCKER_TAG=$DOCKER_TAG" >> $WORKSPACE/env_file

echo "--------------------ENV_FILE----------------------------"
cat $WORKSPACE/env_file
echo "--------------------------------------------------------"

source $script_dir/storperf/containers.sh
cd $script_dir/storperf
clean_containers
launch_containers

container_id=$(docker ps | grep "opnfv/qtip:${DOCKER_TAG}" | awk '{print $1}' | head -1)

if [[ "$INSTALLER_TYPE" == "apex" ]];then
    if [ -f /root/.ssh/id_rsa ]; then
        sudo chmod 600 /root/.ssh/id_rsa
        sudo docker cp /root/.ssh/id_rsa ${container_id}:/root/.ssh/
    fi
fi

QTIP_REPO=/home/opnfv/repos/qtip

echo "QTIP: Copying current submit patch to the container ${container_id}"
cd $WORKSPACE
docker cp . ${container_id}:${QTIP_REPO}
docker exec ${container_id} bash -c "cd ${QTIP_REPO} && pip install -U -e ."

docker exec -t ${container_id} bash -c "bash ${QTIP_REPO}/tests/ci/run_storage_qpi.sh"

echo "Verify storage done!"
exit 0