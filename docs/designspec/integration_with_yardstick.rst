.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 ZTE Corp.


**************************
Integration with Yardstick
**************************

Summary
=======

For each specified QPI, QTIP needs to select a suite of test cases and report required
test result data. Based on these results data, Qtip calculate the score.
According to `QTIP architecture Agent mode`_, Yardstick will act as a runner to generate
test result data and trigger Qtip agent.


Requirements
============

1. How to create a customized suites in Yardstick to collect required metrics in Qtip

Yardstick not only has many existing suite files but also support customized suite file.
Qtip could create a suite file named `Qtip-PoC` in Yardstick repos to verify workflow of
Qtip agent mode.

2. How to launch Qtip and trigger Qtip agent in Yardstick

Check whether OS environ variable `QTIP` exists, yardstick decide whether to launch a Qtip.
We can use Yardstick CLI *yardstick plugin install* to install Qtip. After yardstick finish
test execution, Qtip agent will be trigger to collect test result data from *yardstick.out*.
So we need add a function in script `yardstick-verify` to call Qtip agent.

3. How to parse yardstick output data

Take yardstick tc002 for example, which is a ping test case, the result data is as this format:

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

basically, the key "data" contains the metrics. For now, the metrics for each test case is hardcoded
and can not be configurable. According to metric spec configuration, Qtip need parser metrics from
*yardstick.out* to fetch the data which QPI is concerned with.

4. How to retrieve test condition (hardware, software, workload) from yardstick

Qtip should tell user that metrics are based on what kind of hardware and measured by what kind
of software. For now, Yardstick don't support to collect these info. It's possible to have CLI
like *yardstick env collect* to collect hardware info and some basic software info.


..  _QTIP architecture Agent mode: https://wiki.opnfv.org/platform_performance_benchmarking
