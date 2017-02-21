.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2015 Dell Inc.
.. (c) 2016 ZTE Corp.


Network Suite
=============

QTIP uses IPerf3 as the main tool for testing the network throughput.
There are three tests that are run through the QTIP framework.

**1. Network throughput between two compute nodes**

**2. Network Throughput between two VMs on the same compute node**

**3. Network Throughput between two VMs on different compute nodes**


Network throughput between two compute nodes
-----------------------------------------------

For the throughput between two compute nodes, Iperf3 is installed on the compute nodes comprising the systems-under-test.
One of the compute nodes is used as a server and the other as a client.
The client pushes traffic to the server for a duration specified by the user in the configuration file for Iperf3.


These files can be found in the "benchmarks/testplan/{POD}/network/" directory.
The bandwidth is limited by the physical link layer speed connecting the two compute nodes.
The result file includes the b/s bandwidth and the CPU usage for both the client and server.

Network throughput between two VMs on the same compute node
--------------------------------------------------------------

QTIP framework sets up a stack with a private network, security groups, routers and attaches two VMs to this network.
Iperf3 is installed on the VMs and one is assigned the role of client while the other VM serves as a server.
Traffic is pushed over the QTIP private network between the two VMs.
A closer look is  needed to see how the traffic actually flows between the VMs in this configuration to understand what is happening to the packet as it traverses the OpenStack virtual network.

The packet originates from VM1 and its sent to the Linux bridge via a tap interface where the security groups are written.
Afterwards the packet is forwarded to the Integration bridge (br-int) via a patch port.
Since VM2 is also connected to the Integration bridge in a similar manner as VM1, the packet gets forwarded to the linux bridge connecting VM2.
After the Linux bridge the packet is sent to VM2 and is received by the Iperf3 server.
Since no physical link is involved in this topology, only the OVS (Integration bridge) (br-int) is being benchmarked.


Network throughput between two VMs on different compute nodes
--------------------------------------------------------------


As in case 2, QTIP framework sets up a stack with a private network, security groups, routers, and two VMs which are attached to the created network. However, the two VMs are spawned up on different compute nodes.

Since the VMs  are spawned on different nodes, the traffic involves additional paths.

The traffic packet leaves the client VM and makes its way to the Integration Bridge (br-int) as in the previous case through a linux bridge and a patch port.
The integration bridge (br-int) forwards the packet to the the tunneling bridge (br-tun) where the packet is encapsulated based on the tunneling protocol used (GRE/VxLAN).
The packet then moves onto the physical link through the ethernet bridge (br-eth).

On the receiving compute node, the packet arrives at ethernet bridge(br-eth) through the physical link.
This packet then moves to the tunneling bridge (br-tun) where the packet is decapsulated.
The packet then moves onto the internal bridge (br-int) and finally moves through a patch port into the linux bridge and eventually to the VM where it is received by the Iperf server application.
