Contributing to QTIP
====================

First of all, thanks for taking your time to contribute.

QTIP is a project in OPNFV. If you are new to OPNFV, you may read
[Developer Getting Started][gs] first.

Peer Review
-----------

Peer review is the most important communication channel between developers.
Every subtle change to the code or document **MUST** be reviewed before
submission.

Add group `qtip-reviewers` in [gerrit][gr] when you consider a patch set is
ready.


Rule for Submit
---------------

Only members in `ldap/opnfv-gerrit-qtip-submitters`, i.e. committers have
permission to submit. The current committers are listed in [INFO][if].

Before submitting a patch set, please make sure one of the following criteria is
met:

* **Normal**: at least one `+2` from others
* **Fast Track**: no objection from other committers for one or more working day

NOTE: we introduce **fast track** because currently there are not enough active
committers reviewing the patch sets.

Active Reviewers
----------------

Current list of active reviewers in gerrit group `qtip-reviewers`

* Akhil Batra <akhil.batra@research.iiit.ac.in>
* Serena Feng <feng.xiaowei@zte.com.cn>
* Taseer Ahmed <taseer94@gmail.com>
* Yujun Zhang <zhang.yujunz@zte.com.cn>
* Zhifeng Jiang <jiang.zhifeng@zte.com.cn>
* Zhihui Wu <wu.zhihui1@zte.com.cn>

By becoming an active reviewer, you agree to allow others to invite you as
reviewers in QTIP project freely. Any one in OPNFV community can apply to join
QTIP reviewers group or leave by submitting a patch on this document.

Tasks and Issues
----------------

Tasks and issues are management in [JIRA][jr]. The usage of different
[Issue Types][it] in QTIP are as following:

* `Task`: it must be achievable in **one sprint**, otherwise it needs to be split.
* `Sub-Task`: it must be resolvable by **one developer** within **one sprint**,
otherwise it need to be split.

`Bug`, `New Feature`, `Improvement`, `Story` and `Epic` are not
restricted by time frame. But it is recommended to to define the scope clearly
and break down into manageable tasks.

Development Cycle
-----------------

QTIP follows the cycle of [OPNFV Releases][or] which is approximately one release
every half year.

The tasks are organized by sprints, three weeks for each.

The target and content of each sprint is discussed in weekly meeting.

Coding Style
------------

QTIP follows [OpenStack Style Guidelines][os] for source code and commit message.

Specially, it is recommended to link each patch set with a JIRA issue. Put

    JIRA: QTIP-n

in commit message to create an automatic link.

Test Coverage
-------------

The implementation, including new features and bug fix, **must** be covered by
unit test. The criteria for test coverage in QTIP project are as following:

* >=80% coverage for each file
* >=90% overall coverage for whole project

Documentation
-------------

The documents are built automatically by sphinx from reStructuredText (reST).
Please read [reStructuredText Primer][rp] if you are not familiar with it.

Start a new document by copying an example from ``docs/example``

Frequent Asked Questions
------------------------

Q: May I work on task which have already been assigned to others?

A: Yes. But please make sure you have contacted the original assignee to avoid
overlapping.

[gs]: https://wiki.opnfv.org/display/DEV/Developer+Getting+Started
[gr]: https://gerrit.opnfv.org/gerrit/#/q/project:+qtip
[jr]: https://jira.opnfv.org/browse/QTIP
[or]: https://wiki.opnfv.org/display/SWREL
[it]: https://jira.opnfv.org/secure/ShowConstantsHelp.jspa?decorator=popup#IssueTypes
[os]: http://docs.openstack.org/developer/hacking/
[if]: https://git.opnfv.org/cgit/qtip/tree/INFO
[rp]: http://www.sphinx-doc.org/en/stable/rest.html
