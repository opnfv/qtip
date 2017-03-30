.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.


********
Overview
********

`QTIP`_ is the project for **Platform Performance Benchmarking** in `OPNFV`_. It aims to provide user a simple indicator
for performance, simple but supported by comprehensive testing data and transparent calculation formula.

QTIP introduces a concept called **QPI**, a.k.a. QTIP Performance Index, which aims to be a **TRUE** indicator of
performance. **TRUE** reflects the core value of QPI in four aspects

- *Transparent*: being an open source project, user can inspect all details behind QPI, e.g. formulas, metrics, raw data
- *Reliable*: the integrity of QPI will be guaranteed by traceability in each step back to raw test result
- *Understandable*: QPI is broke down into section scores, and workload scores in report to help user to understand
- *Extensible*: users may create their own QPI by composing the existed metrics in QTIP or extend new metrics


Benchmarks
==========

The builtin benchmarks of QTIP are located in ``<package_root>/benchmarks`` folder

- *QPI*: specifications about how an QPI is calculated and sources of metrics
- *metric*: performance metrics referred in QPI, currently it is categorized by performance testing tools
- *plan*: executable benchmarking plan which collects metrics and calculate QPI

.. _QTIP: https://wiki.opnfv.org/display/qtip
.. _OPNFV: https://www.opnfv.org/
