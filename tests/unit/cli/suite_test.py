import pytest
import yaml
import os

from click.testing import CliRunner
from qtip.cli.entry import cli


class TestClass(object):

    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test(self, runner):
        path = os.path.join(os.path.dirname(__file__), 'helper/suite.yaml')
        with open(path) as suite:
            content = suite.read()
            data = yaml.safe_load(content)['tests']
            for i in range(0, len(data)):
                result = runner.invoke(cli, data[i]['command'])
                assert result.output == data[i]['output']
