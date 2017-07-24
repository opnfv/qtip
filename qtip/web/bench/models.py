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
    git_link = models.URLField(unique=True)

    def get_absolute_url(self):
        return reverse('repo_update', args=[self.pk])

    def __str__(self):
        return "%s, %s" % (self.name, self.git_link)


class Task(models.Model):
    TASK_STATUS_CHOICES = (
        ('P', 'Pending'),
        ('IP', 'In progress'),
        ('F', 'Finished')
    )

    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=TASK_STATUS_CHOICES, default='P', max_length=20)
    end_time = models.DateTimeField(null=True)
    run_time = models.DurationField(null=True)
    repo = models.ForeignKey('Repo', on_delete=models.DO_NOTHING)
    log = models.FileField(upload_to='logs')

    def save(self, **kwargs):
        if self.end_time:
            self.run_time = self.end_time - self.start_time
        super(Task, self).save(kwargs)

    def get_absolute_url(self):
        return reverse('task_view', args=[self.pk])
