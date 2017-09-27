.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


***************
CLI User Manual
***************

QTIP consists of a number of benchmarking tools or metrics, grouped under QPI's. QPI's map to the different
components of a NFVi ecosystem, such as compute, network and storage. Depending on the type of application,
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

  qtip --help

Usage
=====
QTIP is currently supports two different QPI's, compute and storage. To list all the supported QPI
::

  qtip qpi list

The details of any QPI can be viewed as follows
::

qtip qpi show <qpi_name>

In order to benchmark either one of them, their respective templates need to be generated
::

  qtip create --project-template [compute|storage] <workspace_name>

By default, the compute template will be generated. An interactive prompt would gather all parameters specific to
OpenStack installation.

Once the template generation is complete, configuration for OpenStack needs to be generated.
::

  cd <workspace_name>
  qtip setup

This step generates the inventory, populating it with target nodes.

QTIP can now be run
::

  qtip run

This would start the complete testing suite, which is either compute or storage. Each suite normally takes about
half an hour to complete.

Benchmarking report is made for each and every individual section in a QPI, on a particular target node. It consists of
the actual test values on that node along with scores calculated by comparison against a baseline.
::

  qtip report show [-n|--node] <node> <section_name>


Debugging options
=================

QTIP uses Ansible as the runner. One can use all of Ansible's CLI option with QTIP. In order to enable verbose mode
::

  qtip setup -v

One may also be able to achieve the different levels of verbosity
::

  qtip run [-v|-vv|-vvv]
