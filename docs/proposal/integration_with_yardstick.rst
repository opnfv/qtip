.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 ZTE Corp.


**************************
Integration with Yardstick
**************************

Problem description
===================

For each specified QPI [1]_, QTIP needs to select a suite of test cases and collect
required test results. Based on these results, QTIP calculates the score.

Proposed change
===============
QTIP has a flexible architecture [2]_ to support different mode: standalone and agent.
It is recommended to use **agent mode** to work with existing test runners. Yardstick will
act as a runner to generate test result and trigger QTIP agent on the completion of test.


Work Items in Yardstick
-----------------------

1. Create a customized suite in Yardstick

Yardstick not only has many existing suites but also support customized suites. QTIP could
create a suite named **QTIP-PoC** in Yardstick repo to verify workflow of QTIP agent mode.

2. Launch QTIP in Yardstick

Whether to launch QTIP will be determined by checking the existence of OS environment
variable *QTIP*. If it exists, QTIP will be launched by using Yardstick CLI
`yardstick plugin install` [3]_.

3. Yardstick interacts with QTIP

See
`Yardstick-QTIP+integration <https://wiki.opnfv.org/display/yardstick/Yardstick-QTIP+integration>`_
for details.

Work Items in QTIP
------------------

1. Provide an API for Yardstick to post test result and environment info

After completing test execution, Yardstick will post test result and enviroment info with
JSON format via QTIP API. See
`Yardstick-QTIP+integration <https://wiki.opnfv.org/display/yardstick/Yardstick-QTIP+integration>`_
for details.

2. Parse yardstick test result

When QTIP agent receive Yarstick test result and enviroment info, QTIP agent will extract
metrics which is definded in metric spec configuration file. Based on these metrics, QTIP
agent will caculate QPI.

3. Provide an API for querying QPI

QTIP will provide an API for querying QPI. See
`Yardstick-QTIP+integration <https://wiki.opnfv.org/display/yardstick/Yardstick-QTIP+integration>`_
for details.

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
