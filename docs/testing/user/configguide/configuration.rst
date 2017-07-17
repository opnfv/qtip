.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2015 Dell Inc.
.. (c) 2016 ZTE Corp.

*************
Configuration
*************

QTIP currently supports by using a Docker image. Detailed steps
about setting up QTIP can be found below.

To use QTIP you should have access to an OpenStack environment, with at least
Nova, Neutron, Glance, Keystone and Heat installed. Add a brief introduction
to configure OPNFV with this specific installer


Installing QTIP using Docker
============================

QTIP docker image
-----------------

QTIP has a Docker images on the docker hub. Pulling opnfv/qtip docker image
from docker hub:
::

  docker pull opnfv/qtip:stable

Verify that ``opnfv/qtip`` has been downloaded. It should be listed as an image by
running the following command.
::

  docker images


Run and enter the docker instance
---------------------------------

1. If you want to run benchmarks:
::

  envs="INSTALLER_TYPE={INSTALLER_TYPE} -e INSTALLER_IP={INSTALLER_IP} -e  NODE_NAME={NODE_NAME}"
  docker run -p [HOST_IP:]<HOST_PORT>:5000 --name qtip -id -e $envs opnfv/qtip
  docker exec -i -t qtip /bin/bash

``INSTALLER_TYPE`` should be one of OPNFV installer, e.g. apex, compass, daisy, fuel
and joid. Currenty, QTIP only supports installer fuel.

``INSTALLER_IP`` is the ip address of the installer that can be accessed by QTIP.

``NODE_NAME`` is the name of opnfv pod, e.g. zte-pod1.

2. If you do not want to run any benchmarks:
::

  docker run --name qtip -id opnfv/qtip
  docker exec -i -t qtip /bin/bash

Now you are in the container and QTIP can be found in the ``/repos/qtip`` and can
be navigated to using the following command.
::

  cd repos/qtip

Install from source code
========================

You may try out the latest version of QTIP by installing from source code. It is recommended to run it under Python
``virtualenv`` so it won't screw system libraries.

Run the following commands::

  git clone https://git.opnfv.org/qtip && cd qtip
  virtualenv .venv && source .venv/bin/activate
  pip install -e .

Use the following command to exit virtualenv::

  deactivate

Re-enter the virtualenv with::

  cd <qtip-directory>
  source .venv/bin/activate

Environment configuration
=========================

Hardware configuration
----------------------

QTIP does not have specific hardware requriements, and it can runs over any
OPNFV installer.


Jumphost configuration
----------------------

Installer Docker on Jumphost, which is used for running QTIP image.

You can refer to these links:

Ubuntu: https://docs.docker.com/engine/installation/linux/ubuntu/

Centos: https://docs.docker.com/engine/installation/linux/centos/


Platform components configuration
---------------------------------

Describe the configuration of each component in the installer.
