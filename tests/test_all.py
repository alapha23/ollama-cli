import unittest
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ollama_cli.core.config import load_config, DEFAULT_CONFIG
from ollama_cli.core.sessions import save_session, load_session, list_sessions
from ollama_cli.tools.base import registry
import ollama_cli.tools.filesystem as fs
import ollama_cli.tools.system as system
import ollama_cli.tools.code as code
import ollama_cli.tools.knowledge as kb
import ollama_cli.tools.memory as memory

import ollama_cli.tools.execution as execution
import ollama_cli.tools.media as media
from unittest.mock import patch, MagicMock

class TestOllamaCLI(unittest.TestCase):
    def test_run_python(self):
        """Test Python execution tool"""
        code_str = "print(1 + 1)"
        res = execution.run_python(code_str)
        self.assertIn("Success", res)
        self.assertIn("2", res)

    @patch('requests.get')
    @patch('requests.post')
    def test_generate_image_mock(self, mock_post, mock_get):
        """Test image generation logic (mocked)"""
        # Mock server is up
        mock_get.return_value.status_code = 200
        # Mock successful queue
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"prompt_id": "mock_id"}
        
        # We need to mock websocket or skip the monitoring part for unit test
        with patch('websocket.WebSocket') as mock_ws:
            # Short circuit the monitoring loop by making recv return empty
            mock_ws.return_value.recv.return_value = None
            res = media.generate_image("a test prompt")
            self.assertIn("Image generation finished", res)

    def test_config_loading(self):
        """Test if config loads and has defaults"""
        cfg = load_config()
        self.assertIn("ollama_url", cfg)
        self.assertIn("comfy_url", cfg)

    def test_session_management(self):
        """Test saving and loading sessions"""
        test_msgs = [{"role": "user", "content": "test message"}]
        name = "test_unit_session"
        path = save_session(test_msgs, name)
        self.assertTrue(os.path.exists(path))
        
        loaded = load_session(name)
        self.assertEqual(loaded, test_msgs)
        
        sessions = list_sessions()
        self.assertIn(name, sessions)
        
        # Cleanup
        os.remove(path)

    def test_tool_registry(self):
        """Test if all tools are registered"""
        tools = [t["name"] for t in registry.list_tools()]
        expected = [
            "read_file", "write_file", "list_directory", "grep_search", "get_tree",
            "execute_bash", "get_env_info",
            "code_analyze_file", "generate_readme", "run_linter", "replace_text",
            "kb_add", "kb_search",
            "remember_fact", "recall_facts", "clear_memory"
        ]
        for e in expected:
            self.assertIn(e, tools, f"Tool {e} missing from registry")

    def test_filesystem_tools(self):
        """Test core filesystem tools"""
        test_file = "test_fs_tool.txt"
        content = "hello world"
        
        # Write
        res = fs.write_file(test_file, content)
        self.assertIn("Successfully", res)
        
        # Read
        read_res = fs.read_file(test_file)
        self.assertEqual(read_res, content)
        
        # Grep (search directly in the file path to be efficient)
        grep_res = fs.grep_search("hello", test_file, "*")
        self.assertIn("hello world", grep_res)
        
        # Cleanup
        os.remove(test_file)

    def test_code_tools(self):
        """Test code manipulation tools"""
        test_file = "test_code.py"
        code_content = "def hello():\n    print('hi')"
        fs.write_file(test_file, code_content)
        
        # Replace
        code.replace_text(test_file, "'hi'", "'hello'")
        new_content = fs.read_file(test_file)
        self.assertIn("'hello'", new_content)
        
        # Analyze
        analysis = code.code_analyze_file(test_file)
        self.assertIn("Functions: 1", analysis)
        
        # Cleanup
        os.remove(test_file)

    def test_memory_tools(self):
        """Test project memory tools"""
        memory.clear_memory()
        fact = "Unit test is running"
        memory.remember_fact(fact)
        
        recall = memory.recall_facts()
        self.assertIn(fact, recall)
        
        memory.clear_memory()

if __name__ == "__main__":
    unittest.main()
