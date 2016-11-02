####################
Contributing to QTIP
####################

First of all, thanks for taking your time to contribute.

QTIP is a project in OPNFV. If you are new to OPNFV, you may read
:title:`Developer Getting Started`_ first.

***********
Peer Review
***********

Peer review is the most important communication channel between developers.
Every subtle change to the code or document **MUST** be reviewed before
submission.

Please make sure there is at least one ``+1`` or ``+2`` from others before
submitting[#f1] a patch set.

****************
Tasks and Issues
****************

Tasks and issues are management in `JIRA`_. The usage of different
:title:`Issue Types`_ in QTIP are as following:

* ``Task``: it must be achievable in **one sprint**, otherwise it needs to be split.
* ``Sub-Task``: it must be resolvable by **one developer** within **one sprint**,
otherwise it need to be split.

``Bug``, ``New Feature``, ``Improvement``, ``Story`` and ``Epic`` are not
restricted by time frame. But it is recommended to to define the scope clearly
and break down into manageable tasks.

*****************
Development Cycle
*****************

QTIP follows the cycle of `OPNFV Releases`_ which is approximately one release
every half year.

The tasks are organized by sprints, three weeks for each.

The target and content of each sprint is discussed in weekly meeting.

************
Coding Style
************

QTIP follows :title:`OpenStack Style Guidelines`_ for source code and commit message.

Specially, it is recommended to link each patch set with a JIRA issue. Put

    JIRA: QTIP-n

in commit message to create an automatic link.

*************
Documentation
*************

The documents are built automatically by sphinx from reStructuredText (reST).
Please read `reStructuredText Primer`_ if you are not familiar with it.

A cheat sheet for headings are as following

* # with overline, for parts
* * with overline, for chapters
* =, for sections
* -, for subsections
* ^, for subsubsections
* ", for paragraphs

************************
Frequent Asked Questions
************************

Q: May I work on task which have already been assigned to others?
A: Yes. But please make sure you have contacted the original assignee to avoid
overlapping.

.. rubric:: Footnotes

.. [#f1] only members in ``ldap/opnfv-gerrit-qtip-submitters`` have permission
to submit. The current members are listed in `INFO`_.

.. rubric:: Reference

.. _Developer Getting Started: https://wiki.opnfv.org/display/DEV/Developer+Getting+Started
.. _JIRA: https://jira.opnfv.org/browse/QTIP
.. _OPNFV Releases: https://wiki.opnfv.org/display/SWREL
.. _Issue Types: https://jira.opnfv.org/secure/ShowConstantsHelp.jspa?decorator=popup#IssueTypes
.. _OpenStack Style Guidelines: http://docs.openstack.org/developer/hacking/
.. _INFO: https://git.opnfv.org/cgit/qtip/tree/INFO
.. _reStructuredText Primer: http://www.sphinx-doc.org/en/stable/rest.html
