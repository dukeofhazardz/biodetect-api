import io
import shutil
from googleapiclient.discovery import build
import shutil
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class DriveAPI:
    """
    A class representing a Google Drive API client.

    This class provides methods for interacting with Google Drive,
    including authentication, token management, and file download.

    Attributes:
        SCOPES (list): List of OAuth 2.0 scopes required for accessing Google Drive API.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        """
        Initializes a new instance of the DriveAPI class.

        This constructor sets up authentication and establishes a connection to the Google Drive API.
        If a valid access token is not found, it initiates the OAuth 2.0 authorization flow to obtain one.
        """
        self.creds = Credentials.from_service_account_file('service_account_key.json', scopes=self.SCOPES)
        # Connects to the API service
        self.service = build('drive', 'v3', credentials=self.creds)

    def FileDownload(self, file_id, file_name):
        """
        Downloads a file from Google Drive.

        Parameters:
            file_id (str): The ID of the file to download.
            file_name (str): The name of the file to save the downloaded content to.

        Returns:
            bool: True if the file download is successful, False otherwise.
        """
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()

        # Initialises a downloader object to download the file
        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False

        try:
            # Downloads the data in chunks
            while not done:
                status, done = downloader.next_chunk()

            fh.seek(0)

            # Writes the received data to the file
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)
            return True
        except Exception:
            return False
