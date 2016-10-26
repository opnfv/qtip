#! /bin/bash

DEST_IP=$1
HOSTNAME=$(hostname)
sshoptions="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

case "$INSTALLER_TYPE" in
    fuel)
        ssh $sshoptions -i ./config/QtipKey root@$DEST_IP "sed -i '/root@$HOSTNAME/d' /root/.ssh/authorized_keys"
        ;;
esac



