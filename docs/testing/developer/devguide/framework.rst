.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.


*********
Framework
*********

QTIP is built upon `Ansible`_ by extending `modules`_, `playbook roles`_ and `plugins`_.

.. _Ansible: https://www.ansible.com/
.. _modules: http://docs.ansible.com/ansible/modules.html
.. _playbook roles: http://docs.ansible.com/ansible/playbooks_roles.html
.. _plugins: http://docs.ansible.com/ansible/dev_guide/developing_plugins.html

Modules
=======

QTIP creates dedicated modules to gather slave node list and information from installer master. See embedded document
in ``qtip/ansible_library/modules`` for details

Plugins
=======

Stored in ``qtip/ansible_library/plugins``

Action plugins
--------------

Several action plugins have been created for test data post processing

* collect - parse and collect metrics from raw test results like log files
* calculate - calculate score according to specification
* aggregate - aggregate calculated results from all hosts under test

Playbook roles
==============

