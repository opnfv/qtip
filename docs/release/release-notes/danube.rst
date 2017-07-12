.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

******
Danube
******

This document provides the release notes for Danube of QTIP.

.. contents::
   :depth: 3
   :local:

Version history
===============

+--------------------+--------------------+--------------------+--------------------+
| **Date**           | **Ver.**           | **Author**         | **Comment**        |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2017-03-30         | Danube 1.0         | Yujun Zhang        |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2017-05-04         | Danube 2.0         | Yujun Zhang        |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2017-07-14         | Danube 3.0         | Yujun Zhang        |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+

Important notes
===============

QTIP is totally reworked in Danube release. The legacy benchmarks released in Brahmaputra (compute, network and storage)
are deprecated.

Summary
=======

QTIP Danube release introduces **QPI**, a.k.a. QTIP Performance Index, which is calculated from metrics collected in
performance tests.

A PoC of compute performance benchmark plan is provided as a sample use case.

Available benchmark plans can be listed, shown and executed from command line or over API.

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | QTIP                                 |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/commit-ID**                   | qtip/danube.3.0                      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Tag update only                      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | 2017-07-14                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | OPNFV quality assurance              |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Version change
--------------

New in Danube 3.0
^^^^^^^^^^^^^^^^^

* No change in QTIP itself
* Validated on OPNFV Danube latest release

New in Danube 2.0
^^^^^^^^^^^^^^^^^

* Bug fix in regex of ssl

Module version changes
^^^^^^^^^^^^^^^^^^^^^^

The following Python packages are used in this release::

   ansible==2.1.2.0
   click==6.7
   connexion==1.1.5
   Jinja2==2.9.5
   numpy==1.12.1
   paramiko==2.1.2
   pbr==2.0.0
   prettytable==0.7.2
   six==1.10.0
   PyYAML==3.12


It is considered as a baseline for future releases.

Reason for version
------------------

Features additions
^^^^^^^^^^^^^^^^^^

* Compute QPI (QTIP Performance Index) specification and benchmarking plan
* Command line interface
* API server

Framework evolution
^^^^^^^^^^^^^^^^^^^

The following components are implemented and integrated

* Native runner
* File loader
* Ansible driver
* Logfile collector
* Grep parser
* Console reporter

See JIRA for full `change log <https://jira.opnfv.org/jira/secure/ReleaseNote.jspa?projectId=10308&version=10555>`_

Deliverables
------------

Software
^^^^^^^^

- `QTIP Docker image <https://hub.docker.com/r/opnfv/qtip>`_ (tag: danube.3.0)
- `QTIP Docker image <https://hub.docker.com/r/opnfv/qtip>`_ (tag: danube.2.0)
- `QTIP Docker image <https://hub.docker.com/r/opnfv/qtip>`_ (tag: danube.1.0)

Documentation
^^^^^^^^^^^^^

- `Installation & Configuration <http://docs.opnfv.org/en/stable-danube/qtip/docs/testing/user/configguide>`_
- `User Guide <http://docs.opnfv.org/en/stable-danube/submodules/qtip/docs/testing/user/userguide>`_
- `Developer Guide <http://docs.opnfv.org/en/stable-danube/submodules/qtip/docs/testing/developer/devguide>`_

Known Limitations, Issues and Workarounds
=========================================

Limitations
-----------

- The compute benchmark plan is hard coded in native runner
- Baseline for Compute QPI is not created yet, therefore scores are not available

Known issues
------------

* QTIP-230 - logger warns about socket /dev/log when running in container

Test Result
===========

QTIP has undergone QA test runs with the following results:

+---------------------------------------------------+--------------------------------------+
| **TEST-SUITES**                                   | **Results:**                         |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
| qtip-verify-danube                                | 94/94 passed                         |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
| qtip-os-nosdn-kvm-ha-zte-pod3-daily-danube        | passed                               |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
| qtip-os-nosdn-nofeature-ha-zte-pod3-daily-danube  | passed                               |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
| qtip-os-odl_l2-nofeature-ha-zte-pod1-daily-danube | passed                               |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
