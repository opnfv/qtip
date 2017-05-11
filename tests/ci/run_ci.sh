#!/bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
set -e

usage(){
   echo "usage: $0 -t <installer_type> -i <installer_ip> -p <pod_name> -s <scenario>" >&2
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
   error "Can not talk to $ip."
}

#Getoptions
while getopts ":t:i:p:s:he" optchar; do
   case "${optchar}" in
       t) installer_type=${OPTARG} ;;
       i) installer_ip=${OPTARG} ;;
       p) pod_name=${OPTARG} ;;
       s) scenario=${OPTARG} ;;
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


if [ "$installer_type" != "fuel" ]; then
    echo "Not support ${installer_type} right now!"
    exit 1
fi

verify_connectivity ${installer_ip}

ssh-keygen -t rsa -f ~/.ssh/id_rsa -P ''
sshpass -p r00tme ssh-copy-id -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${installer_ip}

cd /home/opnfv

qtip workspace create --pod ${pod_name} --installer ${installer_type} \
--master-host ${installer_ip} --scenario ${scenario} workspace

cd /home/opnfv/workspace/

ansible-playbook setup.yml
eval `ssh-agent`
ansible-playbook run.yml
ansible-playbook teardown.yml

echo "Qtip done!"
exit 0