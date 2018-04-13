.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


***************************************
Web Portal for Benchmarking Services
***************************************

QTIP consists of different tools(metrics) to benchmark the NFVI. These metrics
fall under different NFVI subsystems(QPI's) such as compute, storage and network.
QTIP benchmarking tasks are built upon `Ansible`_ playbooks and roles.
QTIP web portal is a platform to expose QTIP as a benchmarking service hosted on a central host.

Framework
=========

The web travel has been developed on Python `Django`_ framework. Dig into the documentation to learn about Django.

Design
======

Django is a MTV (Model Template View) framework. Database objects are mapped to models in ``models.py``. Views handle the
requests from client side and interact with database using Django ORM. Templates are responsible for
UI rendering based on response context from Views.

Models
------

Repo
~~~~

Model for `workspace`_ repos

::

    Repo:
        name
        git_link


Task
~~~~

Tasks keep track of every benchmark run through QTIP-Web Services. Whenever you run a benchmark,
a new task is created which keep track of time stats and log task progress and ansible output for
the respective playbook.

::

    Task
        start_time
        end_time
        status
        run_time
        repo
        log


Views
-----

Dashboard
~~~~~~~~~

    - Base class - TemplateVIew

Class based view serving as home page for the application.


ReposView
~~~~~~~~~

    - Base class - LoginRequiredMixin, CreateView

Class based view for listing and add new repos


RepoUpdate
~~~~~~~~~~

    - Base class - LoginRequiredMixin, UpdateView

Class based View for listing and updating an existing repo details.

*Both ReposView and RepoUpdate View use same template ``repo_form.html``. The context has an extra variable ``template_role`` which is used to distinguish if repo form is for create or edit operation.*


Run
~~~

    - Base class - LoginRequiredMixin, View
    - template name - run.html

Class based View for adding new task and run benchmark based on task details. The logs are saved
in ``logs/run_<log_id>`` directory.


.. _Ansible: https://www.ansible.com/
.. _Django: https://docs.djangoproject.com/en/1.11/
.. _workspace: https://github.com/opnfv/qtip/blob/master/docs/testing/developer/devguide/ansible.rst#create-workspace
