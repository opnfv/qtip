import pytest
import yaml

from click.testing import CliRunner
from qtip.cli.entry import cli


class TestClass(object):

    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test(self, runner):
        with open("helper/perftest.yaml") as perftest:
            content = perftest.read()
            data = yaml.safe_load(content)['tests']
            for i in range(0, len(data)):
                result = runner.invoke(cli, data[i]['command'])
                assert result.output == data[i]['output']
