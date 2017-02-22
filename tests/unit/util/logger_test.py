import pytest

from qtip.util import logger


def debug_exist(content):
    assert 'debug level test' in content


def debug_notexist(content):
    assert 'debug level test' not in content


@pytest.mark.parametrize('debug, expected', [
    ('true', debug_exist),
    ('false', debug_notexist)])
def test_logger(monkeypatch, tmpdir, capsys, debug, expected):
    monkeypatch.setenv('IF_DEBUG', debug)

    filename = 'test_logger'
    tmpdir_fie = tmpdir.join('{}.log'.format(filename))
    logger.QtipLogger.file_path = str(tmpdir)

    log = logger.QtipLogger(filename).get
    log.error('error level test')
    log.info('info level test')
    log.debug('debug level test')

    file_content = tmpdir_fie.read()
    print file_content
    assert 'error level test' in file_content
    assert 'info level test' in file_content
    assert 'debug level test' in file_content
    
    _, err = capsys.readouterr()

    expected(err)
