#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

usage(){
   echo "usage: $0 -t <installer_type> -i <installer_ip> -s <stack_json_path> -j <job_json_path> " >&2
}

#Get options
while getopts ":t:i:s:j:he" optchar; do
   case "${optchar}" in
       t) installer_type=${OPTARG} ;;
       i) installer_ip=${OPTARG} ;;
       s) stack_json=${OPTARG} ;;
       j) job_json=${OPTARG} ;;
       h) usage
          exit 0
          ;;
       *) echo "Non-option argument: '-${OPTARG}'" >&2
          usage
          exit 2
          ;;
   esac
done

# See https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ -z $WORKSPACE ]];then
    WORKSPACE=`pwd`
fi

#set vars from env if not provided by user as options
installer_type=${installer_type:-$INSTALLER_TYPE}
installer_ip=${installer_ip:-$INSTALLER_IP}
stack_json=${stack_json:-"$script_dir/default_stack.json"}
job_json=${job_json:-"$script_dir/default_job.json"}

source $script_dir/openstack.sh
source $script_dir/storperf_docker.sh

git clone --depth 1 https://gerrit.opnfv.org/gerrit/storperf $WORKSPACE/storperf
git clone --depth 1 https://gerrit.opnfv.org/gerrit/releng $WORKSPACE/releng

virtualenv $WORKSPACE/storperf_venv
source $WORKSPACE/storperf_venv/bin/activate

pip install -r $script_dir/storperf_requirements.txt

$WORKSPACE/releng/utils/fetch_os_creds.sh -i ${installer_type} -a ${installer_ip} -d $WORKSPACE/openrc
source $WORKSPACE/openrc

grep "export" $WORKSPACE/openrc | sed "s/export //"  > $WORKSPACE/admin.rc
echo "INSTALLER_TYPE=${installer_type}" >> $WORKSPACE/admin.rc
export ENV_FILE=$WORKSPACE/admin.rc

if [[ ! -d $WORKSPACE/carbon ]];then
    mkdir -p $WORKSPACE/carbon
    sudo chown 33:33 $WORKSPACE/carbon
fi
export CARBON_DIR=$WORKSPACE/carbon/

delete_storperf_stack
load_ubuntu_image
create_storperf_flavor

cd $WORKSPACE/storperf/docker
cp $script_dir/storperf-docker-compose.yaml ./
echo "Clean existing storperf containers"
clean_storperf_container
echo "Launch new storperf containers"
launch_storperf_container

$script_dir/start_job.sh -s $stack_json -j $job_json

echo "Clean up environment"
cd $WORKSPACE/storperf/docker
clean_storperf_container
openstack flavor delete storperf
openstack image delete "Ubuntu 16.04 x86_64"

echo "Done!"

