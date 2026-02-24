
import sys
import os
import unittest
import json
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ollama_cli.main import OllamaCLI

class TestLoopPrevention(unittest.TestCase):
    def setUp(self):
        # Prevent loading real config
        with patch('ollama_cli.main.load_config') as mock_load:
            mock_load.return_value = {"ollama_url": "http://localhost:11434"}
            self.cli = OllamaCLI()

    @patch('ollama_cli.main.OllamaClient.chat')
    @patch('ollama_cli.main.OllamaCLI.execute_tool')
    def test_prevent_vision_loop(self, mock_execute, mock_chat):
        # 1. First iteration: Model calls analyze_image
        # 2. Second iteration: Model calls analyze_image again with same path but different (long) prompt
        
        image_path = "/path/to/image.png"
        first_result = "There is a boy on a swing in a park with green grass." # > 30 chars
        
        # Mock chat to return tool call in first iteration, then some text in second
        def chat_side_effect(messages, model):
            # Check if we already have the first result in history
            if any(first_result in m["content"] for m in messages if m["role"] == "user"):
                # This is iteration 2, model is trying to repeat the result as a prompt
                yield f'<tool_call><tool_name>analyze_image</tool_name><parameters>{{"image_path": "{image_path}", "prompt": "{first_result}"}}</parameters></tool_call>'
            else:
                # This is iteration 1
                yield f'<tool_call><tool_name>analyze_image</tool_name><parameters>{{"image_path": "{image_path}", "prompt": "What is in the image?"}}</parameters></tool_call>'
        
        mock_chat.side_effect = chat_side_effect
        mock_execute.return_value = first_result
        
        # Run chat cycle
        self.cli.messages = [{"role": "user", "content": "What's in the image?"}]
        self.cli.process_chat_cycle()
        
        # Verify execute_tool was called only ONCE for analyze_image on this path
        # Actually it should be called once, then the second one blocked.
        # But wait, the second one has a different prompt so it wouldn't be blocked by the generic call_key
        # but SHOULD be blocked by our new vision_path check.
        
        call_count = 0
        for call in mock_execute.call_args_list:
            if call[0][0] == "analyze_image":
                call_count += 1
        
        self.assertEqual(call_count, 1, f"analyze_image was called {call_count} times, expected 1 (loop prevention failed)")

if __name__ == "__main__":
    unittest.main()
