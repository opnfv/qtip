#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
set -e

if [[ -z $WORKSPACE ]];then
    WORKSPACE=`pwd`
fi

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

grep "export" $WORKSPACE/openrc | sed "s/export //"  > $WORKSPACE/admin.rc
echo "INSTALLER_TYPE=$INSTALLER_TYPE" >> $WORKSPACE/admin.rc
export ENV_FILE=$WORKSPACE/admin.rc

clean_storperf_container()
{
    docker-compose -f storperf-docker-compose.yaml down

    for name in storperf-master storperf-swaggerui storperf-httpfrontend storperf-reporting
    do
        container=`docker ps -a -q -f name=$name`
        if [[ ! -z $container ]];then
            echo "Stopping any existing $name container"
            docker rm -fv $container
        fi
        if [[ $(docker images | grep opnfv/${name} | wc -l) -gt 1 ]];then
            echo "Deleteing any existing opnfv/$name image"
            docker rmi -f $(docker images | grep opnfv/${name} | awk '{print $3}')
        fi
    done
}

launch_storperf_container()
{
    docker-compose -f storperf-docker-compose.yaml pull
    docker-compose -f storperf-docker-compose.yaml up -d

    echo "Waiting for StorPerf to become active"

    while [ $(curl -s -o /dev/null -I -w "%{http_code}" -X GET http://127.0.0.1:5000/api/v1.0/configurations) != "200" ]
    do
        sleep 1
    done
}

cd $script_dir
echo "Clean existing storperf containers"
clean_storperf_container

echo "Launch new storperf containers"
launch_storperf_container