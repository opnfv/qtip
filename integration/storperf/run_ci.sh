#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


source $WORKSPACE/integration/storperf/launch_containers.sh -t $INSTALLER_TYPE -n $NODE_NAME

docker exec qtip bash -c "/home/opnfv/repos/qtip/integration/storperf/prepare.sh"

docker exec qtip bash -c "/home/opnfv/repos/qtip/integration/storperf/start_job.sh"

docker exec qtip bash -c "/home/opnfv/repos/qtip/integration/storperf/cleanup.sh"

exit 0


