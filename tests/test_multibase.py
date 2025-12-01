#!/usr/bin/env python

"""Tests for `multibase` package."""

import pytest
from morphys import ensure_bytes

from multibase import (
    Decoder,
    DecodingError,
    Encoder,
    InvalidMultibaseStringError,
    UnsupportedEncodingError,
    decode,
    encode,
    get_encoding_info,
    is_encoded,
    is_encoding_supported,
    list_encodings,
)

TEST_FIXTURES = (
    ("identity", "yes mani !", "\x00yes mani !"),
    ("base2", "yes mani !", "01111001011001010111001100100000011011010110000101101110011010010010000000100001"),
    ("base8", "yes mani !", "7171312714403326055632220041"),
    ("base10", "yes mani !", "9573277761329450583662625"),
    ("base16", "yes mani !", "f796573206d616e692021"),
    ("base16", "\x01", "f01"),
    ("base16", "\x0f", "f0f"),
    ("base16", "f", "f66"),
    ("base16", "fo", "f666f"),
    ("base16", "foo", "f666f6f"),
    ("base16", "foob", "f666f6f62"),
    ("base16", "fooba", "f666f6f6261"),
    ("base16", "foobar", "f666f6f626172"),
    ("base16upper", "yes mani !", "F796573206D616E692021"),
    ("base16upper", "f", "F66"),
    ("base16upper", "fo", "F666F"),
    ("base16upper", "foo", "F666F6F"),
    ("base32", "yes mani !", "bpfsxgidnmfxgsibb"),
    ("base32", "f", "bmy"),
    ("base32", "fo", "bmzxq"),
    ("base32", "foo", "bmzxw6"),
    ("base32", "foob", "bmzxw6yq"),
    ("base32", "fooba", "bmzxw6ytb"),
    ("base32", "foobar", "bmzxw6ytboi"),
    ("base32upper", "yes mani !", "BPFSXGIDNMFXGSIBB"),
    ("base32upper", "f", "BMY"),
    ("base32upper", "fo", "BMZXQ"),
    ("base32upper", "foo", "BMZXW6"),
    ("base32pad", "yes mani !", "cpfsxgidnmfxgsibb"),
    ("base32pad", "f", "cmy======"),
    ("base32pad", "fo", "cmzxq===="),
    ("base32pad", "foo", "cmzxw6==="),
    ("base32pad", "foob", "cmzxw6yq="),
    ("base32pad", "fooba", "cmzxw6ytb"),
    ("base32pad", "foobar", "cmzxw6ytboi======"),
    ("base32padupper", "yes mani !", "CPFSXGIDNMFXGSIBB"),
    ("base32padupper", "f", "CMY======"),
    ("base32padupper", "fo", "CMZXQ===="),
    ("base32padupper", "foo", "CMZXW6==="),
    ("base32hex", "yes mani !", "vf5in683dc5n6i811"),
    ("base32hex", "f", "vco"),
    ("base32hex", "fo", "vcpng"),
    ("base32hex", "foo", "vcpnmu"),
    ("base32hex", "foob", "vcpnmuog"),
    ("base32hex", "fooba", "vcpnmuoj1"),
    ("base32hex", "foobar", "vcpnmuoj1e8"),
    ("base32hexupper", "yes mani !", "VF5IN683DC5N6I811"),
    ("base32hexupper", "f", "VCO"),
    ("base32hexupper", "fo", "VCPNG"),
    ("base32hexpad", "yes mani !", "tf5in683dc5n6i811"),
    ("base32hexpad", "f", "tco======"),
    ("base32hexpad", "fo", "tcpng===="),
    ("base32hexpad", "foo", "tcpnmu==="),
    ("base32hexpad", "foob", "tcpnmuog="),
    ("base32hexpad", "fooba", "tcpnmuoj1"),
    ("base32hexpad", "foobar", "tcpnmuoj1e8======"),
    ("base32hexpadupper", "yes mani !", "TF5IN683DC5N6I811"),
    ("base32hexpadupper", "f", "TCO======"),
    ("base32hexpadupper", "fo", "TCPNG===="),
    ("base32z", "yes mani !", "hxf1zgedpcfzg1ebb"),
    ("base36", "Decentralize everything!!!", "km552ng4dabi4neu1oo8l4i5mndwmpc3mkukwtxy9"),
    ("base36upper", "Decentralize everything!!!", "KM552NG4DABI4NEU1OO8L4I5MNDWMPC3MKUKWTXY9"),
    ("base58flickr", "yes mani !", "Z7Pznk19XTTzBtx"),
    ("base58btc", "yes mani !", "z7paNL19xttacUY"),
    ("base64", "÷ïÿ", "mw7fDr8O/"),
    ("base64", "f", "mZg"),
    ("base64", "fo", "mZm8"),
    ("base64", "foo", "mZm9v"),
    ("base64", "foob", "mZm9vYg"),
    ("base64", "fooba", "mZm9vYmE"),
    ("base64", "foobar", "mZm9vYmFy"),
    ("base64pad", "f", "MZg=="),
    ("base64pad", "fo", "MZm8="),
    ("base64pad", "foo", "MZm9v"),
    ("base64pad", "foob", "MZm9vYg=="),
    ("base64pad", "fooba", "MZm9vYmE="),
    ("base64pad", "foobar", "MZm9vYmFy"),
    ("base64url", "÷ïÿ", "uw7fDr8O_"),
    ("base64urlpad", "f", "UZg=="),
    ("base64urlpad", "fo", "UZm8="),
    ("base64urlpad", "foo", "UZm9v"),
    ("base64urlpad", "foob", "UZm9vYg=="),
    ("base64urlpad", "fooba", "UZm9vYmE="),
    ("base64urlpad", "foobar", "UZm9vYmFy"),
)


