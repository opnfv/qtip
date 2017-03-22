**************
QTIP CLI Usage
**************

QTIP consists of a number of benchmarking tools or metrics, grouped under QPI's. QPI's map to the different
components of a NFVI ecosystem, such as compute, network and storage. Depending on the type of application,
a user may group them under plans.

QTIP CLI provides interface to all of the above the components. A help page provides a list of all the commands
along with a short description.
::

  qtip [-h|--help]

Typically a complete plan is executed at the
target environment. QTIP defaults to a number of sample plans. One may be able to list them using
::

  qtip plan list

One can also be able to view the details about a specific plan.
::

  qtip plan show <plan_name>

where *plan_name* is one of those listed from the previous command.

To execute a complete plan
::

  qtip plan run <plan_name>

Similarly, the same commands can be used for the other two components making up the plans, i.e QPI's and metrics.

Debug option helps identify the error by providing a detailed traceback. It can be enabled as
::

  qtip [-d|--debug] plan run <plan_name>
