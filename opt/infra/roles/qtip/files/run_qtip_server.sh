#!/bin/bash

envs="INSTALLER_TYPE=fuel -e INSTALLER_IP=10.20.0.2 -e NODE_NAME=zte-pod1"

# use ramfs to fix docker socket connection issue with overlay mode in centos
ramfs=/tmp/qtip/ramfs
if [ ! -d $ramfs ]; then
    mkdir -p $ramfs
fi

if [ ! -z $(df $ramfs | tail -n -1 | grep $ramfs) ]; then
    sudo mount -t tmpfs -o size=32M tmpfs $ramfs
fi

# enable contro path in docker
echo <<EOF > /tmp/ansible.cfg
[defaults]
callback_whitelist = profile_tasks
[ssh_connection]
control_path=/mnt/ramfs/ansible-ssh-%%h-%%p-%%r
EOF

docker run --name qtip -id -e $envs -p 5000:5000 -v $ramfs:/mnt/ramfs opnfv/qtip
docker cp qtip /tmp/ansible.cfg /home/opnfv/.ansible.cfg
