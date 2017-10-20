.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

*********
Euphrates
*********

This document provides the release notes of QTIP for OPNFV Euphrates release

.. contents::
   :depth: 3
   :local:

Version history
===============

+--------------------+--------------------+--------------------+--------------------+
| **Date**           | **Ver.**           | **Author**         | **Comment**        |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2017-10-20         | Euphrates 1.0      | Yujun Zhang        |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+

Summary
=======

QTIP Euphrates release continues working on **QPI**, a.k.a. QTIP Performance Index, which is calculated from metrics
collected in performance tests.

Besides compute performance benchmark, QTIP has integrated OPNFV storperf for storage performance benchmarking.

A PoC of web portal is implemented as the starting point of Benchmarking as a Service.

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | QTIP                                 |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/commit-ID**                   | qtip/euphrates.1.0                   |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | stable version                       |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | 2017-10-20                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | release with OPNFV cycle             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Version change
--------------

Module version changes
^^^^^^^^^^^^^^^^^^^^^^

The following Python packages are used in this release::

   humanfriendly==4.4.1
   connexion==1.1.11
   Jinja2==2.9.6
   Django==1.11.5
   asq==1.2.1
   six==1.11.0
   ansible==2.4.0.0
   requests==2.18.4
   prettytable==0.7.2
   numpy==1.13.1
   click==6.7
   pbr==3.1.1
   PyYAML==3.12

It is considered as a baseline for future releases.

Reason for version
------------------

Features additions
^^^^^^^^^^^^^^^^^^

* Storage QPI (QTIP Performance Index) specification and benchmarking project

Framework evolution
^^^^^^^^^^^^^^^^^^^

Ansible is used as the backbone of QTIP framework. Not only the main testing procedure is built as Ansible roles, but
also the inventory discovery is implemented as Ansible module, the calculation and collection actions are Ansible
plugins. Even the testing project itself is generated using jinja2 template rendering driven by Ansible.

Deliverables
------------

Software
^^^^^^^^

- `QTIP Docker image <https://hub.docker.com/r/opnfv/qtip>`_ (tag: euphrates.1.0)

Documentation
^^^^^^^^^^^^^

- `Installation & Configuration <http://docs.opnfv.org/en/stable-euphrates/qtip/docs/testing/user/configguide>`_
- `User Guide <http://docs.opnfv.org/en/stable-euphrates/submodules/qtip/docs/testing/user/userguide>`_
- `Developer Guide <http://docs.opnfv.org/en/stable-euphrates/submodules/qtip/docs/testing/developer/devguide>`_

Known Limitations, Issues and Workarounds
=========================================

Limitations
-----------

- Supporting on legacy OPNFV fuel installer is no longer maintained.

Known issues
------------

Test Result
===========

QTIP has undergone QA test runs with the following results:

+---------------------------------------------------+--------------------------------------+
| **TEST-SUITES**                                   | **Results:**                         |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
| qtip-verify-euphrates                             | 53/53 passed, 86% lines coverage     |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
| qtip-compute-apex-euphrates                       | passed                               |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
| qtip-storage-apex-euphrates                       | passed                               |
|                                                   |                                      |
+---------------------------------------------------+--------------------------------------+
