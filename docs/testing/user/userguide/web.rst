.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


**********************
Web Portal User Manual
**********************

QTIP consists of different tools(metrics) to benchmark the NFVI. These metrics
fall under different NFVI subsystems(QPI's) such as compute, storage and network.
QTIP benchmarking tasks are built upon `Ansible`_ playbooks and roles.
QTIP web portal is a platform to expose QTIP as a benchmarking service hosted on a central host.


Running
=======

After setting up the web portal as instructed in config guide, cd into the `web` directory.

and run.

::

    python manage.py runserver 0.0.0.0


You can access the portal by logging onto `<host>:8000/bench/login/`

If you want to use port 80, you may need sudo permission.

::

    sudo python manage.py runserver 0.0.0.0:80

To Deploy on `wsgi`_, Use the Django `deployment tutorial`_


Features
========

After logging in You'll be redirect to QTIP-Web Dashboard. You'll see following menus on left.

    * Repos
    * Run Benchmarks
    * Tasks

Repo
----

    Repos are links to qtip `workspaces`_. This menu list all the aded repos. Links to new repos
    can be added here.

Run Benchmarks
--------------

    To run a benchmark, select the corresponding repo and run. QTIP Benchmarking service will clone
    the workspace and run the benchmarks. Inventories used are predefined in the workspace repo in the `/hosts/` config file.

Tasks
-----

    All running or completed benchmark jobs can be seen in Tasks menu with their status.


*New users can be added by Admin on the Django Admin app by logging into `/admin/'.*

.. _Ansible: https://www.ansible.com/
.. _wsgi: https://wsgi.readthedocs.io/en/latest/what.html
.. _deployment tutorial: https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
.. _workspaces: https://github.com/opnfv/qtip/blob/master/docs/testing/developer/devguide/ansible.rst#create-workspace
