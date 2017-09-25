#!/bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -o nounset
set -o errexit
set -o pipefail
set -x

usage(){
   echo "usage: $0 -q <qtip_test_suite> -t <installer_type> -i <installer_ip> -p <pod_name> -s <scenario> -r <report_url>" >&2
}

verify_connectivity(){
   local ip=$1
   echo "Verifying connectivity to $ip..."
   for i in $(seq 0 10); do
       if ping -c 1 -W 1 $ip > /dev/null; then
           echo "$ip is reachable!"
           return 0
       fi
       sleep 1
   done
   echo "Can not talk to $ip."
}

#Getoptions
while getopts ":t:i:p:s:r:he" optchar; do
   case "${optchar}" in
       q) test_suite=${OPTARG} ;;
       t) installer_type=${OPTARG} ;;
       i) installer_ip=${OPTARG} ;;
       p) pod_name=${OPTARG} ;;
       s) scenario=${OPTARG} ;;
       r) testapi_url=${OPTARG} ;;
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
installer_ip=${installer_ip:-$INSTALLER_IP}
test_suite=${test_suite:-$TEST_SUITE}
pod_name=${pod_name:-$NODE_NAME}
scenario=${scenario:-$SCENARIO}
testapi_url=${testapi_url:-$TESTAPI_URL}

# we currently support ericsson, intel, lf and zte labs
if [[ ! "$installer_type" =~ (fuel|apex) ]]; then
    echo "Unsupported/unidentified installer $installer_type. Cannot continue!"
    exit 1
fi

sshoptions="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

verify_connectivity ${installer_ip}

case "$installer_type" in
    fuel)
        ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa -q
        sshpass -p r00tme ssh-copy-id $sshoptions ${installer_ip}
        ;;
esac

cd /home/opnfv

qtip create --project-template ${test_suite} --pod-name ${pod_name} --installer-type ${installer_type} \
--installer-host ${installer_ip} --scenario ${scenario} ${test_suite}

cd ${test_suite}

qtip setup
eval `ssh-agent`
if [[ -z $testapi_url ]];then
    qtip run
else
    qtip run --extra-vars "testapi_url=$testapi_url"
fi
qtip teardown

# Remove ssh public key from installer
case "$installer_type" in
    fuel)
        publickey=$(sed -r 's/\//\\\//g' /root/.ssh/id_rsa.pub)
        ssh $sshoptions root@${installer_ip} "sed -i '/$publickey/d' /root/.ssh/authorized_keys"
        ;;
esac

echo "QTIP testing done!"
exit 0
