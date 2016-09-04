import pytest
import mock
import os
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
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel', 'PWD': '/home'})
        with pytest.raises(SystemExit):
            k.start()
            cli(test_input)
            k.stop()
        resout, reserr = capfd.readouterr()
        assert expected in resout

    @pytest.mark.parametrize("test_input, expected", [
        (['-l',
          'zte-pod1',
          '-f',
          'storage'], [('fuel', '/home', './test_cases/zte-pod1/storage/fio_bm.yaml'),
                       ('fuel', '/home', './test_cases/zte-pod1/storage/fio_vm.yaml')])
    ])
    @mock.patch('func.cli.args_handler.prepare_and_run_benchmark')
    def test_cli_successful(self, mock_args_handler, test_input, expected):
        k = mock.patch.dict(os.environ, {'INSTALLER_TYPE': 'fuel', 'PWD': '/home'})
        k.start()
        cli(test_input)
        k.stop()
        call_list = map(lambda x: mock_args_handler.call_args_list[x][0], range(len(expected)))
        assert sorted(call_list) == sorted(expected)
