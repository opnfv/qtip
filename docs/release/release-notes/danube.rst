.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


This document provides the release notes for <RELEASE> of <COMPONENT>.

.. contents::
   :depth: 3
   :local:


Version history
---------------

+--------------------+--------------------+--------------------+--------------------+
| **Date**           | **Ver.**           | **Author**         | **Comment**        |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2017-03-14         | TODO(yujunz): tag  | Yujun Zhang        | First draft        |
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

A PoC of compute qpi benchmark plan is provided as a sample use case.

Available benchmark plans can be listed, shown and executed from `qtip-cli`, the command line interpreter of QTIP.

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | QTIP                                 |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/commit-ID**                   | qtip/TBD                             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Danube 1.0                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | TODO(yujunz): fill date              |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | OPNFV quality assurance              |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Version change
^^^^^^^^^^^^^^

Module version changes
~~~~~~~~~~~~~~~~~~~~~~

N/A

Document version changes
~~~~~~~~~~~~~~~~~~~~~~~~

N/A

Reason for version
^^^^^^^^^^^^^^^^^^
Feature additions
~~~~~~~~~~~~~~~~~

**JIRA BACK-LOG:**

** TODO(yujunz) pull data from JIRA **

+--------------------------------------+--------------------------------------+
| **JIRA REFERENCE**                   | **SLOGAN**                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
|                                      |                                      |
+--------------------------------------+--------------------------------------+
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Bug corrections
~~~~~~~~~~~~~~~

**JIRA TICKETS:**

** TODO(yujunz) pull data from JIRA **

+--------------------------------------+--------------------------------------+
| **JIRA REFERENCE**                   | **SLOGAN**                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
|                                      |                                      |
+--------------------------------------+--------------------------------------+
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Deliverables
------------

Software deliverables
^^^^^^^^^^^^^^^^^^^^^

** TODO(yujunz) docker image, pip package **

Documentation deliverables
^^^^^^^^^^^^^^^^^^^^^^^^^^

** TODO(yujunz) links to qtip document publish **

Known Limitations, Issues and Workarounds
=========================================

System Limitations
^^^^^^^^^^^^^^^^^^

None

Known issues
^^^^^^^^^^^^

** TODO(yujunz) pull data from JIRA **

**JIRA TICKETS:**

+--------------------------------------+--------------------------------------+
| **JIRA REFERENCE**                   | **SLOGAN**                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
|                                      |                                      |
+--------------------------------------+--------------------------------------+
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Workarounds
^^^^^^^^^^^

N/A

Test Result
===========

QTIP has undergone QA test runs with the following results:

+--------------------------------------+--------------------------------------+
| **TEST-SUITES**                      | **Results:**                         |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| qtip-verify-danube                   | 72/72 passed                         |
|                                      |                                      |
|                                      | 73% lines of code covered            |
+--------------------------------------+--------------------------------------+
| qtip-daily-fuel-zte-pod3-danube      | Last 7 build fails                   |
|                                      |                                      |
|                                      | blocked by the failure of zte-pod3   |
+--------------------------------------+--------------------------------------+

References
==========

For more information on the OPNFV Danube release, please see:

http://opnfv.org/danube
