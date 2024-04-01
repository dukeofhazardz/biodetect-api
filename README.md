# BioDetect API

The BioDetect API is a tool designed to detect various organisms based on images provided to the API. It utilizes machine learning models to analyze images and provide information about the detected organism.

## Usage

### Home Endpoint

- **Method:** GET
- **URL:** `/`
- **Description:** Returns information about the BioDetect API and instructions on how to use it.
- **Response:**
  ```json
  {
      "message": "Welcome to the BioDetect API",
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
  ```

### Detection Endpoint

- **Method:** POST
- **URL:** `/detect`
- **Description:** Detects an organism based on the image provided in the request.
- **Request Body:** Upload a file containing the image of the organism.
- **Response:** Returns detailed information about the detected organism.
  
## Author
- Nnaemeka Daniel John

## Powered By
- Google Gemini-Pro-Vision