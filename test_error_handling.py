#!/usr/bin/env python3
"""Test error handling for nutstore_sync"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from nutstore_sync import NutstoreSync, NutstoreError, ConfigError, APIError

print("=" * 50)
print("Testing Error Handling")
print("=" * 50)

# Test 1: ConfigError for missing file
print("\n1. Testing ConfigError for missing config file...")
try:
    client = NutstoreSync('/nonexistent/config.json')
    print("   ❌ Should have raised ConfigError")
except ConfigError as e:
    print(f"   ✅ ConfigError caught: {e}")
except Exception as e:
    print(f"   ❌ Wrong exception type: {type(e).__name__}: {e}")

# Test 2: ConfigError for invalid JSON
print("\n2. Testing ConfigError for invalid JSON...")
import tempfile
import os

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    f.write("invalid json content")
    temp_path = f.name

try:
    client = NutstoreSync(temp_path)
    print("   ❌ Should have raised ConfigError")
except ConfigError as e:
    print(f"   ✅ ConfigError caught: {e}")
except Exception as e:
    print(f"   ❌ Wrong exception type: {type(e).__name__}: {e}")
finally:
    os.unlink(temp_path)

# Test 3: ConfigError for missing required fields
print("\n3. Testing ConfigError for missing required fields...")
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    import json
    json.dump({"username": "test"}, f)  # Missing app_password
    temp_path = f.name

try:
    client = NutstoreSync(temp_path)
    print("   ❌ Should have raised ConfigError")
except ConfigError as e:
    print(f"   ✅ ConfigError caught: {e}")
except Exception as e:
    print(f"   ❌ Wrong exception type: {type(e).__name__}: {e}")
finally:
    os.unlink(temp_path)

# Test 4: APIError with status code
print("\n4. Testing APIError with status code...")
try:
    error = APIError("Test error", 404)
    assert error.status_code == 404
    print(f"   ✅ APIError created with status_code: {error.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: APIError without status code
print("\n5. Testing APIError without status code...")
try:
    error = APIError("Test error")
    assert error.status_code == 0
    print(f"   ✅ APIError created with default status_code: {error.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Exception hierarchy
print("\n6. Testing exception hierarchy...")
try:
    raise ConfigError("test")
except NutstoreError:
    print("   ✅ ConfigError is subclass of NutstoreError")
except Exception as e:
    print(f"   ❌ Error: {e}")

try:
    raise APIError("test")
except NutstoreError:
    print("   ✅ APIError is subclass of NutstoreError")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("Error Handling Tests Complete")
print("=" * 50)
