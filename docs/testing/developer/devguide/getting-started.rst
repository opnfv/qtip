.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

*************************
Getting started with QTIP
*************************

Introduction
============

QTIP architecture has been changed, with Ansible becoming the backbone of the entire project. Previously, Python was used to load configurations
required to run QTIP.

Overview
========

QTIP follows the concept of generating its framework on the fly, a concept similiar to MVC frameworks, with the logic being distributed to help
the user with customization. To generate the QTIP framework
::
i
    qtip project create <project_name>

The user would be prompted for OPNFV installer, its hostname etc.

With the framework generated, user should now proceed on to setting up QTIP. In this step, information related to OPNFV cluster would be generated,
such as getting the IP addresses of the compute nodes.
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
