import pytest
import mock
import os
from func.cli import Cli


class TestClass:
    @pytest.mark.parametrize("test_input, expected", [
        (['-l',
          'zte',
          '-f',
          'compute'], "You have specified a lab that is not present in test_cases"),
        (['-l',
          'default',
          '-f',
          'test'], "This suite file doesn't exist under benchmarks/suite/")
    ])
    def test_cli_error(self, capfd, test_input, expected):
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel', 'PWD': '/home'})
        with pytest.raises(SystemExit):
            k.start()
            Cli(test_input)
            k.stop()
        resout, reserr = capfd.readouterr()
        assert expected in resout

    @pytest.mark.parametrize("test_input, expected", [
        (['-l',
          'default',
          '-f',
          'storage'], [('fuel', '/home', './test_cases/default/storage/fio_bm.yaml'),
                       ('fuel', '/home', './test_cases/default/storage/fio_vm.yaml')])
    ])
    @mock.patch('func.cli.args_handler.prepare_and_run_benchmark')
    def test_cli_successful(self, mock_args_handler, test_input, expected):
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel', 'PWD': '/home'})
        k.start()
        Cli(test_input)
        k.stop()
        call_list = map(lambda x: mock_args_handler.call_args_list[x][0], range(len(expected)))
        assert sorted(call_list) == sorted(expected)
