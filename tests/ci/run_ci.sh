#! /bin/bash
##############################################################################
# Copyright (c) 2017 ZTE corp. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

export CI_DEBUG=false

cd ${QTIP_DIR}/qtip/runner/
python runner.py -d ${HOME}/qtip/results/ -b all
