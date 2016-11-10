#!/bin/bash

envs="INSTALLER_TYPE=fuel -e INSTALLER_IP=10.20.0.2 -e NODE_NAME=zte-pod1"
docker run --name qtip -id -e $envs -p 5000:5000 opnfv/qtip
