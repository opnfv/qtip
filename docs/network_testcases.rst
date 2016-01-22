NETWORK THROUGHPUT TESTCASE

QTIP uses IPerf3 as the main tool for testing the network throughput.
There are two tests that are run through the QTIP framework.

Network Throughput for VMs
Network Throughput for Compute Nodes

For the throughout of the compute nodes we simply go into the systems-under-test
 and install iperf3 on the nodes. One of the SUTs is used a server and the
 other as a client. The client pushes traffic to the server for a duration specified by
 the user
 configuration file for iperf. These files can be found in the test_cases/{POD}/network/
 directory. The bandwidth is limited only by the physical link layer speed available to the server.
 The result file inlcudes the b/s bandwidth and the CPU usage for both the client and server.

For the VMs we are running two topologies through the framework.

1: VMs on the same compute nodes
2: VMs on different compute nodes

QTIP framework sets up a stack with a private network, security groups, routers and attaches the VMs to this network. Iperf3 is installed
 on the VMs and one is assigned the role of client while other serves as a server. Traffic is pushed
 over the QTIP private network between the VMs. A closer look in needed to see how the traffic actually
 flows between the VMs in this configuration to understand what is happening to the packet as traverses
 the openstack network.

The packet originates from VM1 and its sent to the linux bridge via a tap interface where the security groups
 are written. Afterwards the packet is forwarded to the Integration bridge via a patch port. Since VM2 is also connected
 to the Integration bridge in a similar manner as VM1 so the packet gets forwarded to the linux bridge connecting
 VM2. After the linux bridge the packet is sent to VM2 and is recieved by the Iperf3 server. Since no physical link is
 involved in this topology, only the OVS (Integration bridge) is being benchmarked and we are seeing bandwidth in the range
 of 14-15 Gbps.

For the topology where the VMs are spawned on different compute nodes, the path the packet takes becomes more cumbersome.
The packet leaves a VM and makes its way to the Integration Bridge as in the first topology however the integration bridge 
forwards the packet to the physical link through the ethernet bridge. The packet then gets a VLAN/Tunnel depending on the network
and is forwarded to the particular Compute node where the second VM is spwaned. The packets enter the compute node through the physical
ethernet port and makes its way to the VM through the integration bridge and linux bridge. As seen here the path is much more involved
even when discussed without the mention of overheads faced at all the internfaces so we are seeing the results in the range of 2 Gbps.


