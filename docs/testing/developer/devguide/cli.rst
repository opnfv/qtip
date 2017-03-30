.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


****************************
CLI - Command Line Interface
****************************

QTIP consists of different tools(metrics) to benchmark the NFVI. These metrics fall under different NFVI
subsystems(QPI's) such as compute, storage and network. A plan consists of one or more QPI's, depending upon how
the end user would want to measure performance. CLI is designed to help the user, execute benchmarks and
view respective scores.

Framework
=========

QTIP CLI has been created using the Python package `Click`_, Command Line Interface Creation Kit. It has been
chosen for number of reasons. It presents the user with a very simple yet powerful API to build complex
applications. One of the most striking features is command nesting.

As explained, QTIP consists of metrics, QPI's and plans. CLI is designed to provide interface to all
these components. It is responsible for execution, as well as provide listing and details of each individual
element making up these components.

Design
======

CLI's entry point extends Click's built in MultiCommand class object. It provides two methods, which are
overridden to provide custom configurations.

.. code-block:: python

    class QtipCli(click.MultiCommand):

        def list_commands(self, ctx):
            rv = []
            for filename in os.listdir(cmd_folder):
                if filename.endswith('.py') and \
                    filename.startswith('cmd_'):
                    rv.append(filename[4:-3])
            rv.sort()
            return rv

        def get_command(self, ctx, name):
            try:
                if sys.version_info[0] == 2:
                    name = name.encode('ascii', 'replace')
                mod = __import__('qtip.cli.commands.cmd_' + name,
                                 None, None, ['cli'])
            except ImportError:
                return
            return mod.cli

Commands and subcommands will then be loaded by the ``get_command`` method above.

Extending the Framework
=======================

Framework can be easily extended, as per the users requirements. One such example can be to override the builtin
configurations with user defined ones. These can be written in a file, loaded via a Click Context and passed
through to all the commands.

.. code-block:: python

   class Context:

       def __init__():

           self.config = ConfigParser.ConfigParser()
           self.config.read('path/to/configuration_file')

       def get_paths():

           paths = self.config.get('section', 'path')
           return paths

The above example loads configuration from user defined paths, which then need to be provided to the actual
command definitions.

.. code-block:: python

   from qtip.cli.entry import Context

   pass_context = click.make_pass_decorator(Context, ensure=False)

   @cli.command('list', help='List the Plans')
   @pass_context
   def list(ctx):
       plans = Plan.list_all(ctx.paths())
       table = utils.table('Plans', plans)
       click.echo(table)

.. _Click: http://click.pocoo.org/5/
