"""Tests for nutstore_sync module."""

import unittest
import json
import tempfile
import os
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from nutstore_sync import NutstoreSync, ConfigError, APIError


class TestConfig(unittest.TestCase):
    """Test configuration loading."""

    def test_missing_config_raises_error(self):
        """Test that missing config raises ConfigError."""
        with self.assertRaises(ConfigError):
            NutstoreSync("/nonexistent/config.json")

    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises ConfigError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json")
            temp_path = f.name
        
        try:
            with self.assertRaises(ConfigError):
                NutstoreSync(temp_path)
        finally:
            os.unlink(temp_path)

    def test_missing_required_fields_raises_error(self):
        """Test that missing required fields raises ConfigError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"username": "test"}, f)
            temp_path = f.name
        
        try:
            with self.assertRaises(ConfigError):
                NutstoreSync(temp_path)
        finally:
            os.unlink(temp_path)

    def test_valid_config_loads(self):
        """Test that valid config loads successfully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "username": "test@example.com",
                "app_password": "test_password"
            }, f)
            temp_path = f.name
        
        try:
            client = NutstoreSync(temp_path)
            self.assertEqual(client.config['username'], "test@example.com")
        finally:
            os.unlink(temp_path)


class TestURLBuilding(unittest.TestCase):
    """Test URL building logic."""

    def setUp(self):
        """Set up test client."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "username": "test@example.com",
                "app_password": "test_password"
            }, f)
            self.config_path = f.name
        
        self.client = NutstoreSync(self.config_path)

    def tearDown(self):
        """Clean up."""
        os.unlink(self.config_path)

    def test_base_url_normalization(self):
        """Test that base URL is properly normalized."""
        self.assertTrue(self.client.base_url.endswith('/'))
        self.assertIn('dav.jianguoyun.com', self.client.base_url)


class TestExceptions(unittest.TestCase):
    """Test exception classes."""

    def test_api_error_with_status(self):
        """Test APIError with status code."""
        error = APIError("Test error", 404)
        self.assertEqual(error.status_code, 404)
        self.assertEqual(str(error), "Test error")

    def test_api_error_without_status(self):
        """Test APIError without status code."""
        error = APIError("Test error")
        self.assertEqual(error.status_code, 0)


if __name__ == '__main__':
    unittest.main()
