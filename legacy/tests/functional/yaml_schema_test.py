##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import os
import os.path
from pykwalify.core import Core


class TestClass:
    def test_schema_success(self):
        for root, dirs, files in os.walk("test_cases"):
            for name in files:
                print root + "/" + name
                if "_bm" in name:
                    schema = "tests/schema/test_bm_schema.yaml"
                if "_vm" in name:
                    schema = "tests/schema/test_vm_schema.yaml"
                c = Core(source_file=root + "/" + name, schema_files=[schema])
                c.validate(raise_exception=True)
