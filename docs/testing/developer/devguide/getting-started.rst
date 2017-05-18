.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

*************************
Getting started with QTIP
*************************

Overview
========

Create a new project to hold the neccessary configurations and test results
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

    **OPNFV Scenario [unknown]: os-no-sdn**
    Depends on the OPNFV scenario deployed

With the framework generated, user should now proceed on to setting up testing environment. In this step, information related to OPNFV cluster would
be generated, such as getting the IP addresses of the nodes in System Under Test (SUT).
::

    cd <project_name>
    $ qtip setup

QTIP uses `ssh-agent` for authentication. It is critical that it started and stopped in the correct way.


ssh-agent
=========

ssh-agent is used to hold the private keys for RSA, DCA authentication. In order to start the process
::

    $ eval $(ssh-agent)

This would start the agent in background. One must now be able to execute QTIP
::

    $ qtip run

However, if QTIP is not working because of `ssh-agent`, one should kill the process as follows
::

    $ eval $(ssh-agent -k)

Then start the agent again as described above.
