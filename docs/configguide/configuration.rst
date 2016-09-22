.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2015 Dell Inc.
.. (c) 2016 ZTE Corp.


Qtip configuration
==================

QTIP currently supports by using a Docker image or by pulling the repo from
the upstream repository found at https://git.opnfv.org/qtip. Detailed steps
about setting up QTIP using both of these options can be found below.

To use QTIP you should have access to an OpenStack environment, with at least
Nova, Neutron, Glance, Keystone and Heat installed. Add a brief introduction
to configure OPNFV with this specific installer


Pre-configuration activities
----------------------------


Setting QTIP framework on Ubuntu 14.04
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install dependencies:
::

  sudo apt-get install python-dev
  sudo apt-get install python-pip
  sudo apt-get install build-essential
  sudo apt-get install git wget
  sudo pip install python-heatclient python-glanceclient python-neutronclient


Download source code and install python dependencies:
::

  git clone https://git.opnfv.org/qtip
  cd qtip


Installing QTIP using Docker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

QTIP has a Docker images on the docker hub. Pulling opnfv/qtip docker image
from docker hub:
::

  sudo docker pull opnfv/qtip

Verify that opnfv/qtip has been downloaded. It should be listed as an image by
running the following command.
::

  sudo docker images

Run the Docker instance:
::

  docker run -it opnfv/qtip

Now you are in the container and QTIP can be found in the  /repos/qtip and can
be navigated to using the following command.
::

  cd repos/qtip


OpenStack parameters and credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Environment variables
"""""""""""""""""""""

Before running QTIP it is necessary to export OpenStack environment variables
from the OpenStack *openrc* file. This can be done by running the following
command.
::

  source get_env_info.sh -n {INSTALLER_TYPE} -i {INSTALLER_IP}
  source opnfv-creds.sh

This provides a ``opnfv-creds.sh`` file which can be sources to get the
environment variables. For running QTIP manually, it is also necessary to
export the installer type.
::

  export INSTALLER_TYPE="{installer-type}"


QTIP  default key pair
""""""""""""""""""""""

QTIP uses a SSH key pair to connect to the guest image. This key pair can
be found in the ``data/`` directory.


Hardware configuration
----------------------

Qtip does not have specific hardware requriements, and it can runs over any
OPNFV installer.


Jumphost configuration
----------------------

Installer Docker on Jumphost, which is used for running Qtip image.

The first step is to install docker:
::

  sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80
  --recv-keys 58118E89F3A912897C070ADBF76221572C52609D


Add an entry for your Ubuntu operating system:
::

  Open the /etc/apt/sources.list.d/docker.list file in your favorite editor.

If the file doesn’t exist, create it.

Remove any existing entries.

Add an entry for your Ubuntu operating system.

On Ubuntu Trusty 14.04 (LTS)
::

  deb https://apt.dockerproject.org/repo ubuntu-trusty main

Update the package manager
::

  sudo apt-get update

Install Docker:
::

  sudo apt-get install docker-engine

Starting Docker Daemon:
::

  sudo service docker start


Platform components configuration
---------------------------------

Describe the configuration of each component in the installer
