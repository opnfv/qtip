.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2018 Spirent Communications Corp.


********************************
Network Performance Benchmarking
********************************
Like compute or storage QPI, network QPI gives users an overall score for system network performance.
For now it focuses on L2 virtual switch performance on NFVI. Current testcase are from RFC2544 standart and
implemntation is based on Spirent Testcenter Virtual.

For now, network QPI runs against on the baremetal/virtual scenario deployed by
the OPNFV installer `APEX`_.

Getting started
===============
Notice: All descriptions are based on containers.

Requirements
------------

* Git must be installed.
* Docker and docker-compose must be installed.
* Spirent Testcenter Virtual image must be uploaded to the target cloud and the
 associated flavor must be created before test.
* Spirent License Server and Spirent LabServer must be set up and keep them ip
 reachable from target cloud external network before test.

Git Clone QTIP Repo
-------------------

::

  git clone https://git.opnfv.org/qtip

Running QTIP container and Nettest Containers
----------------------------------------------

With Docker Compose, we can use a YAML file to configure application's services and
use a single command to create and start all the services.

There is a YAML file ``./qtip/tests/ci/network/docker-compose.yaml`` from QTIP repos.
It can help you to create and start the network QPI service.

Before running docker-compose, you must specify these three variables:

* DOCKER_TAG, which specified the Docker tag(ie: latest)
* SSH_CREDENTIALS, a directory which includes an SSH key pair will be mounted into QTIP container.
  QTIP use this SSH key pair to connect to remote hosts.
* ENV_FILE, which includes the environment variables required by QTIP and Storperf containers

  A example of ENV_FILE:

  ::

    INSTALLER_TYPE=apex
    INSTALLER_IP=192.168.122.247
    TEST_SUITE=network
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
    # The below environment variables are extra info with Spirent.
    SPT_LICENSE_SERVER_IP=192.168.37.251
    SPT_LAB_SERVER_IP=192.168.37.122
    SPT_STCV_IMAGE_NAME=stcv-4.79
    SPT_STCV_FLAVOR_NAME=m1.tiny

Then, you use the following commands to start network QPI service.

::

  docker-compose -f docker-compose.yaml pull
  docker-compose -f docker-compose.yaml up -d

Execution
---------

You can run network QPI with docker exec:
::

  docker exec <qtip container> bash -x /home/opnfv/repos/qtip/qtip/scripts/quickstart.sh

QTIP generates results in the ``$PWD/results/`` directory are listed down under the
timestamp name.

Metrics
-------

Nettest provides the following `metrics`_:

* RFC2544 througput
* RFC2544 latency


.. _APEX: https://wiki.opnfv.org/display/apex
.. _metrics: https://tools.ietf.org/html/rfc2544

