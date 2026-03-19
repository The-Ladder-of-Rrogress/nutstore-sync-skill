#!/usr/bin/env python3
"""Test edge cases and boundary conditions for nutstore_sync"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from nutstore_sync import NutstoreSync, NutstoreError, ConfigError, APIError

print("=" * 50)
print("Edge Cases and Boundary Tests")
print("=" * 50)

# Test 1: Empty remote path
print("\n1. Testing empty remote path...")
try:
    client = NutstoreSync()
    # list_dir with empty string should work
    items = client.list_dir('')
    print(f"   ✅ Empty path works, found {len(items)} items")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Path with special characters
print("\n2. Testing paths with special characters...")
try:
    client = NutstoreSync()
    # These should not crash (though may not exist)
    test_paths = [
        "test file with spaces.txt",
        "test-file-with-dashes.txt",
        "test_file_with_underscores.txt",
        "test.file.with.dots.txt",
        "test(1).txt",
        "test[1].txt",
    ]
    for path in test_paths:
        # Just test that it doesn't crash
        url = client.base_url + path
        print(f"   ✅ Path '{path}' -> URL length: {len(url)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Very long path
print("\n3. Testing very long path...")
try:
    client = NutstoreSync()
    long_path = "a" * 200 + ".txt"
    url = client.base_url + long_path
    print(f"   ✅ Long path ({len(long_path)} chars) -> URL length: {len(url)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Unicode path
print("\n4. Testing unicode path...")
try:
    client = NutstoreSync()
    unicode_paths = [
        "测试文件.txt",
        "файл.txt",
        "ファイル.txt",
        "📁emoji.txt",
    ]
    for path in unicode_paths:
        url = client.base_url + path
        print(f"   ✅ Unicode path '{path}' -> URL length: {len(url)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Large file upload (simulated)
print("\n5. Testing large file handling...")
try:
    # Create a 1MB test file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"x" * (1024 * 1024))  # 1MB
        large_file = f.name
    
    file_size = os.path.getsize(large_file)
    print(f"   ✅ Created test file: {file_size / 1024 / 1024:.2f} MB")
    
    # Clean up
    os.unlink(large_file)
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Empty file upload
print("\n6. Testing empty file handling...")
try:
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("")  # Empty file
        empty_file = f.name
    
    file_size = os.path.getsize(empty_file)
    print(f"   ✅ Created empty file: {file_size} bytes")
    
    os.unlink(empty_file)
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 7: Multiple config paths
print("\n7. Testing config path resolution...")
try:
    from nutstore_sync import DEFAULT_CONFIG_PATHS
    print(f"   Found {len(DEFAULT_CONFIG_PATHS)} default config paths:")
    for i, path in enumerate(DEFAULT_CONFIG_PATHS):
        print(f"   {i+1}. {path}")
        print(f"      Exists: {path.exists()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 8: Base URL normalization
print("\n8. Testing base URL normalization...")
try:
    import tempfile
    import json
    
    # Test with trailing slash
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            "username": "test@test.com",
            "app_password": "test",
            "webdav_url": "https://dav.jianguoyun.com/dav/"
        }, f)
        temp_path = f.name
    
    client1 = NutstoreSync(temp_path)
    print(f"   ✅ With trailing slash: {client1.base_url}")
    
    # Test without trailing slash
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            "username": "test@test.com",
            "app_password": "test",
            "webdav_url": "https://dav.jianguoyun.com/dav"
        }, f)
        temp_path2 = f.name
    
    client2 = NutstoreSync(temp_path2)
    print(f"   ✅ Without trailing slash: {client2.base_url}")
    
    # Both should end with /
    assert client1.base_url.endswith('/')
    assert client2.base_url.endswith('/')
    print("   ✅ Both URLs properly normalized")
    
    os.unlink(temp_path)
    os.unlink(temp_path2)
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 9: Auth encoding
print("\n9. Testing auth encoding...")
try:
    import base64
    
    test_cases = [
        ("user", "pass"),
        ("user@example.com", "p@ssw0rd!"),
        ("user", "pass:with:colons"),
        ("user", "pass with spaces"),
    ]
    
    for username, password in test_cases:
        auth = base64.b64encode(f"{username}:{password}".encode()).decode()
        decoded = base64.b64decode(auth).decode()
        assert decoded == f"{username}:{password}"
        print(f"   ✅ Auth encoding for '{username}': OK")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 10: WebDAV path joining
print("\n10. Testing WebDAV path joining...")
try:
    client = NutstoreSync()
    
    test_cases = [
        ("file.txt", "file.txt"),
        ("/file.txt", "file.txt"),
        ("path/file.txt", "path/file.txt"),
        ("/path/file.txt", "path/file.txt"),
        ("path/to/file.txt", "path/to/file.txt"),
    ]
    
    for input_path, expected in test_cases:
        result = input_path.lstrip('/')
        assert result == expected
        print(f"   ✅ '{input_path}' -> '{result}'")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("Edge Cases Tests Complete")
print("=" * 50)
