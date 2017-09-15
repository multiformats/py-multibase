#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `multibase` package."""

import pytest
from morphys import ensure_bytes

from multibase import encode, decode, is_encoded

TEST_FIXTURES = [
    ['identity', 'yes mani !', '\x00yes mani !'],
    ['base2', 'yes mani !', '01111001011001010111001100100000011011010110000101101110011010010010000000100001'],
    ['base8', 'yes mani !', '7171312714403326055632220041'],
    ['base10', 'yes mani !', '9573277761329450583662625'],
    ['base16', 'yes mani !', 'f796573206d616e692021'],
    ['base16', '\x01', 'f01'],
    ['base16', '\x0f', 'f0f'],
    ['base32hex', 'yes mani !', 'vf5in683dc5n6i811'],
    ['base32', 'yes mani !', 'bpfsxgidnmfxgsibb'],
    ['base32z', 'yes mani !', 'hxf1zgedpcfzg1ebb'],
    ['base58flickr', 'yes mani !', 'Z7Pznk19XTTzBtx'],
    ['base58btc', 'yes mani !', 'z7paNL19xttacUY'],
    ['base64', '÷ïÿ', 'mw7fDr8O/'],
    ['base64url', '÷ïÿ', 'uw7fDr8O_'],
]

INCORRECT_ENCODINGS = ['base58', 'base4']
INCORRECT_ENCODED_DATA = ['abcdefghi', '!qweqweqeqw']


@pytest.mark.parametrize('encoding,data,encoded_data', TEST_FIXTURES)
def test_encode(encoding, data, encoded_data):
    assert encode(encoding, data) == ensure_bytes(encoded_data)


@pytest.mark.parametrize('encoding', INCORRECT_ENCODINGS)
def test_encode_incorrect_encoding(encoding):
    with pytest.raises(ValueError) as excinfo:
        encode(encoding, 'test data')
    assert 'not supported' in str(excinfo.value)


@pytest.mark.parametrize('_,data,encoded_data', TEST_FIXTURES)
def test_decode(_, data, encoded_data):
    assert decode(encoded_data) == ensure_bytes(data)


@pytest.mark.parametrize('encoded_data', INCORRECT_ENCODED_DATA)
def test_decode_incorrect_encoding(encoded_data):
    with pytest.raises(ValueError) as excinfo:
        decode(encoded_data)
    assert 'Can not determine encoding' in str(excinfo.value)


@pytest.mark.parametrize('_,data,encoded_data', TEST_FIXTURES)
def test_is_encoded(_, data, encoded_data):
    assert is_encoded(encoded_data)
    assert not is_encoded(data)


@pytest.mark.parametrize('encoded_data', INCORRECT_ENCODED_DATA)
def test_is_encoded_incorrect_encoding(encoded_data):
    assert not is_encoded(encoded_data)
