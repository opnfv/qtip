#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE corp. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

DEST_IP=$1
PRIVATE_KEY=$2
PUBLIC_KEY=$3
sshoptions="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

case "$INSTALLER_TYPE" in
    fuel)
        ssh $sshoptions -i $PRIVATE_KEY root@$DEST_IP "sed -i '/$PUBLIC_KEY/d' /root/.ssh/authorized_keys"
        ;;
esac
