.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.


********************************
Storage Performance Benchmarking
********************************

Like compute QPI, storage QPI gives users an overall score for system storage performance.
The project `StorPerf`_ in OPNFV provides a tool to measure ephemeral and block storage
performance of OpenStack. Naturally, QTIP integrates `StorPerf`_ to generate the storage
performance data.

For now, storage QPI runs against on the baremetal/virtual scenario deployed by
the OPNFV installer `APEX`_.

Getting started
===============

Notice: All descriptions are based on containers.

Requirements
------------

* Git must be installed.
* Docker and docker-compose must be installed.

Git Clone QTIP Repo
-------------------

::

  git clone https://git.opnfv.org/qtip

Running QTIP container and Storperf Containers
----------------------------------------------

With Docker Compose, we can use a YAML file to configure application's services and
use a single command to create and start all the services.

There is a YAML file ``./qtip/tests/ci/storage/docker-compose.yaml`` from QTIP repos.
It can help you to create and start the storage QPI service.

Before running docker-compose, you must specify these three variables:

* DOCKER_TAG, which specified the Docker tag(ie: latest)
* SSH_CREDENTIALS, a directory which includes an SSH key pair will be mounted into QTIP container.
  QTIP use this SSH key pair to connect to remote hosts.
* ENV_FILE, which includes the environment variables required by QTIP and Storperf containers

  A example of ENV_FILE:

  ::

    INSTALLER_TYPE=apex
    INSTALLER_IP=192.168.122.247
    TEST_SUITE=storage
    NODE_NAME=zte-virtual5
    SCENARIO=generic
    TESTAPI_URL=
    OPNFV_RELEASE=euphrates
    # The below environment variables are Openstack Credentials.
    OS_USERNAME=admin
    OS_USER_DOMAIN_NAME=Default
    OS_PROJECT_DOMAIN_NAME=Default
    OS_BAREMETAL_API_VERSION=1.29
    NOVA_VERSION=1.1
    OS_PROJECT_NAME=admin
    OS_PASSWORD=ZjmZJmkCvVXf9ry9daxgwmz3s
    OS_NO_CACHE=True
    COMPUTE_API_VERSION=1.1
    no_proxy=,192.168.37.10,192.0.2.5
    OS_CLOUDNAME=overcloud
    OS_AUTH_URL=http://192.168.37.10:5000/v3
    IRONIC_API_VERSION=1.29
    OS_IDENTITY_API_VERSION=3
    OS_AUTH_TYPE=password

Then, you use the following commands to start storage QPI service.

::

  docker-compose -f docker-compose.yaml pull
  docker-compose -f docker-compose.yaml up -d

Execution
---------

You can run storage QPI with docker exec:
::

  docker exec <qtip container> bash -x /home/opnfv/repos/qtip/qtip/scripts/quickstart.sh

QTIP generates results in the ``$PWD/results/`` directory are listed down under the
timestamp name.

Metrics
-------

Storperf provides the following `metrics`_:

* IOPS
* Bandwidth (number of kilobytes read or written per second)
* Latency


.. _StorPerf: https://wiki.opnfv.org/display/storperf
.. _APEX: https://wiki.opnfv.org/display/apex
.. _metrics: http://docs.opnfv.org/en/stable-euphrates/submodules/storperf/docs/testing/user/introduction.html#what-data-can-i-get
