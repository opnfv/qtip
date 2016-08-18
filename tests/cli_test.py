import pytest
from func.cli import cli


class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        (['-l',
          'zte',
          '-f',
          'compute'], "You have specified a lab that is not present in test_cases"),
        (['-l',
          'zte-pod1',
          '-f',
          'test'], "Test File Does not exist in test_list")
    ])
    def test_cli_error(self, capfd, test_input, expected):
        with pytest.raises(SystemExit):
            cli(test_input)
        resout, reserr = capfd.readouterr()
        assert expected in resout
