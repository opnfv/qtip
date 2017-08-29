#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -o errexit
set -o pipefail
set -o nounset
set -x

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

stack_json=${stack_json:-"$script_dir/default_stack.json"}
job_json=${job_json:-"$script_dir/default_job.json"}

WORKSPACE=${WORKSPACE:-$(pwd)}

nova_vm_mapping()
{
    openstack server list --name storperf-agent -c ID -c Host --long -f json > $WORKSPACE/nova_vm.json

    echo ==========================================================================
    echo "Vms vs. Compute nodes"
    cat $WORKSPACE/nova_vm.json
    echo ==========================================================================
}

storperf_api="http://storperf:5000/api/v1.0"

echo "QTIP: Waiting for storperf api ready"
while [ $(curl -s -o /dev/null -I -w "%{http_code}" -X GET ${storperf_api}/configurations) != "200" ]
do
    sleep 1
done

echo ==========================================================================
echo "Start to create storperf stack"
cat ${stack_json} 1>&2
echo ==========================================================================

curl -X POST --header 'Content-Type: application/json' \
     --header 'Accept: application/json' -d @${stack_json} \
     ${storperf_api}/configurations

nova_vm_mapping

echo
echo ==========================================================================
echo "Start to run storperf test"
cat ${job_json} 1>&2
echo ==========================================================================

JOB=$(curl -s -X POST --header 'Content-Type: application/json' \
    --header 'Accept: application/json' \
    -d @${job_json} ${storperf_api}/jobs | \
    awk '/job_id/ {print $2}' | sed 's/"//g')

echo "JOB ID: $JOB"
if [[ -z "$JOB" ]]; then
    echo "Oops, JOB ID is empty!"
    exit 1
else
    echo "checking job status..."
    curl -s -X GET "${storperf_api}/jobs?id=$JOB&type=status" \
        -o $WORKSPACE/status.json

    cat $WORKSPACE/status.json

    JOB_STATUS=`cat $WORKSPACE/status.json | awk '/Status/ {print $2}' | cut -d\" -f2`

    while [ "$JOB_STATUS" != "Completed" ]
    do
        sleep 180
        mv $WORKSPACE/status.json $WORKSPACE/old-status.json
        curl -s -X GET "${storperf_api}/jobs?id=$JOB&type=status" \
            -o $WORKSPACE/status.json
        JOB_STATUS=`cat $WORKSPACE/status.json | awk '/Status/ {print $2}' | cut -d\" -f2`

        set +o errexit # disable error exit checking for diff
        diff $WORKSPACE/status.json $WORKSPACE/old-status.json >/dev/null
        if [ $? -eq 1 ]
        then
            cat $WORKSPACE/status.json
        fi
        set -o errexit

    done

    echo
    echo "Storperf test completed!"

    echo ==========================================================================
    echo Final report
    echo ==========================================================================
    curl -s -X GET "${storperf_api}/jobs?id=$JOB&type=metadata" \
    -o $WORKSPACE/report.json
    cat $WORKSPACE/report.json
fi

echo "Deleting stack for cleanup"
curl -s -X DELETE --header 'Accept: application/json' ${storperf_api}/configurations
