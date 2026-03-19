#!/usr/bin/env python3
"""Test performance characteristics of nutstore_sync"""

import sys
import time
import tempfile
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from nutstore_sync import NutstoreSync

print("=" * 50)
print("Performance Tests")
print("=" * 50)

# Test 1: Client initialization time
print("\n1. Testing client initialization time...")
try:
    start = time.time()
    client = NutstoreSync()
    elapsed = time.time() - start
    print(f"   ✅ Client initialized in {elapsed:.4f} seconds")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Connection test time
print("\n2. Testing connection test time...")
try:
    client = NutstoreSync()
    start = time.time()
    result = client.test()
    elapsed = time.time() - start
    print(f"   ✅ Connection test: {result}, took {elapsed:.4f} seconds")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: List directory time
print("\n3. Testing list directory time...")
try:
    client = NutstoreSync()
    start = time.time()
    items = client.list_dir('')
    elapsed = time.time() - start
    print(f"   ✅ Listed {len(items)} items in {elapsed:.4f} seconds")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Small file upload time
print("\n4. Testing small file upload time...")
try:
    client = NutstoreSync()
    
    # Create small test file (1KB)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("x" * 1024)
        small_file = f.name
    
    start = time.time()
    client.upload(small_file, 'skills/perf_test_small.txt')
    elapsed = time.time() - start
    print(f"   ✅ Uploaded 1KB file in {elapsed:.4f} seconds")
    
    # Clean up
    client.delete('skills/perf_test_small.txt')
    os.unlink(small_file)
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Medium file upload time
print("\n5. Testing medium file upload time...")
try:
    client = NutstoreSync()
    
    # Create medium test file (100KB)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("x" * (100 * 1024))
        medium_file = f.name
    
    start = time.time()
    client.upload(medium_file, 'skills/perf_test_medium.txt')
    elapsed = time.time() - start
    file_size = os.path.getsize(medium_file)
    speed = file_size / elapsed / 1024  # KB/s
    print(f"   ✅ Uploaded 100KB file in {elapsed:.4f} seconds ({speed:.2f} KB/s)")
    
    # Clean up
    client.delete('skills/perf_test_medium.txt')
    os.unlink(medium_file)
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Multiple operations
print("\n6. Testing multiple operations batch...")
try:
    client = NutstoreSync()
    
    # Create test file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        test_file = f.name
    
    start = time.time()
    
    # Upload
    client.upload(test_file, 'skills/perf_test_batch.txt')
    
    # Check exists
    exists = client.exists('skills/perf_test_batch.txt')
    
    # Download
    client.download('skills/perf_test_batch.txt', test_file + '.down')
    
    # Delete
    client.delete('skills/perf_test_batch.txt')
    
    elapsed = time.time() - start
    print(f"   ✅ 4 operations (upload, exists, download, delete) in {elapsed:.4f} seconds")
    
    # Clean up
    os.unlink(test_file)
    os.unlink(test_file + '.down')
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 7: Memory efficiency
print("\n7. Testing memory efficiency...")
try:
    import tracemalloc
    
    tracemalloc.start()
    
    # Create client and perform operations
    client = NutstoreSync()
    client.test()
    items = client.list_dir('')
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"   ✅ Current memory: {current / 1024:.2f} KB")
    print(f"   ✅ Peak memory: {peak / 1024:.2f} KB")
except ImportError:
    print("   ⚠️ tracemalloc not available, skipping memory test")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 8: Import time
print("\n8. Testing module import time...")
try:
    start = time.time()
    import nutstore_sync
    elapsed = time.time() - start
    print(f"   ✅ Module imported in {elapsed:.4f} seconds")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("Performance Tests Complete")
print("=" * 50)
