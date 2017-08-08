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
from multiprocessing import Process

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.utils import timezone

import forms
import models
import utils


class Dashboard(TemplateView):
    template_name = "bench/index.html"


class ReposView(LoginRequiredMixin, CreateView):
    model = models.Repo
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ReposView, self).get_context_data(**kwargs)
        context["repos"] = self.model.objects.all()
        context["template_role"] = "add"
        return context


class RepoUpdate(LoginRequiredMixin, UpdateView):
    model = models.Repo
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(RepoUpdate, self).get_context_data(**kwargs)
        context["repos"] = self.model.objects.all()
        context["template_role"] = "edit"
        return context


class Run(LoginRequiredMixin, View):
    template_name = 'bench/run.html'
    form_class = forms.TaskForm

    def get(self, request):
        task_form = self.form_class()
        return render(request, self.template_name, {'form': task_form})

    def post(self, request):
        task_form = self.form_class(request.POST)
        if task_form.is_valid():
            new_task = task_form.save()
            new_task.log.save("run_%s.log" % new_task.pk, ContentFile(''))
            p = Process(target=self.start_task, args=(new_task,))
            p.start()
            return redirect('tasks')
            p.join()

    def start_task(self, task):
        task = models.Task.objects.get(pk=task.pk)
        task.status = 'IP'
        task.save()
        with open(task.log.path, "a") as logfile:
            for line in utils.run(task.repo):
                logfile.write(line)
        now = timezone.now()
        task = models.Task.objects.get(pk=task.pk)
        task.end_time = now
        task.status = 'F'
        task.save()


class Logs(LoginRequiredMixin, ListView):
    model = models.Task


class TaskView(LoginRequiredMixin, DetailView):
    model = models.Task

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        try:
            with open(context['object'].log.path, "r") as log_file:
                context['log'] = log_file.read()
        except ValueError:
            context['log'] = "No log to show"
        return context
