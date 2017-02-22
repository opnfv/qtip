import pytest
from qtip.util import logger

module = 'test_logger'
error_message = 'error level test'
info_message = 'info level test'
debug_message = 'debug level test'


@pytest.fixture()
def env_home(monkeypatch, tmpdir):
    monkeypatch.setenv('HOME', str(tmpdir))
    return tmpdir


@pytest.fixture()
def logger_file(env_home):
    return env_home.mkdir('qtip').mkdir('logs').join('{}.log'.format(module))


def console_expect_debug(content):
    assert debug_message in content


def console_expect_nodebug(content):
    assert debug_message not in content


@pytest.mark.parametrize('debug, console_expected', [
    ('true', console_expect_debug),
    ('false', console_expect_nodebug)])
def test_logger(monkeypatch, capsys, logger_file, debug, console_expected):
    monkeypatch.setenv('IF_DEBUG', debug)

    log = logger.QtipLogger(module).get
    log.error(error_message)
    log.info(info_message)
    log.debug(debug_message)

    file_print = logger_file.read()
    assert error_message in file_print
    assert info_message in file_print
    assert debug_message in file_print

    _, console_print = capsys.readouterr()

    console_expected(console_print)
