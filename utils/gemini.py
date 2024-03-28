import google.generativeai as genai
from dotenv import load_dotenv
from utils.helper import *
import PIL.Image
import os
import io

load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

class genAI:
    """ genAI is a class that utilizes the google gemini api
        to generate text response from an image """
    def __init__(self):
        """ This initializes the genAI class """
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def generateResponse(self, image):
        img = PIL.Image.open(io.BytesIO(image))
        file_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
        text = read_text_from_file(file_path)
        response = self.model.generate_content([text, img], stream=True)
        response.resolve()
        return parse_response_to_json(response.text)
