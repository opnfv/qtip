.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 ZTE Corp.


*********
Dashboard
*********

The dashboard gives user an intuitive view of benchmark result.

Purpose
=======

The basic element to be displayed is QPI a.k.a. QTIP Performance Index. But it
is also important to show user

#. How is the final score calculated?
#. Under what condition is the test plan executed?
#. How many runs of a performance tests have been executed and is there any deviation?
#. Comparison of benchmark result from different PODs or configuration

Templates
=========

Different board templates are created to satisfy the above requirements.

Composition
-----------

QTIP gives a simple score but there must be a complex formula behind it. This
view explains the composition of the QPI.

Condition
---------

The condition of a benchmark result includes

* System Under Test

  * Hardware environment
  * Hypervisor version
  * Operation System release version
  * System Configuration

* Test Tools

  * Release version
  * Configuration

* Test Facility

  * Laboratory
  * Engineer
  * Date

Conditions that do NOT have an obvious affect on the test result may be ignored,
e.g. temperature, power supply.

Deviation
---------

Performance tests are usually repeated many times to reduce random disturbance.
This view shall show an overview of deviation among different runs.

Comparison
----------

Comparison can be done between different PODs or different configuration on the
same PODs.

In a comparison view, the metrics are displayed in the same diagram. And the
parameters are listed side by side.

Both common parameters and different parameters are listed. Common values are
merged to the same cell. And user may configure the view to hide common rows.

A draft design is as following::

    ^
    |
    |
    |
    |           XXXXXXXX
    |         XXX      XX+-+ XXXXXXXXXX
    |      XXX          +XXXX         XXXXX
    +-+XX X         +--+    ++            XXXXXX     +-+
    | X+-+X   +----+          +-+              +----+X
    |X    +--+                   +---+         XXXXXX X
    |                                 +-------+        X
    |
    |
    +----------------------------------------------------->

    +--------------------+----------------+---------------+
    | different param 1  |                |               |
    |                    |                |               |
    +-----------------------------------------------------+
    | different param 2  |                |               |
    |                    |                |               |
    +-------------------------------------+---------------+
    | common param 1     |                                |
    |                    |                                |
    +-------------------------------------+---------------+
    | different param 3  |                |               |
    |                    |                |               |
    +-------------------------------------+---------------+
    | common param 2     |                                |
    |                    |                                |
    +--------------------+--------------------------------+
                                             +------------+
                                             | HIDE COMMON|
                                             +------------+

