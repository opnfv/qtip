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

from django.conf.urls import include, url

import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^repos/$', views.ReposView.as_view(), name='repos'),
    url('^repos/(?P<pk>\d+)$', views.RepoUpdate.as_view(), name='repo_update'),
]
