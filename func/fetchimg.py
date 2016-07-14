##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import time

IMGSTORE="/iso_mount/opnfv_ci/master"

class FetchImg:

    def __init__(self):
        print 'Fetching Image!'
        print 'Fetching QTIP_VM Image'

    @staticmethod
    def download():
        time.sleep(2)
        os.system('mkdir -p Temp_Img')
        filepath = './Temp_Img/QTIP_CentOS.qcow2'
        imgstorepath = IMGSTORE+"/QTIP_CentOS.qcow2"
        if os.path.isfile(imgstorepath):
            os.system("ln -s %s %s" % (imgstorepath, filepath))
            print "QTIP_CentOS IMG exists locally. Skipping the download and using the file from IMG store"
        else:
            os.system(
            'wget http://artifacts.opnfv.org/qtip/QTIP_CentOS.qcow2 -P Temp_Img')

            while not os.path.isfile(filepath):
                time.sleep(10)
            print 'Download Completed!'
