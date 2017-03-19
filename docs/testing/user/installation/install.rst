*****************
QTIP Installation
*****************

QTIP is a python package to benchmark the NFV Infrastructure.
Currently QTIP supports installation on a Jumphost and Docker.
To install QTIP via docker, please read the `configuration guide
<http://artifacts.opnfv.org/qtip/docs/configguide/configguide.pdf>`_.
It provides a detailed tutorial on installing QTIP with Docker.
The steps below explain QTIP installation on any Jumphost system.

To use QTIP, one must have access to an OpenStack environment,
with Nova, Neutron, Keystone and Glance installed.


Installing QTIP on Jumphost System
==================================

Installation on your system requires pulling the QTIP repository
and installing the package via pip package manager.

Dependencies
------------

QTIP requires setuptools version greater than or equal to 17.1.
Before installing QTIP, check the version of setuptools:
::

  pip show setuptools


If the version does not match the requirement, then upgrade setuptools:
::

  pip install --upgrade setuptools


Clone the QTIP repository on your system.
::

  git clone https://git.opnfv.org/qtip


Install QTIP.
::

  pip install qtip


The above would install the remaining dependencies for QTIP.