from django import forms

import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['repo']
