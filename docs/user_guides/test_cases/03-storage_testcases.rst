.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) <optionally add copywriters name>


.. two dots create a comment. please leave this logo at the top of each of your rst files.
image:: ../etc/opnfv-logo.png
  :height: 40
  :width: 200
  :alt: OPNFV
  :align: left
.. these two pipes are to seperate the logo from the first title
|
|

Storage test cases
=======================

The QTIP benchmark suite aims to evaluate storage components within an OPNFV platform. For Brahamaputra release, FIO would evaluate File System performance for the host machine. It will also test the I/O performance provided by the hypervisor(KVM) when Storage benchmarks are run inside VMs.

QTIP storage test cases consist of:

**1. FIO Job to benchmark baremetal file system performance**

**2. FIO Job to bechmark virtual machine file system performance**

**Note: For Brahmaputra release, only the Ephemeral Storage is being tested. For C release persistent block and object storage would be tested.**

The FIO Job would consist of:

1. A file size of 5GB
2. Random Read 50%, Random Write 50%
3. Direct I/O
4. Asynch I/O Engine
5. I/O Queue depth of 2
6. Block size :4K


For this Job, I/O per second would be measured along mean I/O latency to provide storage performance numbers.
