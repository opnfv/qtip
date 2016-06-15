.. two dots create a comment. please leave this logo at the top of each of your rst files.
.. image:: ../etc/opnfv-logo.png
  :height: 40
  :width: 200
  :alt: OPNFV
  :align: left
.. these two pipes are to seperate the logo from the first title
|
|

Roadmap for Release D
=====================

The development of QTIP has been paused after Brahmaputra release due the
shortage on resource. We will skip Colorado release and target for Release D.

The project will stick to the original scope as a benchmark platform and
continue to develop on existing framework.

We will focus on integrating more benchmark tools and supporting new technology
applied in OPNFV.

Another target is to attract more developers to the project by improving the
document, source code and development management.

Framework
---------

Error Handling
^^^^^^^^^^^^^^

The QTIP will be used against different environment. It is not possible to run
without any error all at once.

We will not be able to get rid of errors, but we may handle them gracefully.

Comprehensive error messages will help to locate the issue quickly and help user
to resolve them.

Declarative Playbook
^^^^^^^^^^^^^^^^^^^^

QTIP uses ansible for setting up the environment. It is nice and powerful tool
we will keep for Release D.

However, existing playbooks is full of hardcoded shell scripts which sometimes
will fail in specific OS distribution.

Although most system administrators will be familiar with shell script, it is
not easy to tell the purpose of a long command line at a glance.

Ansible's solution for these issues is to provide modules as an abstract layer
to handle the devergence, and it will also be more compact and easier to
understand. This is something we should leverage.

Scenario Configuration
^^^^^^^^^^^^^^^^^^^^^^

Currently the scenario configuration is hard coded and not able to be run under
different environment. The variables should be separated from the configuration
template.

Features
--------

Benchmarks
^^^^^^^^^^

1. vswitch perf
2. Cyclictest
3. Stress
4. Lmbench
5. Sar

Technology
^^^^^^^^^^

Some new technology is introduced into OPNFV and it would be good if we can
support them at the first time.

1. SR-IOV

Development Management
----------------------

We will make improvement on development management

1. Continuous Integration
2. Documentation
3. Issue Tracking
