#!/bin/bash

envs="mongodb_url=mongodb://mongo:27017/  -e api_port=8000 -e swagger_url=http://testapi.qtip.openzero.net"
docker run --name testapi --link mongo:mongo -p 8000:8000 -e $envs -d opnfv/testapi
