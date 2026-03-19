#!/usr/bin/env python3
"""Test cross-platform compatibility for nutstore_sync"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 50)
print("Cross-Platform Compatibility Test")
print("=" * 50)

# Test 1: Python version
print(f"\n1. Python Version: {sys.version}")
print(f"   Major: {sys.version_info.major}")
print(f"   Minor: {sys.version_info.minor}")
print(f"   Micro: {sys.version_info.micro}")

if sys.version_info >= (3, 8):
    print("   ✅ Python 3.8+ supported")
else:
    print("   ❌ Python 3.8+ required")

# Test 2: Platform
print(f"\n2. Platform: {sys.platform}")
if sys.platform == 'win32':
    print("   Running on Windows")
elif sys.platform == 'darwin':
    print("   Running on macOS")
elif sys.platform == 'linux':
    print("   Running on Linux")
else:
    print(f"   Running on: {sys.platform}")

# Test 3: Standard library imports
print("\n3. Testing standard library imports...")
try:
    import urllib.request
    import urllib.error
    import base64
    import json
    import ssl
    import re
    from pathlib import Path
    from typing import Optional, Tuple, List
    print("   ✅ All required modules available")
except ImportError as e:
    print(f"   ❌ Import error: {e}")

# Test 4: Path handling
print("\n4. Testing path handling...")
from pathlib import Path
test_paths = [
    Path("/unix/path/to/file"),
    Path("C:\\Windows\\path\\to\\file"),
    Path("relative/path/to/file"),
    Path.home() / ".config" / "test",
]

for p in test_paths:
    try:
        str_path = str(p)
        print(f"   ✅ Path: {str_path}")
    except Exception as e:
        print(f"   ❌ Path error: {e}")

# Test 5: SSL context
print("\n5. Testing SSL context...")
try:
    import ssl
    context = ssl._create_unverified_context()
    print("   ✅ SSL unverified context created")
except Exception as e:
    print(f"   ❌ SSL error: {e}")

# Test 6: Base64 encoding
print("\n6. Testing Base64 encoding...")
try:
    import base64
    test_auth = base64.b64encode(b"user:password").decode()
    print(f"   ✅ Base64 encoding works: {test_auth}")
except Exception as e:
    print(f"   ❌ Base64 error: {e}")

# Test 7: JSON handling
print("\n7. Testing JSON handling...")
try:
    import json
    test_config = {
        "username": "test@example.com",
        "app_password": "test_pass",
        "webdav_url": "https://dav.jianguoyun.com/dav/"
    }
    json_str = json.dumps(test_config)
    parsed = json.loads(json_str)
    assert parsed["username"] == test_config["username"]
    print("   ✅ JSON serialization works")
except Exception as e:
    print(f"   ❌ JSON error: {e}")

# Test 8: Regular expressions
print("\n8. Testing Regular expressions...")
try:
    import re
    test_xml = "<d:href>/dav/test.txt</d:href>"
    matches = re.findall(r'<d:href>([^<]+)</d:href>', test_xml)
    assert len(matches) == 1
    assert matches[0] == "/dav/test.txt"
    print("   ✅ Regex parsing works")
except Exception as e:
    print(f"   ❌ Regex error: {e}")

# Test 9: Type hints
print("\n9. Testing type hints...")
try:
    from typing import Optional, Tuple, List
    def test_func(path: str) -> Optional[Tuple[str, int]]:
        return ("test", 42)
    result = test_func("test")
    assert result is not None
    print("   ✅ Type hints work (runtime)")
except Exception as e:
    print(f"   ❌ Type hint error: {e}")

# Test 10: File operations
print("\n10. Testing file operations...")
try:
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    with open(temp_path, 'r') as f:
        content = f.read()
    assert content == "test content"
    os.unlink(temp_path)
    print("   ✅ File operations work")
except Exception as e:
    print(f"   ❌ File error: {e}")

print("\n" + "=" * 50)
print("Cross-Platform Tests Complete")
print("=" * 50)
