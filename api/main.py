from fastapi import FastAPI, File, UploadFile
from utils.gemini import genAI

app = FastAPI()

@app.get('/')
async def home():
    return {"message": "Welcome to the BioDetect API",
            "info": "You have to send a POST request to /detect with an image of an animal, insect, or plant to elicit a response from the API.",
            "additional_info": "The API accepts images in common formats such as JPG, PNG, and GIF. Make sure to provide clear and focused images for accurate detection results.",
            "json_response_format": {
                "species": "",
                "common_name": "",
                "scientific_name": "",
                "classification": "",
                "physical_characteristics": "",
                "behavioral_traits": "",
                "habitat": "",
                "geographic_distribution": "",
                "diet_and_feeding_habits": "",
                "reproduction_and_lifecycle": "",
                "conservation_status": "",
                "interactions_with_other_species": "",
                "adaptations_to_the_environment": "",
                "threats_and_challenges": "",
                "conservation_efforts_and_initiatives": ""
                },
            "author": "Nnaemeka Daniel John",
            "powered_by": "google gemini-pro-vision"
            }

@app.post('/detect')
async def detect(image: UploadFile = File(...)):
    image_content = await image.read()
    ai = genAI()
    response = ai.generateResponse(image=image_content)
    return response
