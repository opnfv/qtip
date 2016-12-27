import os
import pytest
import sys
import yaml

from click.testing import CliRunner
from qtip.cli.entry import cli


class TestClass(object):

    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test(self, runner):
        unit = 'perftest'
        test_file = 'data/helper/' + unit + '.yaml'
        path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, test_file)

        with open(path) as trial:
            content = trial.read()
            data = yaml.safe_load(content)['tests']
            if data is None:
                print("Unit Test does not exist")
                sys.exit(1)
            else:
                for i in range(0, len(data)):
                    result = runner.invoke(cli, data[i]['command'])
                    assert result.output == data[i]['output']
