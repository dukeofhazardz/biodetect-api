import unittest
from unittest.mock import patch, MagicMock
from prompt.prompt import DriveAPI

class TestDriveAPI(unittest.TestCase):

    @patch('prompt.prompt.build')
    def test_file_download_failure(self, mock_build):
        # Arrange
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_files = MagicMock()
        mock_service.files.return_value = mock_files
        mock_media = MagicMock()
        mock_files.get_media.return_value = mock_media
        mock_io = MagicMock()
        mock_bytes_io = MagicMock()
        mock_io.BytesIO.return_value = mock_bytes_io
        mock_fh = MagicMock()
        mock_bytes_io.return_value = mock_fh
        mock_downloader = MagicMock()
        mock_media.return_value = mock_downloader
        mock_downloader.next_chunk.side_effect = Exception("Test Error")
        file_id = '1g5iPWk5tf7HTRK39GwrOFLZRoqMPCttW'
        file_name = 'prompt.txt'

        # Act
        drive_api = DriveAPI()
        result = drive_api.FileDownload(file_id, file_name)

        # Assert
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
