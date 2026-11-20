"""Round-trip and invalid-input rejection tests for multibase encodings."""

import os

import pytest

from multibase import ENCODINGS, DecodingError, decode, encode

INVALID_SUFFIXES = [
    ("\u00a0", "low-unicode"),
    ("\U0001f4a8", "emoji"),
    ("!", "punctuation"),
    ("\u00ff", "high-latin1"),
]


@pytest.mark.parametrize("encoding_info", ENCODINGS, ids=lambda e: e.encoding)
@pytest.mark.parametrize(
    "suffix,label",
    INVALID_SUFFIXES,
    ids=[label for _, label in INVALID_SUFFIXES],
)
def test_invalid_input_rejected(encoding_info, suffix, label):
    """Decoding invalid alphabet characters should raise DecodingError."""
    if encoding_info.encoding == "identity":
        pytest.skip("identity accepts all bytes")
    if encoding_info.encoding == "base256emoji":
        pytest.skip("base256emoji has its own alphabet; emoji suffixes are not reliably invalid")

    prefix = encoding_info.code.decode("utf-8")
    invalid_data = prefix + suffix

    with pytest.raises(DecodingError):
        decode(invalid_data)


@pytest.mark.parametrize("encoding_info", ENCODINGS, ids=lambda e: e.encoding)
def test_random_data(encoding_info):
    """Round-trip random data of various sizes."""
    for size in [1, 2, 7, 16, 32, 64, 137, 256, 1024]:
        data = os.urandom(size)
        encoded = encode(encoding_info.encoding, data)
        decoded = decode(encoded)
        assert decoded == data, f"Failed for {encoding_info.encoding} size={size}"


@pytest.mark.parametrize("encoding_info", ENCODINGS, ids=lambda e: e.encoding)
def test_leading_zeros(encoding_info):
    """Round-trip data with leading zero bytes."""
    for num_zeros in [1, 2, 4, 8, 16]:
        data = b"\x00" * num_zeros + b"hello"
        encoded = encode(encoding_info.encoding, data)
        decoded = decode(encoded)
        assert decoded == data, f"Leading zeros lost for {encoding_info.encoding} zeros={num_zeros}"


@pytest.mark.parametrize("encoding_info", ENCODINGS, ids=lambda e: e.encoding)
def test_all_zeros(encoding_info):
    """Round-trip all-zero data."""
    for size in [1, 4, 16, 32]:
        data = b"\x00" * size
        encoded = encode(encoding_info.encoding, data)
        decoded = decode(encoded)
        assert decoded == data


@pytest.mark.parametrize("encoding_info", ENCODINGS, ids=lambda e: e.encoding)
def test_all_ones(encoding_info):
    """Round-trip all-0xFF data."""
    for size in [1, 4, 16, 32]:
        data = b"\xff" * size
        encoded = encode(encoding_info.encoding, data)
        decoded = decode(encoded)
        assert decoded == data
