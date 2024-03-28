import requests
import os
from utils.gemini import genAI
from utils.helper import read_text_from_file

genai = genAI()
# URL of the API endpoint
url = 'http://localhost:8000/detect'

# Path to the image file you want to upload
image_path = 'imgs/images.jpg'

# Open the image file in binary mode
with open(image_path, 'rb') as file:
    # Create a dictionary to hold the file and any additional data (if needed)
    files = {"image": file}

    # Make a POST request to the API endpoint with the image file
    response = requests.post(url, files=files)
    """file_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    print(file_path)
    text = read_text_from_file(file_path)
    response = genai.generateResponse(image=image_content, text=text)"""

# Print the response from the server
print(response.content)
