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


Branching
=========

Stable branches are created when features are frozen for next release. According to
`OPNFV release milestone description`_, stable branch window is open on MS6 and closed on MS7.

#. Contact gerrit admin <opnfv-helpdesk@rt.linuxfoundation.org> to create branch for project.
#. Setup `qtip jobs`_ and `docker jobs`_ for stable branch in releng
#. Follow `instructions for stable branch`_.

NOTE: we do **NOT** create branches for feature development as in the popular `GitHub Flow`_


Releasing
=========

Tag Deliverable and write release note

Git repository
--------------

Follow the example in `Git Tagging Instructions for Danube`_ to tag the source code::

    git fetch gerrit
    git checkout stable/<release-name>
    git tag -am "<release-version>" <release-version>
    git push gerrit <release-version>

Docker image
------------

#. Login `OPNFV Jenkins`_
#. Go to the `qtip-docker-build-push-<release>`_ and click "Build With Parameters"
#. Fill in ``RELEASE_VERSION`` with version number not including release name, e.g. ``1.0``
#. Trigger a manual build

Python Package
--------------

QTIP is also available as a Python Package. It is hosted on the Python Package Index(PyPI).

#. Install twine with ``pip install twine``
#. Build the distributions ``python setup.py  sdist bdist_wheel``
#. Upload the distributions built with ``twine upload dist/*``

NOTE: only package **maintainers** are permitted to upload the package versions.

Release note
------------

Create release note under ``qtip/docs/release/release-notes`` and update ``index.rst``

.. _Connexion: https://pypi.python.org/pypi/connexion/
.. _Click: http://click.pocoo.org/
.. _Jinja2: http://jinja.pocoo.org/
.. _OpenStack Style Guidelines: http://docs.openstack.org/developer/hacking/
.. _pytest: http://doc.pytest.org/
.. _sphinx: http://www.sphinx-doc.org/en/stable/
.. _The Hitchhiker's Guide to Python: http://python-guide-pt-br.readthedocs.io/en/latest/writing/structure/
.. _tox: https://tox.readthedocs.io/
.. _OPNFV release milestone description: https://wiki.opnfv.org/display/SWREL/Release+Milestone+Description
.. _qtip jobs: https://git.opnfv.org/releng/tree/jjb/qtip/
.. _docker jobs: https://git.opnfv.org/releng/tree/jjb/releng/opnfv-docker.yml
.. _instructions for stable branch: https://wiki.opnfv.org/display/SWREL/Stablebranch
.. _GitHub Flow: https://guides.github.com/introduction/flow/
.. _Git Tagging Instructions for Danube: https://wiki.opnfv.org/display/SWREL/Git+Tagging+Instructions+for+Danube
.. _OPNFV Jenkins: https://build.opnfv.org/ci/view/qtip/
.. _docker build job: https://build.opnfv.org/ci/view/qtip/job/qtip-docker-build-push-danube/
