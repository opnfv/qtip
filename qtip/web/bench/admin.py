##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

import models

# Register your models here.


admin.site.register(models.Repo)
admin.site.register(models.Task)
