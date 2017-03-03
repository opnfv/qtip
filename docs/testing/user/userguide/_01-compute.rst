.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2015 Dell Inc.
.. (c) 2016 ZTE Corp.


Compute Suite
=============

Introduction
------------

The QTIP testing suite aims to benchmark the compute components of an OPNFV platform.
Such components include, the CPU performance, the memory performance.
Additionally virtual computing performance provided by the Hypervisor (KVM) installed as part of OPNFV platforms would be benchmarked too.

The test suite consists of both synthetic and application specific benchmarks to test compute components.

All the compute benchmarks could be run in 2 scenarios:

1. On Baremetal Machines provisioned by an OPNFV installer (Host machines)
2. On Virtual Machines brought up through OpenStack on an OPNFV platform

Note: The Compute benchmank suite constains relatively old benchmarks such as dhrystone and whetstone. The suite would be updated for better benchmarks such as Linbench for the OPNFV C release.

Benchmarks
----------

The benchmarks include:

Dhrystone 2.1
^^^^^^^^^^^^^^^^

Dhrystone is a synthetic benchmark for measuring CPU performance. It uses integer calculations to evaluate CPU capabilities.
Both Single CPU performance is measured along multi-cpu performance.


Dhrystone, however, is a dated benchmark and has some short comings.
Written in C, it is a small program that doesn't test the CPU memory subsystem.
Additionally, dhrystone results could be modified by optimizing the compiler and insome cases hardware configuration.

References: http://www.eembc.org/techlit/datasheets/dhrystone_wp.pdf

Whetstone
^^^^^^^^^^^^

Whetstone is a synthetic benchmark to measure CPU floating point operation performance.
Both Single CPU performance is measured along multi-cpu performance.

Like Dhrystone, Whetstone is a dated benchmark and has short comings.

References:

http://www.netlib.org/benchmark/whetstone.c

OpenSSL Speed
^^^^^^^^^^^^^^^^

OpenSSL Speed can be used to benchmark compute performance of a machine. In QTIP, two OpenSSL Speed benchmarks are incorporated:
1. RSA signatunes/sec signed by a machine
2. AES 128-bit encryption throughput for a machine for cipher block sizes

References:

https://www.openssl.org/docs/manmaster/apps/speed.html

RAMSpeed
^^^^^^^^

RAMSpeed is used to measure a machine's memory perfomace.
The problem(array)size is large enough to ensure Cache Misses so that the main machine memory is used.
INTmem and FLOATmem benchmarks are executed in 4 different scenarios:

a. Copy: a(i)=b(i)
b. Add:  a(i)=b(i)+c(i)
c. Scale:  a(i)=b(i)*d
d. Tniad: a(i)=b(i)+c(i)*d

INTmem uses integers in these four benchmarks whereas FLOATmem uses floating points for these benchmarks.

References:

http://alasir.com/software/ramspeed/

https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/W51a7ffcf4dfd_4b40_9d82_446ebc23c550/page/Untangling+memory+access+measurements

DPI
^^^

nDPI is a modified  variant of  OpenDPI, Open source Deep packet Inspection, that is maintained by ntop.
An example application called *pcapreader* has been developed and is available for use along nDPI.

A sample .pcap file is passed to the *pcapreader* application.
nDPI classifies traffic in the pcap file into different categories based on string matching.
The *pcapreader* application provides a throughput number for the rate at which traffic was classified, indicating a machine's computational performance.
The results are run 10 times and an average is taken for the obtained number.

*nDPI may provide non consistent results and was added to Brahmaputra for experimental purposes*

References:

http://www.ntop.org/products/deep-packet-inspection/ndpi/

http://www.ntop.org/wp-content/uploads/2013/12/nDPI_QuickStartGuide.pdf
