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


class GenAI:
    """ This class houses the functionality for generating text response from
        an image using the Google Gemini API. It initializes the API model and
        provides a method to generate a response based on the input image.
    """
    def __init__(self):
        """ Initializes an instance of the GenAI class
        """
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro-vision',
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

    def generateResponse(self, image):
        """ Generates a text response from the input image.
        Parameters:
        @image: The input image content.
        Returns: A JSON object containing the generated text response or an error message if an exception occurs during the process.
        """
        print("in generate res function")
        try:
            img = PIL.Image.open(io.BytesIO(image))
        except Exception as e:
            print("'error': f'Error opening image: {str(e)}'")
            return {"error": f"Error opening image: {str(e)}"}
        print("open image file")
        file_path = os.path.join(os.path.dirname(__file__), "..", FILE_NAME)
        text = ""
        if os.path.exists(file_path):
            text = read_text_from_file(file_path)
            print("file exists")
        else:
            drive_api = DriveAPI()
            drive_api.FileDownload(file_id=FILE_ID, file_name=FILE_NAME)
            text = read_text_from_file(file_path)

        try:
            response = self.model.generate_content([text, img])
            print("content generated")
            response.resolve()
            print("content parsed")
            return parse_response_to_json(response.text)
        except Exception as e:
            print("'error'': str(e)")
            return {"error": str(e)}
