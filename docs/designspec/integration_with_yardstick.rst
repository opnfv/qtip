.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 ZTE Corp.


**************************
Integration with Yardstick
**************************

Problem description
===================

For each specified QPI [1]_, QTIP needs to select a suite of test cases and collect
required test results. Based on these results data, Qtip calculates the score.

Proposed change
===============
Qtip has a flexible QTIP architecture [2]_ to support different mode: standalone and agent.
It is recommended to use **agent mode**. Yardstick will act as a runner to generate test
result and trigger Qtip agent on the completion of test.

Implementation
==============

Assignee(s)
-----------

*Primary assignee:*
  wu.zhihui

*Other contributors*
  TBD

Work Items
----------

1. Create a customized suite in Yardstick

Yardstick not only has many existing suites but also support customized suites. Qtip could
create a suite named **Qtip-PoC** in Yardstick repo to verify workflow of Qtip agent mode.

2. Launch Qtip in Yardstick

Whether to launch Qtip will be determined by checking the existence of OS environ variable
*QTIP*. If it exists, Qtip will be launched by using Yardstick CLI
`yardstick plugin install` [3]_.

3. Trigger Qtip agent in Yardstick

After Yardstick completes the execution of test cases, Qtip agent needs to be called to
collect test result from the output file *yardstick.out*. The function needs to be
created and invoked in script *yardstick-verify*.

4. Parse yardstick test result

Take Yardstick tc002 for example, which is a ping test case, the result is as this format:

.. code-block:: python

   {
        "benchmark":{
            "timestamp": 1476848621.561923,
            "errors": "",
            "data": {
                "rtt": { "ares": 2.802 }
            },
            "sequence": 2
        },
        "runner_id": 7222
   }

Basically, the key *data* contains the metrics. For now, the metrics for each test case is
hardcoded and is not configurable. Qtip agent will fetch metrics which is definded in
`metric spec configuration file` [4]_ by parsering *yardstick.out*.

5. Retrieve test condition (hardware, software, workload) from yardstick

Qtip should note user the hardware the metrics are based on and the software they are
measured. For now, Yardstick doesn't support to collect these info. Yardstick needs to
implement a CLI like *yardstick env collect* to collect these info.

Testing
=======

The changes will be covered by new unit test.

Documentation
=============

TBD

Reference
=========
.. [1] QTIP performance inde
.. [2] https://wiki.opnfv.org/platform_performance_benchmarking
.. [3] https://wiki.opnfv.org/display/yardstick/How+to+install+a+plug-in+into+Yardstick
.. [4] A YAML file which definds the required metrics for one specified QPI