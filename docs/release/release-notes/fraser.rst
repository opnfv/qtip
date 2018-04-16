.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

******
Fraser
******

This document provides the release notes of QTIP for OPNFV Fraser release

.. contents::
   :depth: 3
   :local:

Version history
===============

+--------------------+--------------------+--------------------+--------------------+
| **Date**           | **Ver.**           | **Author**         | **Comment**        |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2018-04-25         | Fraser 1.0         | Zhihui Wu          |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+

Summary
=======

QTIP Fraser release supports the compute QPI(QTIP Performance Index) for **VNF**. In order to
simplify the implementation, a Ubuntu 16.04 virtual machine is regarded as a simple VNF. The
end users can try to run QTIP with a **real** VNF.

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | QTIP                                 |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/commit-ID**                   | qtip/opnfv-6.0.0                     |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | stable version                       |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | 2018-04-18                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | release with OPNFV cycle             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Version change
--------------

Python packaging tool
^^^^^^^^^^^^^^^^^^^^^

Pipenv is the officially recommended Python packaging tool from Python.org.

Pipenv uses the ``Pipfile`` and ``Pipfile.lock`` instead of ``requirements.txt`` to manage
the dependency packages.

Reason for version
------------------

Features additions
^^^^^^^^^^^^^^^^^^

* Support the compute QPI for **VNF**

Deliverables
------------

Software
^^^^^^^^

- `QTIP Docker image <https://hub.docker.com/r/opnfv/qtip>`_ (tag: opnfv-6.0.0)

Documentation
^^^^^^^^^^^^^

- `Installation & Configuration <http://docs.opnfv.org/en/stable-fraser/qtip/docs/testing/user/configguide>`_
- `User Guide <http://docs.opnfv.org/en/stable-fraser/submodules/qtip/docs/testing/user/userguide>`_
- `Developer Guide <http://docs.opnfv.org/en/stable-fraser/submodules/qtip/docs/testing/developer/devguide>`_

Known Limitations, Issues and Workarounds
=========================================

Limitations
-----------

N/A

Known issues
------------

N/A
