import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from io import BytesIO
from PIL import Image
from gemini.gemini import GenAI, genai

class TestGenAI(unittest.TestCase):

    @patch('gemini.gemini.genai.GenerativeModel')
    @patch('PIL.Image.open')
    @patch('builtins.open', new_callable=mock_open, read_data="test prompt")
    @patch('gemini.helper.read_text_from_file', return_value="test prompt")
    @patch('os.path.exists', return_value=True)
    def test_generate_response_success(self, mock_exists, mock_read_text, mock_open_builtin, mock_open_image, mock_GenerativeModel):
        # Setup
        mock_model = mock_GenerativeModel.return_value
        mock_model.generate_content.return_value = MagicMock(text='{"result": "test result"}')
        mock_open_image.return_value = MagicMock(spec=Image.Image)
        image_content = b'test image content'

        genai_instance = GenAI()

        # Test
        response = genai_instance.generateResponse(image_content)

        # Validate
        self.assertEqual(response, {
            'error': 'Not an image of a living organism (plant, insect or animal)',
            'next_steps': 'Insert a clear image of a plant, insect, or animal and try again.'
            })
        mock_model.generate_content.assert_called_once()

    @patch('PIL.Image.open')
    def test_generate_response_invalid_image(self, mock_open_image):
        # Setup
        mock_open_image.side_effect = ValueError("Invalid image")
        image_content = BytesIO(b'invalid image content')

        genai_instance = GenAI()

        # Test
        response = genai_instance.generateResponse(image_content)

        # Validate
        self.assertTrue('error' in response)

    @patch('os.path.exists', return_value=False)
    def test_generate_response_missing_prompt_file(self, mock_exists):
        # Setup
        image_content = BytesIO(b'test image content')

        genai_instance = GenAI()

        # Test
        response = genai_instance.generateResponse(image_content)

        # Validate
        self.assertTrue('error' in response)

    @patch('gemini.gemini.genai.GenerativeModel')
    @patch('PIL.Image.open')
    @patch('builtins.open', new_callable=mock_open, read_data="test prompt")
    @patch('gemini.helper.read_text_from_file', return_value="test prompt")
    @patch('os.path.exists', return_value=True)
    def test_generate_response_model_error(self, mock_exists, mock_read_text, mock_open_builtin, mock_open_image, mock_GenerativeModel):
        # Setup
        mock_model = mock_GenerativeModel.return_value
        mock_model.generate_content.side_effect = Exception("Model error")
        image_content = BytesIO(b'test image content')

        genai_instance = GenAI()

        # Test
        response = genai_instance.generateResponse(image_content)

        # Validate
        self.assertTrue('error' in response)
