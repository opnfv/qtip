.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 ZTE Corp.


**************************
Integration with Yardstick
**************************

Problem description
===================

For each specified QPI [1]_, QTIP needs to select a suite of test cases and collect
required test results. Based on these results, Qtip calculates the score.

Proposed change
===============
Qtip has a flexible architecture [2]_ to support different mode: standalone and agent.
It is recommended to use **agent mode** to work with existing test runners. Yardstick will
act as a runner to generate test result and trigger Qtip agent on the completion of test.


Work Items in Yardstick
-----------------------

1. Create a customized suite in Yardstick

Yardstick not only has many existing suites but also support customized suites. Qtip could
create a suite named **Qtip-PoC** in Yardstick repo to verify workflow of Qtip agent mode.

2. Launch Qtip in Yardstick

Whether to launch Qtip will be determined by checking the existence of OS environment
variable *QTIP*. If it exists, Qtip will be launched by using Yardstick CLI
`yardstick plugin install` [3]_.

3. Yardstick interacts with Qtip

See
`Yardstick-Qtip+integration <https://wiki.opnfv.org/display/yardstick/Yardstick-Qtip+integration>`_
for details.

Work Items in Qtip
------------------

1. Parse yardstick test result

When Qtip agent receive Yarstick test result, Qtip agent will fetch metrics which is
definded in metric spec configuration file. Based on these metrics, Qtip agent will
caculate QPI.

2. Report QPI

Qtip agent will push QPI to database for storage and dashboard for visualization.
And Yardstick can query QPI via API [4]_.

Implementation
==============

Assignee(s)
-----------

*Primary assignee:*
  wu.zhihui

*Other contributors*
  TBD

Testing
=======

The changes will be covered by new unit test.

Documentation
=============

TBD

Reference
=========

.. [1] QTIP performance index
.. [2] https://wiki.opnfv.org/display/qtip/Architecture
.. [3] https://wiki.opnfv.org/display/yardstick/How+to+install+a+plug-in+into+Yardstick
.. [4] https://wiki.opnfv.org/display/yardstick/Yardstick-Qtip+integration