INCORRECT_ENCODINGS = ("base58", "base4")
INCORRECT_ENCODED_DATA = ("abcdefghi", "!qweqweqeqw")


@pytest.mark.parametrize("encoding,data,encoded_data", TEST_FIXTURES)
def test_encode(encoding, data, encoded_data):
    assert encode(encoding, data) == ensure_bytes(encoded_data)


@pytest.mark.parametrize("encoding", INCORRECT_ENCODINGS)
def test_encode_incorrect_encoding(encoding):
    with pytest.raises(UnsupportedEncodingError) as excinfo:
        encode(encoding, "test data")
    assert "not supported" in str(excinfo.value)


@pytest.mark.parametrize("_,data,encoded_data", TEST_FIXTURES)
def test_decode(_, data, encoded_data):
    assert decode(encoded_data) == ensure_bytes(data)


@pytest.mark.parametrize("encoded_data", INCORRECT_ENCODED_DATA)
def test_decode_incorrect_encoding(encoded_data):
    with pytest.raises(InvalidMultibaseStringError) as excinfo:
        decode(encoded_data)
    assert "Can not determine encoding" in str(excinfo.value)


@pytest.mark.parametrize("_,data,encoded_data", TEST_FIXTURES)
def test_is_encoded(_, data, encoded_data):
    assert is_encoded(encoded_data)


@pytest.mark.parametrize("encoded_data", INCORRECT_ENCODED_DATA)
def test_is_encoded_incorrect_encoding(encoded_data):
    assert not is_encoded(encoded_data)


def test_decode_return_encoding():
    """Test decode with return_encoding parameter."""
    encoding, decoded = decode("f796573206d616e692021", return_encoding=True)
    assert encoding == "base16"
    assert decoded == ensure_bytes("yes mani !")


def test_is_encoding_supported():
    """Test is_encoding_supported function."""
    assert is_encoding_supported("base64")
    assert is_encoding_supported("base16")
    assert not is_encoding_supported("base999")


def test_list_encodings():
    """Test list_encodings function."""
    encodings = list_encodings()
    assert "base64" in encodings
    assert "base16" in encodings
    assert "base32pad" in encodings
    assert "base64pad" in encodings
    assert len(encodings) >= 24  # Should have at least 24 encodings


def test_get_encoding_info():
    """Test get_encoding_info function."""
    info = get_encoding_info("base64")
    assert info.encoding == "base64"
    assert info.code == b"m"
    assert info.converter is not None

    with pytest.raises(UnsupportedEncodingError):
        get_encoding_info("base999")


def test_encoder_class():
    """Test Encoder class."""
    encoder = Encoder("base64")
    assert encoder.encoding == "base64"

    encoded = encoder.encode("hello")
    assert encoded.startswith(b"m")

    with pytest.raises(UnsupportedEncodingError):
        Encoder("base999")


def test_decoder_class():
    """Test Decoder class."""
    decoder = Decoder()
    # Use a known good encoding
    test_data = encode("base64", "hello")
    decoded = decoder.decode(test_data)
    assert decoded == ensure_bytes("hello")

    encoding, decoded = decoder.decode(test_data, return_encoding=True)
    assert encoding == "base64"
    assert decoded == ensure_bytes("hello")


def test_decoder_composition():
    """Test decoder composition with or_ method."""
    decoder1 = Decoder()
    decoder2 = Decoder()

    # This should work with any valid multibase string
    composed = decoder1.or_(decoder2)
    test_data = encode("base64", "hello")
    decoded = composed.decode(test_data)
    assert decoded == ensure_bytes("hello")

    # Should fail with invalid data
    with pytest.raises(DecodingError):
        composed.decode("invalid")
