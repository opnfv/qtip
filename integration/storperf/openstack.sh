#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

delete_storperf_stack()
{
    echo "Checking for an existing stack"
    STACK_ID=`openstack stack list | grep StorPerfAgentGroup | awk '{print $2}'`
    if [[ ! -z $STACK_ID ]];then
        openstack stack delete --yes --wait StorPerfAgentGroup
    fi
}

load_ubuntu_image()
{
    echo "Checking for Ubuntu 16.04 image in Glance"
    IMAGE=`openstack image list | grep "Ubuntu 16.04 x86_64"`
    if [[ -z "$IMAGE" ]];then
        cd $WORKSPACE
        if [[ ! -f ubuntu-16.04-server-cloudimg-amd64-disk1.img ]];then
            echo "download Ubuntu 16.04 image"
            wget https://cloud-images.ubuntu.com/releases/16.04/release/ubuntu-16.04-server-cloudimg-amd64-disk1.img
            wget https://cloud-images.ubuntu.com/releases/16.04/release/MD5SUMS
            checksum=$(cat ./MD5SUMS |grep ubuntu-16.04-server-cloudimg-amd64-disk1.img | md5sum -c)
            if [[ $checksum =~ 'FAILED' ]];then
                echo "Check image md5sum failed. Exit!"
                exit 1
            fi
        fi

        echo "Create openstack image Ubuntu 16.04"
        openstack image create "Ubuntu 16.04 x86_64" --disk-format qcow2 --public \
        --container-format bare --file $WORKSPACE/ubuntu-16.04-server-cloudimg-amd64-disk1.img
    fi

    openstack image show "Ubuntu 16.04 x86_64"
}


create_storperf_flavor()
{
    echo "Checking for StorPerf flavor"
    openstack flavor delete storperf
    FLAVOR=`openstack flavor list | grep "storperf"`
    if [[ -z "$FLAVOR" ]];then
        openstack flavor create storperf \
            --id auto \
            --ram 2048 \
            --disk 4 \
            --vcpus 2
    fi
    openstack flavor show storperf
}


nova_vm_mapping()
{
    rm ./nova_vm.json
    openstack server list --name storperf-agent -c ID -c Host --long -f json > nova_vm.json
}