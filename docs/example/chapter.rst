.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


*************
Chapter Title
*************

There is more than one way to write reStructuredText, the following markups are most common in QTIP documentation.

Section
=======

Subsection
----------

Subsubsection
^^^^^^^^^^^^^

Paragraph
"""""""""

Markups
=======

Inline
------

The standard reST inline markup is quite simple: use

* one asterisk: *text* for emphasis (italics),
* two asterisks: **text** for strong emphasis (boldface), and
* backquotes: ``text`` for code samples.

List
----

* This is a bulleted list.
* It has two items, the second
 item uses two lines.

1. This is a numbered list.
2. It has two items too.

#. This is a numbered list.
#. It has two items too.


Nested lists, note the blank lines after parent list items

* this is
* a list

  * with a nested list
  * and some subitems

* and here the parent list continues

Code
----

Start a code blocks with double colon::

    paths:
      /plans/{name}:
        get:
          summary: Get a plan by plan name
          operationId: qtip.api.controllers.plan.get_plan

Note the code block must be indented.

Or create one explicitly and specify the language

.. code-block:: python

    @common.check_endpoint_for_error(resource='Plan')
    def get_plan(name):
        plan_spec = plan.Plan(name)
        return plan_spec.content



Tables
------

Grid Table
^^^^^^^^^^

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | ...        | ...      |          |
+------------------------+------------+----------+----------+

Simple tables
^^^^^^^^^^^^^

Limited to one line per row

=====  =====  =======
A      B      A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======

Hyperlinks
----------

Create `hyperlinks`_ and list them separately at the end of section or chapter

.. _hyperlinks: http://example.com

