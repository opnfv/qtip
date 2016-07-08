import mock
from func.fetchimg import FetchImg


class TestClass:
    @mock.patch('func.fetchimg.os')
    @mock.patch('func.fetchimg.os.path')
    def test_fetch_img_success(self, mock_path, mock_os):
        mock_os.system.return_value = True
        mock_path.isfile.return_value = True
        img = FetchImg()
        img.download()

    @mock.patch('func.fetchimg.time')
    @mock.patch('func.fetchimg.os.system')
    @mock.patch('func.fetchimg.os.path')
    def test_fetch_img_fail(self, mock_path, mock_system, mock_time):
        img = FetchImg()
        mock_system.return_value = True
        mock_path.isfile.side_effect = [False, True]
        img.download()
        assert mock_time.sleep.call_count == 2
