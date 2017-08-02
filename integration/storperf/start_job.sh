#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

usage(){
   echo "usage: $0 -s <stack_json_path> -j <job_json_path>" >&2
}

#Get options
while getopts ":s:j:he" optchar; do
   case "${optchar}" in
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

source $script_dir/openstack.sh

echo ==========================================================================
echo "Start to create storperf stack"
cat ${stack_json} 1>&2
echo ==========================================================================

curl -X POST --header 'Content-Type: application/json' \
     --header 'Accept: application/json' -d @${stack_json} \
     'http://127.0.0.1:5000/api/v1.0/configurations'

nova_vm_mapping

echo
echo ==========================================================================
echo "Start to run storperf test"
cat ${job_json} 1>&2
echo ==========================================================================

JOB=$(curl -s -X POST --header 'Content-Type: application/json' \
    --header 'Accept: application/json' \
    -d @${job_json} 'http://127.0.0.1:5000/api/v1.0/jobs' | \
    awk '/job_id/ {print $2}' | sed 's/"//g')

echo "JOB ID: $JOB"
if [[ -z "$JOB" ]]; then
    echo "Oops, JOB ID is empty!"
else
    echo "Loop: check job status"
    curl -s -X GET "http://127.0.0.1:5000/api/v1.0/jobs?id=$JOB&type=status" \
        -o $WORKSPACE/status.json

    JOB_STATUS=`cat $WORKSPACE/status.json | awk '/Status/ {print $2}' | cut -d\" -f2`
    while [ "$JOB_STATUS" != "Completed" ]
    do
        sleep 30
        mv $WORKSPACE/status.json $WORKSPACE/old-status.json
        curl -s -X GET "http://127.0.0.1:5000/api/v1.0/jobs?id=$JOB&type=status" \
            -o $WORKSPACE/status.json
        JOB_STATUS=`cat $WORKSPACE/status.json | awk '/Status/ {print $2}' | cut -d\" -f2`
        diff $WORKSPACE/status.json $WORKSPACE/old-status.json >/dev/null
        if [ $? -eq 1 ]
        then
            cat $WORKSPACE/status.json
        fi
    done

    echo ==========================================================================
    echo "Storperf test completed!"
    echo ==========================================================================

    curl -s -X GET "http://127.0.0.1:5000/api/v1.0/jobs?id=$JOB&type=metadata" \
    -o $WORKSPACE/report.json

    echo ==========================================================================
    echo Final report
    echo ==========================================================================
    cat $WORKSPACE/report.json
fi

echo "Deleting stack for cleanup"
curl -s -X DELETE --header 'Accept: application/json' 'http://127.0.0.1:5000/api/v1.0/configurations'

