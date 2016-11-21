#!/bin/bash

envs="mongodb_url=mongodb://172.17.0.1:27017/  -e api_port=8000 -e swagger_url=http://testapi.qtip.openzero.net"
docker run --name testapi -id -e $envs -p 8000:8000 opnfv/testapi
