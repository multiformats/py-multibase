"""Round-trip and invalid-input rejection tests for multibase encodings."""

import pytest

from multibase import ENCODINGS, DecodingError, decode

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
