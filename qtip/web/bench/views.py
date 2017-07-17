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

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView

import models

# from django.shortcuts import render

# Create your views here.


class ReposView(LoginRequiredMixin, CreateView):
    model = models.Repo
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ReposView, self).get_context_data(**kwargs)
        context["repos"] = self.model.objects.all()
        return context


class RepoUpdate(LoginRequiredMixin, UpdateView):
    model = models.Repo
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(RepoUpdate, self).get_context_data(**kwargs)
        context["repos"] = self.model.objects.all()
        return context
