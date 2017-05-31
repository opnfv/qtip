.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

*************************
Getting started with QTIP
*************************

.. code-block::

    pip install qtip
    eval $(ssh-agent)

    qtip create <project_name>
    cd <project_name>

    qtip setup
    qtip run
    qtip teardown

Installation
============

Refer to `installation and configuration guide`_ for details

.. _installation and configuration guide:../configguide/

Create
======

Create a new project to hold the necessary configurations and test results
::

    qtip create <project_name>

The user would be prompted for OPNFV installer, its hostname etc
::

    **Pod Name [unknown]: zte-pod1**
    User's choice to name OPNFV Pod

    **OPNFV Installer [manual]: fuel**
    QTIP currently supports fuel and apex only

    **Installer Hostname [dummy-host]: master**
    The hostname for the fuel or apex installer node. The same hostname can be added to **~/.ssh/config** file of current user,
    if there are problems resolving the hostname via interactive input.

    **OPNFV Scenario [unknown]: os-nosdn-nofeature-ha**
    Depends on the OPNFV scenario deployed

Setup
=====

With the project is created, user should now proceed on to setting up testing environment. In this step, ssh connection
to hosts in SUT will be configured automatically::

    cd <project_name>
    $ qtip setup

Run
===

QTIP uses ``ssh-agent`` for authentication of ssh connection to hosts in SUT. It must be started correctly before
running the tests::

    eval $(ssh-agent)

Then run test with ``qtip run``

Teardown
========

Clean up the temporary folder on target hosts.

.. note:: The installed packages for testing won't be uninstalled.

One more thing
==============

You may use ``-v`` for verbose output (``-vvv`` for more, ``-vvvv`` to enable connection debugging)
