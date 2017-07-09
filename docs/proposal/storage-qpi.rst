.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.


***********
Storage QPI
***********

The storage QPI gives user an overall score for storage performance.

The measurement is done by `StorPerf`_.

.. _StorPerf: https://wiki.opnfv.org/display/storperf

System Information
==================

System Information are environmental parameters and factors may affect storage performance:

+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| System Factors                 | Detail                                         | Extraction method                                                           |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Ceph Node List                 | List of nodes which has ceph-osd roles.        | Getting from return result of installer node list CLI command.              |
|                                | For example [node-2, node-3, node-4].          |                                                                             |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Ceph Client RDB Cache Mode     | None :"rds cache" ="false",                    | Getting from value of "rbd cache" and "rbd cache max dirty" keys            |
|                                | or write-through,                              | in client section of ceph configuration;To enable write-through mode,       |
|                                | or write-back.                                 | set rbd cache max dirty to 0.                                               |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Ceph Client RDB Cache Size     | The RBD cache size in bytes.Default is 32 MiB. | Getting from value of "rdb cache size" key in client section                |
|                                |                                                | of ceph configuration.                                                      |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Ceph OSD Tier Cache Mode       | Write-back or Readonly.                        | Getting from ceph CLI "ceph osd tier cache­mode" output info.               |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Use SSD Backed OSD Cache       | Yes or No                                      |  Getting from POD description and CEPH CLI "ceph-disk list" output info.    |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Use SSD For Journal            | Yes or No                                      | Getting from POD description and CEPH CLI "ceph-disk list" output info.     |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Ceph Cluster Network Bandwidth | 1G or 10G or 40G                               | Getting from physical interface information in POD description,             |
|                                |                                                | "ifconfig" output info on ceph osd node,                                    |
|                                |                                                | and value of "cluster network" key in global section of ceph configuration. |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Number of Testing VMs          | Number of VMs which is created,                | Recording the parameter when calling Storperf test case to run.             |
|                                | during running Storperf test case.             |                                                                             |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+
| Distribution of Testing VMS    | Number of VMs on each computer node,           | Recording the distribution  when runing Storperf test case.                 |
|                                | for example [(node-2: 1), (node-3: 2))]        |                                                                             |
+--------------------------------+------------------------------------------------+-----------------------------------------------------------------------------+

Baseline
========

Baseline is established by testing with a set of work loads:

- `Queue depth`_ (1, 2, 8)
- `Block size`_ (2KB, 8KB, 16KB)
- `Read write`_
  - sequential read
  - sequential write
  - random read
  - random write
  - random mixed read write 70/30

.. _Queue depth: http://fio.readthedocs.io/en/latest/fio_man.html#cmdoption-arg-iodepth
.. _Block size: http://fio.readthedocs.io/en/latest/fio_man.html#cmdoption-arg-blocksize
.. _Read write: http://fio.readthedocs.io/en/latest/fio_man.html#cmdoption-arg-readwrite

Metrics
=======

- Throughput: data transfer rate
- IOPS: I/O operations per second
- Latency: response time

Workload Scores
===============

For each test run, if an equivalent work load in baseline is available, a score will be calculated by comparing the
result to baseline.

Section Scores
==============

+-----------------+--------------------------------------------------------+-----------------------------------------+
| Section         | Detail                                                 | Indication                              |
+=================+========================================================+=========================================+
| IOPS            | Read write I/O Operation per second under steady state | Important for frequent storage access   |
|                 | Workloads : random read/write                          | such as event sinks                     |
+-----------------+--------------------------------------------------------+-----------------------------------------+
| Throughput      | Read write data transfer rate under steady state       | Important for high throughput services  |
|                 | Workloads: sequential read/write, block size 16KB      | such as video server                    |
+-----------------+--------------------------------------------------------+-----------------------------------------+
| Latency         | Average response latency under steady state            | Important for real time applications    |
|                 | Workloads: all                                         |                                         |
+-----------------+--------------------------------------------------------+-----------------------------------------+

Section score is the `geometric mean <https://en.wikipedia.org/wiki/Geometric_mean>`_ of all
workload score.

Storage QPI
===========

Storage QPI is the `weighted arithmetic mean <https://en.wikipedia.org/wiki/Weighted_arithmetic_mean>`_ of all section
scores.
