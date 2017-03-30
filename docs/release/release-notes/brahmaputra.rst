.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

***********
Brahmaputra
***********

NOTE: The release note for OPNFV Brahmaputra is missing. This is a copy of the
README.

QTIP Benchmark Suite
====================

QTIP is a benchmarking suite intended to benchmark the following components of the OPNFV Platform:

1. Computing components
2. Networking components
3. Storage components

The efforts in QTIP are mostly focused on identifying

1. Benchmarks to run
2. Test cases in which these benchmarks to run
3. Automation of suite to run benchmarks within different test cases
4. Collection of test results

QTIP Framework can now be called:  (qtip.py).

The Framework can run 5 computing benchmarks:

1. Dhrystone
2. Whetstone
3. RamBandwidth
4. SSL
5. nDPI

These benchmarks can be run in 2 test cases:

1. VM vs Baremetal
2. Baremetal vs Baremetal

Instructions to run the script:

1. Download and source the OpenStack `adminrc` file for the deployment on which you want to create the VM for benchmarking
2. run `python qtip.py -s {SUITE} -b {BENCHMARK}`
3. run `python qtip.py -h` for more help
4. list of benchmarks can be found in the `qtip/test_cases` directory
5. SUITE refers to compute, network or storage

Requirements:

1. Ansible 1.9.2
2. Python 2.7
3. PyYAML

Configuring Test Cases:

Test cases can be found within the `test_cases` directory.
For each Test case, a Config.yaml file contains the details for the machines upon which the benchmarks would run.
Edit the IP and the Password fields within the files for the machines on which the benchmark is to run.
A robust framework that would allow to include more tests would be included within the future.

Jump Host requirements:

The following packages should be installed on the server from which you intend to run QTIP.

1: Heat Client
2: Glance Client
3: Nova Client
4: Neutron Client
5: wget
6: PyYaml

Networking

1: The Host Machines/compute nodes to be benchmarked should have public/access network
2: The Host Machines/compute nodes should allow Password Login

QTIP support for Foreman

{TBA}
