import google.generativeai as genai
from dotenv import load_dotenv
from gemini.helper import *
from prompt.prompt import DriveAPI
import PIL.Image
import os
import io

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FILE_NAME = os.getenv("FILE_NAME")
FILE_ID = os.getenv("FILE_ID")


generation_config = {
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 2,
    "max_output_tokens": 1024,
}


safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT",
     "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",
     "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
     "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
     "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]


class genAI:
    """ genAI is a class that utilizes the google gemini api
        to generate text response from an image """
    def __init__(self):
        """ This initializes the genAI class """
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro-vision',
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

    def generateResponse(self, image):
        try:
            img = PIL.Image.open(io.BytesIO(image))
        except Exception as e:
            return {"error": f"Error opening image: {str(e)}"}
        file_path = os.path.join(os.path.dirname(__file__), "..", FILE_NAME)
        text = ""
        if os.path.exists(file_path):
            text = read_text_from_file(file_path)
        else:
            drive_api = DriveAPI()
            drive_api.FileDownload(file_id=FILE_ID, file_name=FILE_NAME)
            text = read_text_from_file(file_path)

        try:
            response = self.model.generate_content([text, img])
            response.resolve()
            return parse_response_to_json(response.text)
        except Exception as e:
            return {"error": str(e)}
