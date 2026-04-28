"""Tests for nutstore_sync module."""

import unittest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from nutstore_sync import NutstoreSync, ConfigError, APIError, DEFAULT_MAX_FILE_SIZE


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


class TestPathTraversal(unittest.TestCase):
    """Test path traversal protection."""

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

    def test_path_traversal_blocked(self):
        """Test that '..' in path is blocked."""
        with self.assertRaises(APIError) as ctx:
            self.client._request('GET', '../etc/passwd')
        self.assertIn("traversal", str(ctx.exception))


class TestURLScheme(unittest.TestCase):
    """Test URL scheme validation."""

    def setUp(self):
        """Set up test client."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "username": "test@example.com",
                "app_password": "test_password",
                "webdav_url": "file:///etc/"
            }, f)
            self.config_path = f.name
        self.client = NutstoreSync(self.config_path)

    def tearDown(self):
        """Clean up."""
        os.unlink(self.config_path)

    def test_non_http_scheme_blocked(self):
        """Test that non-HTTP schemes are blocked."""
        with self.assertRaises(APIError) as ctx:
            self.client._request('GET', 'test.txt')
        self.assertIn("scheme", str(ctx.exception))


class TestUploadDownload(unittest.TestCase):
    """Test upload and download with mocked requests."""

    def setUp(self):
        """Set up test client."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "username": "test@example.com",
                "app_password": "test_password"
            }, f)
            self.config_path = f.name

        with patch('nutstore_sync.NutstoreSync._request') as mock_request:
            mock_request.return_value = (201, None)
            self.client = NutstoreSync(self.config_path)
            self.client._request = mock_request

    def tearDown(self):
        """Clean up."""
        os.unlink(self.config_path)

    def test_upload_success(self):
        """Test successful upload."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("test content")
            temp_path = f.name

        try:
            result = self.client.upload(temp_path, 'remote.txt')
            self.assertTrue(result)
            self.client._request.assert_called_once()
            call_args = self.client._request.call_args
            self.assertEqual(call_args[0][0], 'PUT')
            self.assertEqual(call_args[0][1], 'remote.txt')
        finally:
            os.unlink(temp_path)

    def test_upload_file_not_found(self):
        """Test upload with missing file."""
        with self.assertRaises(FileNotFoundError):
            self.client.upload('/nonexistent/file.txt')

    def test_upload_too_large(self):
        """Test upload rejects large files."""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"x" * (DEFAULT_MAX_FILE_SIZE + 1))
            temp_path = f.name

        try:
            with self.assertRaises(APIError) as ctx:
                self.client.upload(temp_path)
            self.assertIn("too large", str(ctx.exception).lower())
        finally:
            os.unlink(temp_path)

    def test_upload_progress_callback(self):
        """Test upload calls progress callback."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("x" * 100)
            temp_path = f.name

        progress_calls = []

        def track_progress(uploaded, total):
            progress_calls.append((uploaded, total))

        try:
            self.client.upload(temp_path, 'test.txt', progress_callback=track_progress)
            self.assertTrue(len(progress_calls) > 0)
            self.assertEqual(progress_calls[-1][0], 100)
        finally:
            os.unlink(temp_path)

    def test_download_success(self):
        """Test successful download."""
        self.client._request.return_value = (200, b"downloaded content")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_path = f.name

        try:
            result = self.client.download('remote.txt', temp_path)
            self.assertTrue(result)
            with open(temp_path, 'rb') as f:
                self.assertEqual(f.read(), b"downloaded content")
        finally:
            os.unlink(temp_path)

    def test_download_failure(self):
        """Test download with error status."""
        self.client._request.return_value = (404, None)

        with self.assertRaises(APIError) as ctx:
            self.client.download('nonexistent.txt')
        self.assertEqual(ctx.exception.status_code, 404)


class TestListDir(unittest.TestCase):
    """Test list_dir with mocked XML response."""

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

    def test_list_dir_parses_xml(self):
        """Test that list_dir correctly parses WebDAV XML."""
        # Simulated WebDAV XML response
        xml_response = b'''<?xml version="1.0" encoding="utf-8"?>
        <d:multistatus xmlns:d="DAV:">
            <d:response>
                <d:href>/dav/</d:href>
            </d:response>
            <d:response>
                <d:href>/dav/folder1/</d:href>
            </d:response>
            <d:response>
                <d:href>/dav/file.txt</d:href>
            </d:response>
        </d:multistatus>'''

        with patch.object(self.client, '_request', return_value=(207, xml_response)):
            items = self.client.list_dir('')

        # Should find folder1 and file.txt (skip root)
        names = [name for _, name in items]
        self.assertIn('folder1', names)
        self.assertIn('file.txt', names)

    def test_list_dir_failure(self):
        """Test list_dir with error status."""
        with patch.object(self.client, '_request', return_value=(404, None)):
            with self.assertRaises(APIError):
                self.client.list_dir('')


class TestDeleteExists(unittest.TestCase):
    """Test delete and exists methods."""

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

    def test_delete_success(self):
        """Test successful delete."""
        with patch.object(self.client, '_request', return_value=(204, None)):
            result = self.client.delete('test.txt')
            self.assertTrue(result)

    def test_delete_failure(self):
        """Test delete with error status."""
        with patch.object(self.client, '_request', return_value=(404, None)):
            with self.assertRaises(APIError):
                self.client.delete('nonexistent.txt')

    def test_exists_true(self):
        """Test exists returns True for existing file."""
        with patch.object(self.client, '_request', return_value=(200, None)):
            self.assertTrue(self.client.exists('test.txt'))

    def test_exists_false(self):
        """Test exists returns False for missing file."""
        with patch.object(self.client, '_request', return_value=(404, None)):
            self.assertFalse(self.client.exists('nonexistent.txt'))


class TestTest(unittest.TestCase):
    """Test the test() method."""

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

    def test_connection_success(self):
        """Test successful connection."""
        with patch.object(self.client, '_request', return_value=(207, None)):
            self.assertTrue(self.client.test())

    def test_connection_failure(self):
        """Test failed connection."""
        with patch.object(self.client, '_request', return_value=(401, None)):
            self.assertFalse(self.client.test())


if __name__ == '__main__':
    unittest.main()
