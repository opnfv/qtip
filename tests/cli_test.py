import pytest
import mock
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

    @pytest.mark.parametrize("test_input, expected", [
        (['-l',
          'zte-pod1',
          '-f',
          'storage'], [('./test_cases/zte-pod1/storage/fio_bm.yaml'),
                       ('./test_cases/zte-pod1/storage/fio_vm.yaml')])
    ])
    @mock.patch('func.cli.args_handler.prepare_and_run_benchmark')
    def test_cli_successful(self, mock_args_handler, test_input, expected):
        cli(test_input)
        call_list = map(lambda x: mock_args_handler.call_args_list[x][0][0], range(len(expected)))
        assert sorted(call_list) == sorted(expected)
