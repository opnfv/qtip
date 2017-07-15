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

from django.db import models
from django.urls import reverse

# Create your models here.


class Repo(models.Model):
    name = models.CharField(max_length=200, blank=False)
    github_link = models.URLField(unique=True)

    def get_absolute_url(self):
        return reverse('repo_update', args=[self.pk])


class Task(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    run_time = models.DurationField()
    repo = models.ForeignKey('Repo', on_delete=models.DO_NOTHING)
    log = models.TextField()
