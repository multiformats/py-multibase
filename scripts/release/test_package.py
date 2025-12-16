#!/usr/bin/env python
"""Test that the built package can be installed and works correctly."""

import subprocess
import sys
from pathlib import Path

# Find the dist directory
dist_dir = Path(__file__).parent.parent.parent / "dist"
if not dist_dir.exists():
    print(f"Error: dist directory not found at {dist_dir}")
    sys.exit(1)

# Find wheel or source distribution files
dist_files = list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))
if not dist_files:
    print(f"Error: No distribution files found in {dist_dir}")
    sys.exit(1)

# Install the package
dist_file = dist_files[0]
print(f"Installing {dist_file.name}...")
result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "--force-reinstall", str(dist_file)],
    capture_output=True,
    text=True,
)
if result.returncode != 0:
    print(f"Error installing package: {result.stderr}")
    sys.exit(1)

# Test that the package can be imported and basic functionality works
print("Testing package import and basic functionality...")
try:
    import multibase

    # Test that version is accessible
    assert hasattr(multibase, "__version__"), "Package should have __version__"
    assert multibase.__version__, "Version should not be empty"
    print(f"✓ Version accessible: {multibase.__version__}")

    # Test that main functions are available
    assert callable(multibase.encode), "encode should be callable"
    assert callable(multibase.decode), "decode should be callable"
    assert callable(multibase.is_encoded), "is_encoded should be callable"
    assert callable(multibase.list_encodings), "list_encodings should be callable"
    assert callable(multibase.is_encoding_supported), "is_encoding_supported should be callable"
    assert callable(multibase.get_encoding_info), "get_encoding_info should be callable"
    print("✓ Main functions are callable")

    # Test that exceptions are importable
    assert hasattr(multibase, "UnsupportedEncodingError"), "UnsupportedEncodingError should be available"
    assert hasattr(multibase, "InvalidMultibaseStringError"), "InvalidMultibaseStringError should be available"
    assert hasattr(multibase, "DecodingError"), "DecodingError should be available"
    print("✓ Exceptions are importable")

    # Test that classes are importable
    assert hasattr(multibase, "Encoder"), "Encoder class should be available"
    assert hasattr(multibase, "Decoder"), "Decoder class should be available"
    print("✓ Classes are importable")

    # Test basic encode/decode with multiple encodings
    test_data = "hello world"

    # Test base64
    encoded = multibase.encode("base64", test_data)
    assert encoded.startswith(b"m"), "Base64 encoding should start with 'm'"
    decoded = multibase.decode(encoded)
    assert decoded == b"hello world", "Base64 decoded data should match original"

    # Test base16
    encoded = multibase.encode("base16", test_data)
    assert encoded.startswith(b"f"), "Base16 encoding should start with 'f'"
    decoded = multibase.decode(encoded)
    assert decoded == b"hello world", "Base16 decoded data should match original"

    # Test base32
    encoded = multibase.encode("base32", test_data)
    assert encoded.startswith(b"b"), "Base32 encoding should start with 'b'"
    decoded = multibase.decode(encoded)
    assert decoded == b"hello world", "Base32 decoded data should match original"
    print("✓ Multiple encoding types work (base64, base16, base32)")

    # Test is_encoded
    assert multibase.is_encoded(encoded), "is_encoded should return True for valid multibase string"
    assert not multibase.is_encoded("invalid"), "is_encoded should return False for invalid string"
    print("✓ is_encoded function works")

    # Test is_encoding_supported
    assert multibase.is_encoding_supported("base64"), "base64 should be supported"
    assert multibase.is_encoding_supported("base16"), "base16 should be supported"
    assert not multibase.is_encoding_supported("base999"), "base999 should not be supported"
    print("✓ is_encoding_supported function works")

    # Test list_encodings
    encodings = multibase.list_encodings()
    assert isinstance(encodings, list), "list_encodings should return a list"
    assert "base64" in encodings, "base64 should be in encodings list"
    assert "base16" in encodings, "base16 should be in encodings list"
    assert "base32" in encodings, "base32 should be in encodings list"
    assert len(encodings) >= 20, "Should have at least 20 encodings"
    print(f"✓ list_encodings works (found {len(encodings)} encodings)")

    # Test get_encoding_info
    info = multibase.get_encoding_info("base64")
    assert info.encoding == "base64", "get_encoding_info should return correct encoding name"
    assert info.code == b"m", "base64 code should be 'm'"
    assert info.converter is not None, "converter should not be None"
    print("✓ get_encoding_info function works")

    # Test decode with return_encoding
    test_encoded = multibase.encode("base16", "test")
    encoding, decoded = multibase.decode(test_encoded, return_encoding=True)
    assert encoding == "base16", "return_encoding should return correct encoding"
    assert decoded == b"test", "decoded data should match"
    print("✓ decode with return_encoding works")

    # Test Encoder class
    encoder = multibase.Encoder("base64")
    assert encoder.encoding == "base64", "Encoder should have correct encoding"
    encoded = encoder.encode("test")
    assert encoded.startswith(b"m"), "Encoder.encode should work"
    print("✓ Encoder class works")

    # Test Decoder class
    decoder = multibase.Decoder()
    test_encoded = multibase.encode("base64", "test")
    decoded = decoder.decode(test_encoded)
    assert decoded == b"test", "Decoder.decode should work"
    encoding, decoded = decoder.decode(test_encoded, return_encoding=True)
    assert encoding == "base64", "Decoder.decode with return_encoding should work"
    print("✓ Decoder class works")

    # Test error handling
    try:
        multibase.encode("base999", "test")
        assert False, "Should raise UnsupportedEncodingError"
    except multibase.UnsupportedEncodingError:
        pass
    print("✓ Error handling works (UnsupportedEncodingError)")

    try:
        multibase.decode("invalid")
        assert False, "Should raise InvalidMultibaseStringError"
    except multibase.InvalidMultibaseStringError:
        pass
    print("✓ Error handling works (InvalidMultibaseStringError)")

    print(f"\n✓ Package installed successfully (version {multibase.__version__})")
    print("✓ All functionality tests passed")
    print("Package is ready for release!")

except ImportError as e:
    print(f"Error importing package: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
except AssertionError as e:
    print(f"Test failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
