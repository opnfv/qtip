#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

clean_containers()
{
    echo "QTIP: Cleanup existing qtip and storperf containers"
    docker-compose -f qtip-storperf-docker-compose.yaml down

    for name in qtip storperf-master storperf-swaggerui storperf-httpfrontend storperf-reporting
    do
        container=$(docker ps -a | grep "opnfv/${name}：${DOCKER_TAG}" | awk '{print $1}')
        if [[ ! -z "$container" ]]; then
            echo "QTIP: Removing any existing $name container"
            docker rm -v $container
        fi

        if [[ $(docker images opnfv/${name}:${DOCKER_TAG} | wc -l) -gt 1 ]]; then
            echo "QTIP: Removing docker image opnfv/$name :$DOCKER_TAG..."
            docker rmi opnfv/${name}:${DOCKER_TAG}
        fi
    done
}


launch_containers()
{
    echo "Launch new qtip and storperf containers"
    docker-compose -f qtip-storperf-docker-compose.yaml pull
    docker-compose -f qtip-storperf-docker-compose.yaml up -d

    echo "QTIP: Waiting for StorPerf to become active"

    while [ $(curl -s -o /dev/null -I -w "%{http_code}" -X GET http://127.0.0.1:5000/api/v1.0/configurations) != "200" ]
    do
        sleep 1
    done
}