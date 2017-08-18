#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
set -e


case $INSTALLER_TYPE in
    apex)
        INSTALLER_IP=`sudo virsh domifaddr undercloud | grep ipv4 | awk '{print $4}' | cut -d/ -f1`
        ;;
esac

cat << EOF > $WORKSPACE/env_file
INSTALLER_TYPE=$INSTALLER_TYPE
INSTALLER_IP=$INSTALLER_IP
POD_NAME=$NODE_NAME
SCENARIO=$DEPLOY_SCENARIO
TESTAPI_URL=$TESTAPI_URL
EOF

echo "--------------------------------------------------------"
cat $WORKSPACE/env_file
echo "--------------------------------------------------------"

# Remove previous running containers if exist
if [[ ! -z $(docker ps -a | grep "opnfv/qtip:$DOCKER_TAG") ]]; then
    echo "Removing existing opnfv/qtip containers..."
    # workaround: sometimes it throws an error when stopping qtip container.
    # To make sure ci job unblocked, remove qtip container by force without stopping it.
    docker rm -f $(docker ps -a | grep "opnfv/qtip:$DOCKER_TAG" | awk '{print $1}')
fi

# Remove existing images if exist
if [[ $(docker images opnfv/qtip:${DOCKER_TAG} | wc -l) -gt 1 ]]; then
    echo "Removing docker image opnfv/qtip:$DOCKER_TAG..."
    docker rmi -f opnfv/qtip:$DOCKER_TAG
fi

echo "Qtip: Pulling docker image: opnfv/qtip:${DOCKER_TAG}"
docker pull opnfv/qtip:$DOCKER_TAG >/dev/null

envs="--env-file $WORKSPACE/env_file"
vols="-v /root/.ssh:/root/.ssh"

cmd="sudo docker run -id ${envs} ${vols} opnfv/qtip:${DOCKER_TAG} /bin/bash"
echo "Qtip: Running docker command: ${cmd}"
${cmd}

container_id=$(docker ps | grep "opnfv/qtip:${DOCKER_TAG}" | awk '{print $1}' | head -1)
if [ $(docker ps | grep 'opnfv/qtip' | wc -l) == 0 ]; then
    echo "The container opnfv/qtip with ID=${container_id} has not been properly started. Exiting..."
    exit 1
fi

echo "The container ID is: ${container_id}"
QTIP_REPO=/home/opnfv/repos/qtip

case $TEST_SUITE in
    compute)
        docker exec -t ${container_id} bash -c "bash ${QTIP_REPO}/tests/ci/run_compute_qpi.sh"
        ;;
esac

echo "Qtip done!"
exit 0