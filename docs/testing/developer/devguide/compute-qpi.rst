.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 ZTE Corp.


***********
Compute QPI
***********

The compute QPI gives user an overall score for system compute performace.

Summary
=======

The compute QPI are calibrated a ZTE `E9000 <http://www.zte.com.cn/global/products/cocloud/cloud_computing/cloud_infrastructure/cloud_hw/429552>`_ server as a baseline with score of 2500 points.
Higher scores are better, with double the score indicating double the performance.
The compute QPI provides three different kinds of scores:

* Workload Scores
* Section Scores
* Compute QPI Scores

Baseline
========

ZTE E9000 server with an 2 Deca core Intel Xeon CPU processor,128560.0MB Memory.

Workload Scores
===============

Each time a workload is executed QTIP calculates a score based on the computer's performance
compared to the baseline performance.

Section Scores
==============

QTIP uses a number of different tests, or workloads, to measure performance.
The workloads are divided into five different sections:

+-----------------+--------------------------------------------------------+------------------------------------------+
| Section         | Detail                                                 | Indication                               |
+=================+========================================================+==========================================+
| Arithmetic      | Arithmetic workloads measure integer operations        | Software with heavy calculation tasks.   |
|                 | floating point operations and mathematical functions   |                                          |
|                 | with whetstone and dhrystone instructions.             |                                          |
+-----------------+--------------------------------------------------------+------------------------------------------+
| Memory          | Memory workloads measure memory transfer performance   | Software working with large scale data   |
|                 | with RamSpeed test.                                    | operation.                               |
+-----------------+--------------------------------------------------------+------------------------------------------+
| DPI             | DPI workloads measure deep-packet inspection speed by  | Software working with network packet     |
|                 | performing nDPI test.                                  | analysis relies on DPI performance.      |
+-----------------+--------------------------------------------------------+------------------------------------------+
| SSL             | SSL Performance workloads measure cipher speeds by     | Software working with cipher large       |
|                 | using the OpenSSL tool.                                | amounts data relies on SSL Performance.  |
+-----------------+--------------------------------------------------------+------------------------------------------+

A section score is the `geometric mean <https://en.wikipedia.org/wiki/Geometric_mean>`_ of all the workload scores for workloads
that are part of the section. These scores are useful for determining the performance of
the computer in a particular area.

Compute QPI Scores
==================

The compute QPI score is the `weighted arithmetic mean <https://en.wikipedia.org/wiki/Weighted_arithmetic_mean>`_ of the five section scores.
The compute QPI score provides a way to quickly compare performance across different
computers and different platforms without getting bogged down in details.
