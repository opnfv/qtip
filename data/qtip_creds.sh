#! /bin/bash

DEST_IP=$1
echo $INSTALLER_TYPE
echo $INSTALLER_IP
sshoptions="-o StrictHostKeyChecking=no"
case "$INSTALLER_TYPE" in
    apex)
        PSWD="vagrant"
        ;;
    fuel)
        PSWD="r00tme"
        sshpass -p $PSWD scp $sshoptions ./data/QtipKey.pub root@$INSTALLER_IP:/root
        sshpass -p $PSWD scp $sshoptions ./data/QtipKey root@$INSTALLER_IP:/root
        sshpass -p $PSWD ssh $sshoptions root@$INSTALLER_IP "ssh-copy-id -i /root/QtipKey.pub root@$DEST_IP && rm -rf /root/QtipKey && rm -rf /root/QtipKey.pub"
        ;;
    compass)
        PSWD="root"
        sshpass -p $PSWD scp $sshoptions ./data/QtipKey.pub root@$INSTALLER_IP:/root
        sshpass -p $PSWD scp $sshoptions ./data/QtipKey root@$INSTALLER_IP:/root
        sshpass -p $PSWD ssh $sshoptions root@$INSTALLER_IP "ssh-copy-id -i /root/QtipKey.pub root@$DEST_IP && rm -rf /root/QtipKey && rm -rf /root/QtipKey.pub"
        ;;
    joid)
        PSWD="joid";;
       *)
        echo "Unkown installer $INSTALLER_TYPE specified";;
esac
