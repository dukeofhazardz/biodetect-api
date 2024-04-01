import pickle
import os.path
import io
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload


class DriveAPI:
    global SCOPES


# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']


def __init__(self):
    """ Variable self.creds will store the user access token.
        If no valid token found it will create one. """
    self.creds = None

    # Check if file token.pickle exists
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

        # Save the access token in token.pickle file for future usage
        with open('token.pickle', 'wb') as token:
            pickle.dump(self.creds, token)

    # Connect to the API service
    self.service = build('drive', 'v3', credentials=self.creds)


def FileDownload(self, file_id, file_name):
    request = self.service.files().get_media(fileId=file_id)
    fh = io.BytesIO()

    # Initialise a downloader object to download the file
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    done = False

    try:
        # Download the data in chunks
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)

        # Write the received data to the file
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(fh, f)

        print("File Downloaded")
        return True
    except Exception as e:
        print("Something went wrong: ", e)
        return False
