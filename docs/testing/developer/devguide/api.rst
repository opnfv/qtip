.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


***************************************
API - Application Programming Interface
***************************************

QTIP consists of different tools(metrics) to benchmark the NFVI. These metrics
fall under different NFVI subsystems(QPI's) such as compute, storage and network.
A plan consists of one or more QPI's, depending upon how the end-user would want
to measure performance. API is designed to expose a RESTful interface to the user
for executing benchmarks and viewing respective scores.

Framework
=========

QTIP API has been created using the Python package `Connexion`_. It has been chosen
for a number of reasons. It follows API First approach to create micro-services.
Hence, firstly the API specifications are defined from the client side perspective,
followed by the implementation of the micro-service. It decouples the business logic
from routing and resource mapping making design and implementation cleaner.

It has two major components:

API Specifications

   The API specification is defined in a yaml or json file. Connexion follows
   `Open API specification`_ to determine the design and maps the endpoints to methods in python.

Micro-service Implementation
   Connexion maps the ``operationId`` corresponding to every operation in API
   Specification to methods in python which handles request and responses.

As explained, QTIP consists of metrics, QPI's and plans. The API is designed to provide
a RESTful interface to all these components. It is responsible to provide listing and details of
each individual element making up these components.

Design
======

Specification
-------------

API's entry point (``main``) runs connexion ``App`` class object after adding API Specification
using ``App.add_api`` method. It loads specification from ``swagger.yaml`` file by specifying
``specification_dir``.

Connexion reads API's endpoints(paths), operations, their request and response parameter
details and response definitions from the API specification i.e. ``swagger.yaml`` in this case.

Following example demonstrates specification for the resource ``plans``.

::

    paths:
      /plans/{name}:
        get:
          summary: Get a plan by plan name
          operationId: qtip.api.controllers.plan.get_plan
          tags:
            - Plan
            - Standalone
          parameters:
            - name: name
              in: path
              description: Plan name
              required: true
              type: string
          responses:
            200:
              description: Plan information
              schema:
                $ref: '#/definitions/Plan'
            404:
              description: Plan not found
              schema:
                $ref: '#/definitions/Error'
            501:
              description: Resource not implemented
              schema:
                $ref: '#/definitions/Error'
            default:
              description: Unexpected error
              schema:
                $ref: '#/definitions/Error'
    definitions:
      Plan:
        type: object
        required:
          - name
        properties:
          name:
            type: string
          description:
            type: string
          info:
            type: object
          config:
            type: object

Every ``operationId`` in above operations corresponds to a method in controllers.
QTIP has three controller modules each for plan, QPI and metric. Connexion will
read these mappings and automatically route endpoints to business logic.

`Swagger Editor`_ can be explored to play with more such examples and to validate
the specification.

Controllers
-----------

The request is handled through these methods and response is sent back to the client.
Connexion takes care of data validation.

.. code-block:: python

    @common.check_endpoint_for_error(resource='Plan')
    def get_plan(name):
        plan_spec = plan.Plan(name)
        return plan_spec.content

In above code ``get_plan`` takes a plan name and return its content.

The decorator ``check_endpoint_for_error`` defined in ``common`` is used to handle error
and return a suitable error response.


During Development the server can be run by passing specification file(``swagger.yaml``
in this case) to connexion cli -

::

    connexion run <path_to_specification_file> -v


Extending the Framework
=======================

Modifying Existing API:
-----------------------
    API can be modified by adding entries in ``swagger.yaml`` and adding the corresponding
    controller mapped from ``operationID``.

    Adding endpoints:

        New endpoints can be defined in ``paths`` section in ``swagger.yaml``. To add a new resource *dummy* -

        ::

            paths:
              /dummies:
                get:
                  summary: Get all dummies
                  operationId: qtip.api.controllers.dummy.get_dummies
                  tags:
                    - dummy
                  responses:
                    200:
                      description: Foo information
                      schema:
                        $ref: '#/definitions/Dummy
                    default:
                      description: Unexpected error
                      schema:
                        $ref: '#/definitions/Error'


        And then model of the resource can be defined in the ``definitions`` section.

            ::

                definitions:
                  Dummy:
                    type: object
                    required:
                      - name
                    properties:
                      name:
                        type: string
                      description:
                        type: string
                      id:
                        type: string


    Adding controller methods:
        Methods for handling requests and responses for every operation for the endpoint added can be
        implemented in ``controller``.

        In ``controllers.dummy``

        .. code-block:: python

            def get_dummies():
                all_dummies = [<code to get all dummies>]
                return all_dummies, httplib.OK

    Adding error responses
        Decorators for handling errors are defined in ``common.py`` in ``api``.

        .. code-block:: python

            from qtip.api import common

            @common.check_endpoint_for_error(resource='dummy',operation='get')
            def get_dummies()
                all_dummies = [<code to get all dummies>]
                return all_dummies

Adding new API:
---------------

    API can easily be extended by adding more APIs to ``Connexion.App`` class object using
    ``add_api`` class method.

    In ``__main__``

    .. code-block:: python

        def get_app():
        app = connexion.App(__name__, specification_dir=swagger_dir)
        app.add_api('swagger.yaml', base_path='/v1.0', strict_validation=True)
        return app


    Extending it to add new APIs. The new API should have all endpoints mapped using ``operationId``.

    .. code-block:: python

        from qtip.api import __main__
        my_app = __main__.get_app()
        my_app.add_api('new_api.yaml',base_path'api2',strict_validation=True)
        my_app.run(host="0.0.0.0", port=5000)


.. _Connexion: https://connexion.readthedocs.io/en/latest/
.. _Open API specification: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md
.. _Swagger Editor: http://editor.swagger.io/
