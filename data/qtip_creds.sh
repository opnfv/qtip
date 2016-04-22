#! /bin/bash

DEST_IP=$1
echo $INSTALLER_TYPE
echo $INSTALLER_IP
sshoptions="-o StrictHostKeyChecking=no"
case "$INSTALLER_TYPE" in
    apex)
        scp $sshoptions -i $APEX_KEY ./data/QtipKey.pub stack@$INSTALLER_IP:/home/stack
        scp $sshoptions -i $APEX_KEY ./data/QtipKey stack@$INSTALLER_IP:/home/stack
        ssh $sshoptions -i $APEX_KEY stack@$INSTALLER_IP "ssh-copy-id $sshoptions -i /home/stack/QtipKey.pub heat-admin@$DEST_IP && rm -rf /home/stack/QtipKey && rm -rf /home/stack/QtipKey.pub"
        ;;
    fuel)
        PSWD="r00tme"
        sshpass -p $PSWD scp $sshoptions ./data/QtipKey.pub root@$INSTALLER_IP:/root
        sshpass -p $PSWD scp $sshoptions ./data/QtipKey root@$INSTALLER_IP:/root
        sshpass  -p $PSWD ssh $sshoptions root@$INSTALLER_IP "cat /root/QtipKey.pub | ssh root@$DEST_IP 'cat >> .ssh/authorized_keys'"
        sshpass  -p $PSWD ssh $sshoptions root@$INSTALLER_IP "rm -rf /root/QtipKey && rm -rf /root/QtipKey.pub"
        ;;
    compass)
        PSWD="root"
        sshpass -p $PSWD scp $sshoptions ./data/QtipKey.pub root@$INSTALLER_IP:/root
        sshpass -p $PSWD scp $sshoptions ./data/QtipKey root@$INSTALLER_IP:/root
        sshpass -p $PSWD ssh $sshoptions root@$INSTALLER_IP "ssh-copy-id $sshoptions -i /root/QtipKey.pub root@$DEST_IP && rm -rf /root/QtipKey && rm -rf /root/QtipKey.pub"
        ;;
    joid)
        PSWD="joid";;
       *)
        echo "Unkown installer $INSTALLER_TYPE specified";;
esac
