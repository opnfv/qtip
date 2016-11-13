.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 ZTE Corp.


***********
Compute QPI
***********

The compute QPI gives user an overall score for system compute performace.

Summary
=======

The compute QPI are calibrated a ZTE E9000 server as a baseline with score of 2500 points. Higher scores are better, with double the score indicating double the performance.
The compute QPI provides three different kinds of scores:
*Workload Scores
*Section Scores
*Compute QPI Scores

Baseline
========

ZTE E9000 server with an 2 Deca core Intel Xeon CPU processor,128560.0MB Memory.

Workload Scores
===============

Each time a workload is executed QTIP calculates a score based on the computer's performance compared to the baseline performance.

Section Scores
==============

QTIP uses a number of different tests, or workloads, to measure performance. The workloads are divided into five different sections:
Integer performance: Integer workloads measure the integer instruction performace of host or vm by performing Dhrystone test.
Floating point performance: Floating point workloads measure the floating point performance by performing Whetstone test.Floating point performance is especially important in video games, digital content creation applications.
Memory Performance: Memory workloads measure memory bandwidth by performing RamSpeed test.Software working with large amounts data relies on good memory performance.
DPI Performance:DPI workloads measure deep-packet inspection speed by performing nDPI test.Software working with network packet anlysis relies on DPI performance.
SSL Performance:SSL Performance workloads measure cipher speeds by using the OpenSSL tool.Software working with cipher large amounts data relies on SSL Performace.
A section score is the geometric mean of all the workload scores for workloads that are part of the section. These scores are useful for determining the performance of the computer in a particular area.

Compute QPI Scores
==================

The compute QPI score is the weighted arithmetic mean of the five section scores. The compute QPI score provides a way to quickly compare performance across different computers and different platforms without getting bogged down in details
