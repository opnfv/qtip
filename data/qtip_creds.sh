#! /bin/bash

DEST_IP=$1
echo $INSTALLER_TYPE
echo $INSTALLER_IP

case "$INSTALLER_TYPE" in
    apex)
        PSWD="vagrant";;
    fuel)
        PSWD="r00tme";;
    compass)
        PSWD="root";;
    joid)
        PSWD="joid";;
       *)
        echo "Unkown installer $INSTALLER_TYPE specified";;
esac
echo $PWD
sshoptions="-o StrictHostKeyChecking=no"
sshpass -p $PSWD scp $sshoptions ./data/QtipKey.pub root@$INSTALLER_IP:/root
sshpass -p $PSWD ssh $sshoptions root@$INSTALLER_IP "ssh-copy-id -i /root/QtipKey.pub root@$DEST_IP && rm -rf /root/QtipKey.pub"

