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
QTIP is currently supports two OPNFV different components of the NFVi, compute and storage. In order to benchmark
either one of them, one needs to generate their respective templates.
::

  qtip create --project-template [compute|storage] <workspace_name>

By default, the compute template will be generated. One will be prompted to enter the parameters required
to generate the template.

Once the generation is complete one needs to setup the OpenStack configuration to get started.
::

  cd <workspace_name>
  qtip setup

After the setup has been completed, one is now ready to run QTIP.
::

  qtip run

Debugging options
=================

QTIP uses Ansible as the runner. One can use all of Ansible's CLI option with QTIP. In order to enable verbose mode
::

  qtip setup -v

One may also be able to achieve the different levels of verbosity
::

  qtip run [-v|-vv|-vvv]
