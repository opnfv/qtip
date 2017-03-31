.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


***************
API User Manual
***************

QTIP consists of a number of benchmarking tools or metrics, grouped under QPI's. QPI's map to the different
components of an NFVI ecosystem, such as compute, network and storage. Depending on the type of application,
a user may group them under plans.

QTIP API provides a RESTful interface to all of the above components. User can retrieve list of plans, QPIs
and metrics and their individual information.


Running
=======

After installing QTIP. API server can be run using command ``qtip-api`` on the local machine.

All the resources and their corresponding operation details can be seen at ``/v1.0/ui``.

The whole API specification in json format can be seen at ``/v1.0/swagger.json``.

The data models are given below:

  * Plan
  * Metric
  * QPI

Plan::

  {
    "name": <plan name>,
    "description": <plan profile>,
    "info": <{plan info}>,
    "config": <{plan configuration}>,
    "QPIs": <[list of qpis]>,
  },

Metric::

  {
    "name": <metric name>,
    "description": <metric description>,
    "links": <[links with metric information]>,
    "workloads": <[cpu workloads(single_cpu, multi_cpu]>,
  },

QPI::

  {
    "name": <qpi name>,
    "description": <qpi description>,
    "formula": <formula>,
    "sections": <[list of sections with different metrics and formulaes]>,
  }

The API can be described as follows

Plans:

 +--------+----------------------------+-----------------------------------------+
 | Method | Path                       | Description                             |
 +========+============================+=========================================+
 | GET    | /v1.0/plans                | Get the list of of all plans            |
 +--------+----------------------------+-----------------------------------------+
 | GET    | /v1.0/plans/{name}         | Get details of the specified plan       |
 +--------+----------------------------+-----------------------------------------+

Metrics:

 +--------+----------------------------+-----------------------------------------+
 | Method | Path                       | Description                             |
 +========+============================+=========================================+
 | GET    | /v1.0/metrics              | Get the list of all metrics             |
 +--------+----------------------------+-----------------------------------------+
 | GET    | /v1.0/metrics/{name}       | Get details of specified metric         |
 +--------+----------------------------+-----------------------------------------+

QPIs:

 +--------+----------------------------+-----------------------------------------+
 | Method | Path                       | Description                             |
 +========+============================+=========================================+
 | GET    | /v1.0/qpis                 | Get the list of all QPIs                |
 +--------+----------------------------+-----------------------------------------+
 | GET    | /v1.0/qpis/{name}          | Get details of specified QPI            |
 +--------+----------------------------+-----------------------------------------+


*Note:*
    *running API with connexion cli does not require base path (/v1.0/) in url*
