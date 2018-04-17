.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2018 Spirent Communications Corp.
.. Template to be used for test case descriptions in QTIP Project.


Test Case Description
=====================

+-----------------------------------------------------------------------------+
|Network throughput                                                           |
+==============+==============================================================+
|test case id  | qtip_throughput                                              |
+--------------+--------------------------------------------------------------+
|metric        | rfc2544 throughput                                           |
+--------------+--------------------------------------------------------------+
|test purpose  | get the max throughput of the pathway on same host or accross|
|              | hosts                                                        |
+--------------+--------------------------------------------------------------+
|configuration | None                                                         |
+--------------+--------------------------------------------------------------+
|test tool     | Spirent Test Center Virtual                                  |
+--------------+--------------------------------------------------------------+
|references    | RFC2544                                                      |
+--------------+--------------------------------------------------------------+
|applicability | 1. test the switch throughput on same host or accross hosts  |
|              | 2. test the switch throughput for different packet sizes     |
+--------------+--------------------------------------------------------------+
|pre-test      | 1. deploy STC license server and LabServer on public network |
|conditions    | and verify it can operate correctlly                         |
|              | 2. upload STC virtual image and create STCv flavor on the    |
|              | deployed cloud environment                                   |
+--------------+------+----------------------------------+--------------------+
|test sequence | step | description                      | result             |
|              +------+----------------------------------+--------------------+
|              |  1   | deploy STCv stack on the target  | 2 STCv VM will be  |
|              |      | cloud with affinity attribute    | established on the |
|              |      | according to requirements.       | cloud              |
|              +------+----------------------------------+--------------------+
|              |  2   | run rfc2544 throughput test with | test result report |
|              |      | different packet size            | will be produced in|
|              |      |                                  | QTIP container     |
|              +------+----------------------------------+--------------------+
|              |  3   | destory STCv stack               | STCv stack         |
|              |      | different packet size            | destoried          |
+--------------+------+----------------------------------+--------------------+
|test verdict  | find the test result report in QTIP container running        |
|              | directory                                                    |
+--------------+--------------------------------------------------------------+

+-----------------------------------------------------------------------------+
|Network throughput                                                           |
+==============+==============================================================+
|test case id  | qtip_latency                                                 |
+--------------+--------------------------------------------------------------+
|metric        | rfc2544 lantency                                             |
+--------------+--------------------------------------------------------------+
|test purpose  | get the latency value of the pathway on same host or accross |
|              | hosts                                                        |
+--------------+--------------------------------------------------------------+
|configuration | None                                                         |
+--------------+--------------------------------------------------------------+
|test tool     | Spirent Test Center Virtual                                  |
+--------------+--------------------------------------------------------------+
|references    | RFC2544                                                      |
+--------------+--------------------------------------------------------------+
|applicability | 1. test the switch latency on same host or accross hosts     |
|              | 2. test the switch latency for different packet sizes        |
+--------------+--------------------------------------------------------------+
|pre-test      | 1. deploy STC license server and LabServer on public network |
|conditions    | and verify it can operate correctlly                         |
|              | 2. upload STC virtual image and create STCv flavor on the    |
|              | deployed cloud environment                                   |
+--------------+------+----------------------------------+--------------------+
|test sequence | step | description                      | result             |
|              +------+----------------------------------+--------------------+
|              |  1   | deploy STCv stack on the target  | 2 STCv VM will be  |
|              |      | cloud with affinity attribute    | established on the |
|              |      | according to requirements.       | cloud              |
|              +------+----------------------------------+--------------------+
|              |  2   | run rfc2544 latency test with    | test result report |
|              |      | different packet size            | will be produced in|
|              |      |                                  | QTIP container     |
|              +------+----------------------------------+--------------------+
|              |  3   | destroy STCv stack               | STCv stack         |
|              |      |                                  | destried           |
+--------------+------+----------------------------------+--------------------+
|test verdict  | find the test result report in QTIP container running        |
|              | directory                                                    |
+--------------+--------------------------------------------------------------+
