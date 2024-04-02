import pickle
import os.path
import io
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload


class DriveAPI:
    """
    A class representing a Google Drive API client.

    This class provides methods for interacting with Google Drive,
    including authentication, token management, and file download.

    Attributes:
        SCOPES (list): List of OAuth 2.0 scopes required for accessing Google Drive API.
    """
    global SCOPES

    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        """
        Initializes a new instance of the DriveAPI class.

        This constructor sets up authentication and establishes a connection to the Google Drive API.
        If a valid access token is not found, it initiates the OAuth 2.0 authorization flow to obtain one.
        """
        self.creds = None

        # Checks if file token.pickle exists
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If no valid credentials are available, request the user to log in.
        if not self.creds or not self.creds.valid:

            # If token is expired, it will be refreshed, else,
            # we will request a new one.
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Saves the access token in token.pickle file for future usage
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

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
