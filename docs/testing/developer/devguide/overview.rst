.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corporation


********
Overview
********

QTIP uses Python as primary programming language and build the framework from the following packages

======== ===============================================================================================================
Module   Package
======== ===============================================================================================================
api      `Connexion`_ - API first applications with OpenAPI/Swagger and Flask
cli      `Click`_ - the “Command Line Interface Creation Kit”
template `Jinja2`_ - a full featured template engine for Python
docs     `sphinx`_ - a tool that makes it easy to create intelligent and beautiful documentation
testing  `pytest`_ - a mature full-featured Python testing tool that helps you write better programs
======== ===============================================================================================================


Source Code
===========

The structure of repository is based on the recommended sample in `The Hitchhiker's Guide to Python`_

==================  ====================================================================================================
Path                Content
==================  ====================================================================================================
``./benchmarks/``   builtin benchmark assets including plan, QPI and metrics
``./contrib/``      independent project/plugin/code contributed to QTIP
``./docker/``       configuration for building Docker image for QTIP deployment
``./docs/``         release notes, user and developer documentation, design proposals
``./legacy/``       legacy obsoleted code that is unmaintained but kept for reference
``./opt/``          optional component, e.g. scripts to setup infrastructure services for QTIP
``./qtip/``         the actual package
``./tests/``        package functional and unit tests
``./third-party/``  third part included in QTIP project
==================  ====================================================================================================


Coding Style
============

QTIP follows `OpenStack Style Guidelines`_ for source code and commit message.

Specially, it is recommended to link each patch set with a JIRA issue. Put::

    JIRA: QTIP-n

in commit message to create an automatic link.


Testing
=======

All testing related code are stored in ``./tests/``

==================  ====================================================================================================
Path                Content
==================  ====================================================================================================
``./tests/data/``   data fixtures for testing
``./tests/unit/``   unit test for each module, follow the same layout as ./qtip/
``./conftest.py``   pytest configuration in project scope
==================  ====================================================================================================

`tox`_ is used to automate the testing tasks

.. code-block:: shell

    cd <project_root>
    pip install tox
    tox

The test cases are written in `pytest`_. You may run it selectively with

.. code-block:: shell

    pytest tests/unit/reporter

.. _Connexion: https://pypi.python.org/pypi/connexion/
.. _Click: http://click.pocoo.org/
.. _Jinja2: http://jinja.pocoo.org/
.. _OpenStack Style Guidelines: http://docs.openstack.org/developer/hacking/
.. _pytest: http://doc.pytest.org/
.. _sphinx: http://www.sphinx-doc.org/en/stable/
.. _The Hitchhiker's Guide to Python: http://python-guide-pt-br.readthedocs.io/en/latest/writing/structure/
.. _tox: https://tox.readthedocs.io/
