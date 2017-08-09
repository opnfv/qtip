#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

usage(){
   echo "usage: $0 -t <installer_type> -n <node_name>" >&2
}

#Get options
while getopts ":t:n:he" optchar; do
   case "${optchar}" in
       t) installer_type=${OPTARG} ;;
       n) node_name=${OPTARG} ;;
       h) usage
          exit 0
          ;;
       *) echo "Non-option argument: '-${OPTARG}'" >&2
          usage
          exit 2
          ;;
   esac
done


#set vars from env if not provided by user as options
installer_type=${installer_type:-$INSTALLER_TYPE}
node_name=${node_name:-$NODE_NAME}

case $installer_type in
    apex)
        installer_ip=`sudo virsh domifaddr undercloud | grep ipv4 | awk '{print $4}' | cut -d/ -f1`
        ;;
    *)

        echo "Unsupported $installer_type. Cannot continue!"
        exit 1
esac

if [[ -z $WORKSPACE ]];then
    WORKSPACE=`pwd`
fi

git clone --depth 1 https://gerrit.opnfv.org/gerrit/releng $WORKSPACE/releng

$WORKSPACE/releng/utils/fetch_os_creds.sh -i ${installer_type} -a ${installer_ip} -d $WORKSPACE/openrc

grep "export" $WORKSPACE/openrc | sed "s/export //"  > $WORKSPACE/admin.rc
echo "INSTALLER_TYPE=${installer_type}" >> $WORKSPACE/admin.rc
echo "INSTALLER_IP=${installer_ip}" >> $WORKSPACE/admin.rc
echo "NODE_NAME=${node_name}" >> $WORKSPACE/admin.rc
export ENV_FILE=$WORKSPACE/admin.rc

export CARBON_DIR=$WORKSPACE/carbon/
WWW_DATA_UID=33
WWW_DATA_GID=33
sudo install --owner=${WWW_DATA_UID} --group=${WWW_DATA_GID} -d "${CARBON_DIR}"

clean_storperf_container()
{
    docker-compose -f docker-compose.yaml down

    for name in qtip storperf-master storperf-swaggerui storperf-httpfrontend storperf-reporting
    do
        container=`docker ps -a -q -f name=$name`
        if [[ ! -z $container ]];then
            echo "Stopping any existing $name container"
            docker rm -fv $container
        fi

        image=`docker images opnfv/$name`
        if [[ ! -z $image ]];then
            echo "Deleteing any existing opnfv/$name image"
            docker rmi -f opnfv/$container_name
        fi
    done
}

launch_storperf_container()
{
    docker-compose pull
    docker-compose -f docker-compose.yaml up -d

    echo "Waiting for StorPerf to become active"

    while [ $(curl -s -o /dev/null -I -w "%{http_code}" -X GET http://127.0.0.1:5000/api/v1.0/configurations) != "200" ]
    do
        sleep 1
    done
}

echo "Clean existing storperf containers"
clean_storperf_container

echo "Launch new storperf containers"
launch_storperf_container