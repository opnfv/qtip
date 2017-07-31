.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


***************
CLI User Manual
***************

QTIP consists of a number of benchmarking tools or metrics, grouped under QPI's. QPI's map to the different
components of a NFVI ecosystem, such as compute, network and storage. Depending on the type of application,
a user may group them under plans.

Bash Command Completion
=======================

To enable command completion, an environment variable needs to be enabled.
Add the following line to the **.bashrc** file
::

  eval "$(_QTIP_COMPLETE=source qtip)"

Getting help
============

QTIP CLI provides interface to all of the above the components. A help page provides a list of all the commands
along with a short description.
::

  qtip [-h|--help]

Usage
=====
Typically a complete plan is executed at the target environment. QTIP defaults to a number of sample plans.
A list of all the available plans can be viewed
::

  qtip plan list

In order to view the details about a specific plan.
::

  qtip plan show <plan_name>

where *plan_name* is one of those listed from the previous command.

To execute a complete plan
::

  qtip plan run <plan_name> -p <path_to_result_directory>

QTIP does not limit result storage at a specific directory. Instead a user may specify his own result storage
as above. An important thing to remember is to provide absolute path of result directory.
::

  mkdir result
  qtip plan run <plan_name> -p $PWD/result

Similarly, the same commands can be used for the other two components making up the plans, i.e QPI's and metrics.
For example, in order to run a single metric
::

  qtip metric run <metric_name> -p $PWD/result

The same can be applied for a QPI.

QTIP also provides the utility to view benchmarking results on the console. One just need to provide to where
the results are stored. Extending the example above
::

  qtip report show <metric_name> -p $PWD/result

Debugging options
=================

Debug option helps identify the error by providing a detailed traceback. It can be enabled as
::

  qtip [-d|--debug] plan run <plan_name>
