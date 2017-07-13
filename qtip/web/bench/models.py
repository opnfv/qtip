# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Repo(models.Model):
    name = models.CharField(max_length=200, blank=False)
    github_link = models.URLField(unique=True)


class Task(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    run_time = models.DurationField()
    repo = models.ForeignKey('Repo', on_delete=models.DO_NOTHING)
    log = models.TextField()
