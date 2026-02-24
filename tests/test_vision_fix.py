
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ollama_cli.core.ollama import OllamaClient

class TestVisionFix(unittest.TestCase):
    @patch('requests.get')
    def test_get_available_models_includes_vision(self, mock_get):
        # Mock response from Ollama API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {"name": "llama3.2:latest"},
                {"name": "llama3.2-vision:latest"},
                {"name": "mistral:latest"}
            ]
        }
        mock_get.return_value = mock_response
        
        client = OllamaClient()
        
        # Test without vision (default)
        models = client.get_available_models(include_vision=False)
        self.assertIn("llama3.2:latest", models)
        self.assertIn("mistral:latest", models)
        self.assertNotIn("llama3.2-vision:latest", models)
        
        # Test with vision
        models_with_vision = client.get_available_models(include_vision=True)
        self.assertIn("llama3.2:latest", models_with_vision)
        self.assertIn("llama3.2-vision:latest", models_with_vision)
        self.assertIn("mistral:latest", models_with_vision)

    @patch('requests.get')
    @patch('subprocess.run')
    @patch('requests.post')
    def test_describe_image_no_pull_if_exists(self, mock_post, mock_run, mock_get):
        # Mock available models to include vision
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [{"name": "llama3.2-vision"}]
        }
        mock_get.return_value = mock_response
        
        # Mock chat response
        mock_chat_response = MagicMock()
        mock_chat_response.status_code = 200
        mock_chat_response.json.return_value = {"message": {"content": "A cat"}}
        mock_post.return_value = mock_chat_response
        
        with patch('builtins.open', unittest.mock.mock_open(read_data=b"fake_image_data")):
            client = OllamaClient()
            client.describe_image("fake_path.png", model="llama3.2-vision")
        
        # Verify subprocess.run (for ollama pull) was NOT called for this model
        for call in mock_run.call_args_list:
            cmd = call[0][0]
            if "ollama pull" in cmd:
                self.fail("ollama pull was called even though model was available")

if __name__ == "__main__":
    unittest.main()
