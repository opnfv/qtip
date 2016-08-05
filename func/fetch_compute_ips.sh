#!/bin/bash
##############################################################################
#Copyright (c) 2015 Ericsson AB, ZTE and others.
#jose.lausuch@ericsson.com
#wu.zhihui1@zte.com.cn
#All rights reserved. This program and the accompanying materials
#are made available under the terms of the Apache License, Version 2.0
#which accompanies this distribution, and is available at
#http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


usage(){
   echo "usage: $0 [-v] -d -i <installer_type> -a <installer_ip>" >&2
   echo "[-v] Virtualized deployment" >&2
}

info()  {
   logger -s -t "fetch_compute_info.info" "$*"
}


error() {
   logger -s -t "fetch_compute_info.error" "$*"
   exit 1
}

verify_connectivity(){
   local ip=$1
   info "Verifying connectivity to $ip..."
   for i in $(seq 0 10); do
       if ping -c 1 -W 1 $ip > /dev/null; then
           info "$ip is reachable!"
           return 0
       fi
       sleep 1
   done
   error "Can not talk to $ip."
}

:${DEPLOY_TYPE:=''}

#Getoptions
whilegetopts ":d:i:a:h:v" optchar; do
   case "${optchar}" in
       i) installer_type=${OPTARG} ;;
       a) installer_ip=${OPTARG} ;;
       v) DEPLOY_TYPE="virt" ;;
       *) echo "Non-option argument: '-${OPTARG}'" >&2
          usage
          exit 2
          ;;
   esac
done

#set vars from env if not provided by user as options
installer_type=${installer_type:-$INSTALLER_TYPE}
installer_ip=${installer_ip:-$INSTALLER_IP}

if[ -z $installer_type ] || [ -z $installer_ip ]; then
   usage
   exit 2
fi

ssh_options="-oUserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

#Start fetching compute ip
if[ "$installer_type" == "fuel" ]; then
   verify_connectivity $installer_ip

   env=$(sshpass -p r00tme ssh 2>/dev/null $ssh_options root@${installer_ip} \
       'fuel env'|grep operational|head -1|awk '{print $1}') &> /dev/null
   if [ -z $env ]; then
       error "No operational environment detected in Fuel"
   fi
   env_id="${FUEL_ENV:-$env}"

   # Check if compute is alive (online='True')
   IPS=$(sshpass -p r00tme ssh 2>/dev/null $ssh_options root@${installer_ip} \
       "fuel node --env ${env_id} | grep compute | grep 'True\|  1' | awk -F\| '{print \$5}' " | \
       sed 's/ //g') &> /dev/null


elif[ "$installer_type" == "apex" ]; then
   echo "not implement now"
   exit 1

elif[ "$installer_type" == "compass" ]; then
   # need test
   verify_connectivity $installer_ip
   IPS=$(sshpass -p'root' ssh 2>/dev/null $ssh_options root@${installer_ip} \
       'mysql -ucompass -pcompass -Dcompass -e"select *  from cluster;"' \
       | awk -F"," '{for(i=1;i<NF;i++)if($i~/\"host[4-5]\"/) {print $(i+1);}}'  \
       | grep -oP "\d+.\d+.\d+.\d+")

elif[ "$installer_type" == "joid" ]; then
   echo "not implement now"
   exit 1

elif[ "$installer_type" == "foreman" ]; then
   echo "not implement now"
   exit 1

else
   error "Installer $installer is not supported by this script"
fi

if[ -z $IPS ]; then
   error "The compute node $IPS are not up. Please check that the POD is correctly deployed."
else
   echo "-------- all compute node ips: --------"
   touch $HOME/ips.log
   echo "$IPS" > $HOME/ips.log
   echo $IPS
fi

exit0
