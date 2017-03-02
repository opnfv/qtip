#! /bin/bash

DEST_IP=$1
PRIVATE_KEY=$2
PUBLIC_KEY=$2.pub
KEYNAME=$(basename $PRIVATE_KEY)

echo $INSTALLER_TYPE
echo $INSTALLER_IP
sshoptions="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
case "$INSTALLER_TYPE" in
    apex)
        scp $sshoptions -i $APEX_KEY $PUBLIC_KEY stack@$INSTALLER_IP:/home/stack
        scp $sshoptions -i $APEX_KEY $PRIVATE_KEY stack@$INSTALLER_IP:/home/stack
        ssh $sshoptions -i $APEX_KEY stack@$INSTALLER_IP "ssh-copy-id $sshoptions -i /home/stack/$KEYNAME.pub heat-admin@$DEST_IP && rm -rf /home/stack/$KEYNAME && rm -rf /home/stack/$KEYNAME.pub"
        ;;
    fuel)
        PSWD="r00tme"
        sshpass -p $PSWD scp $sshoptions $PUBLIC_KEY root@$INSTALLER_IP:/root
        sshpass -p $PSWD scp $sshoptions $PRIVATE_KEY root@$INSTALLER_IP:/root
        sshpass -p $PSWD ssh $sshoptions root@$INSTALLER_IP "grep -q '\-F /dev/null ' /usr/bin/ssh-copy-id || sed -i 's/\(ssh -i.*$\)/\1\n -F \/dev\/null \\\/g' `which ssh-copy-id`"
        sshpass -p $PSWD ssh $sshoptions root@$INSTALLER_IP "ssh-copy-id $sshoptions -i /root/$KEYNAME root@$DEST_IP && rm -rf /root/$KEYNAME && rm -rf /root/$KEYNAME.pub"
        ;;
    compass)
        PSWD="root"
        sshpass -p $PSWD scp $sshoptions $PUBLIC_KEY root@$INSTALLER_IP:/root
        sshpass -p $PSWD scp $sshoptions $PRIVATE_KEY root@$INSTALLER_IP:/root
        sshpass -p $PSWD ssh $sshoptions root@$INSTALLER_IP "ssh-copy-id $sshoptions -i /root/$KEYNAME.pub root@$DEST_IP && rm -rf /root/$KEYNAME && rm -rf /root/$KEYNAME.pub"
        ;;
    joid)
        PSWD="joid";;
       *)
        echo "Unkown installer $INSTALLER_TYPE specified";;
esac