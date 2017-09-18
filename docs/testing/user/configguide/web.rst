.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


***************************************
Web Portal installation & configuration
***************************************

Web Portal for Benchmarking is developed on python `Django`_ Framework. Right now the installation
is need to be done from source.



Clone QTIP Repo
===============

::

    git clone https://github.com/opnfv/qtip.git


Setup database and Initialize user data
=======================================

CD into `web` directory.
------------------------

::

    cd qtip/qtip/web


Setup migrations
----------------

::

    python manage.py makemigrations


In usual case migrations will be already available with source. Console willll notify you
of the same.

Run migrations
--------------

::

    python manage.py migrate


Create superuser
----------------
::

    python manage.py createsuperuser


Console will prompt for adding new web admin. Enter new credentials.



Collecting Static Dependencies
------------------------------
::

    python manage.py importstatic


This will import js and css dependencies for UI in static directory. Now the web application is
ready to run.


.. _Django: https://docs.djangoproject.com/en/1.11/
