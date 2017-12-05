.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 ZTE Corp.


*****************************
Network Performance Indicator
*****************************

Sridhar K. N. Rao, Spirent Communications

Network performance is an important measure that should be considered for design and deployment of virtual network functions in the cloud. In this document, we propose an indicator for network performance. We consider following parameters for the indicator.

#. The network throughput.
#. The network delay
#. Application SLAs
#. The topology - Path Length and Number of Virtual Network-Elements.
#. Network Virtualization - Vxlan, GRE, VLAN, etc.

The most commonly used, and well measured, network-performance metrics are throughput and delay. However, considering the NFV environments, we add additional metrics to come up with a single indicator value. With these additional metrics, we plan to cover various deployment scenarios of the virtualized network functions.

The proposed network performance indicator value ranges from 0 - 1.0

As majority of indicators, these values should mainly be used for comparative analysis, and not to be seen as a absolute indicator.

Note: Additional parameters such as - total load on the network - can be considered in future.

The network performance indicator (I) can be represented as:

:math:`I =  w_t(1- \frac{E_t-O_t}{E_t}) + w_d(1-\frac{O_d - E_d}{O_d}) + w_a(1-\frac{E_a - O_a }{E_a}) + w_s (1-\frac{T_n - V_n}{T_n}) + w_p(1-\frac{1}{T_n + 1}) + w_v * {C_{nv}}`

Where,

+-------------+-----------------------------------------------+---------------+
| Notation    | Description                                   | Example Value |
+=============+===============================================+===============+
| :math:`w_t` | Weightage for the Throughput                  | 0.3           |
+-------------+-----------------------------------------------+---------------+
| :math:`w_d` | Weightage for the Delay                       | 0.3           |
+-------------+-----------------------------------------------+---------------+
| :math:`w_a` | Weightage for the Application SLA             | 0.1           |
+-------------+-----------------------------------------------+---------------+
| :math:`w_s` | Weightage for the Topology - Network Elements | 0.1           |
+-------------+-----------------------------------------------+---------------+
| :math:`w_p` | Weightage for the Topology - Path Length      | 0.1           |
+-------------+-----------------------------------------------+---------------+
| :math:`w_v` | Weightage for the Virtualization              | 0.1           |
+-------------+-----------------------------------------------+---------------+

And

+---------------------------+------------------------------------------------------------+
| Notation                  | Description                                                |
+===========================+============================================================+
| :math:`E_t` & :math:`O_t` | Expected (theoretical Max) and Obtained Average Throughput |
+---------------------------+------------------------------------------------------------+
| :math:`E_d` & :math:`O_d` | Expected and Otained Minimum Delay                         |
+---------------------------+------------------------------------------------------------+
| :math:`E_a` & :math:`O_a` | Expected and Obtained Application SLA Metric               |
+---------------------------+------------------------------------------------------------+
| :math:`T_n`               | Total number of Network Elements (Switches and Routers)    |
+---------------------------+------------------------------------------------------------+
| :math:`V_n`               | Total number of Virtual Network Elements                   |
+---------------------------+------------------------------------------------------------+
| :math:`C_{nv}`            | Network Virtualization Constant                            |
+---------------------------+------------------------------------------------------------+

It would be interesting to explore the following alternative:

:math:`I = I_E - I_O`

where

:math:`I_E = w_t * E_t + w_d* \frac{1}{E_d} + w_a.\frac{1}{E_a} + w_s * \frac{1}{T_n} + w_p * V_n + W_v * C_{nv}`

and

:math:`I_O = w_t * O_t + w_d* \frac{1}{O_d} + w_a.\frac{1}{O_a} + w_s * \frac{1}{T_n} + w_p * V_n + W_v * C_{nv}`