#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `multibase` package."""

import pytest
from morphys import ensure_bytes

from multibase import encode, decode

TEST_FIXTURES = [
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


@pytest.mark.parametrize('encoding,data,encoded_data', TEST_FIXTURES)
def test_encode(encoding, data, encoded_data):
    assert encode(encoding, data) == ensure_bytes(encoded_data)


@pytest.mark.parametrize('encoding,data,encoded_data', TEST_FIXTURES)
def test_decode(encoding, data, encoded_data):
    assert decode(encoded_data) == ensure_bytes(data)
