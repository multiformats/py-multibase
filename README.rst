**This project is no longer maintained and has been archived.**

py-multibase
------------

.. image:: https://img.shields.io/pypi/v/py-multibase.svg
        :target: https://pypi.python.org/pypi/py-multibase

.. image:: https://github.com/multiformats/py-multibase/actions/workflows/tox.yml/badge.svg
        :target: https://github.com/multiformats/py-multibase/actions

.. image:: https://readthedocs.org/projects/py-multibase/badge/?version=stable
        :target: https://py-multibase.readthedocs.io/en/stable/?badge=stable
        :alt: Documentation Status

`Multibase <https://github.com/multiformats/multibase>`_ implementation for Python

Multibase is a protocol for distinguishing base encodings and other simple string encodings, and for ensuring full compatibility with program interfaces.

It answers the question: Given data d encoded into string s, how can I tell what base d is encoded with?

Base encodings exist because transports have restrictions, use special in-band sequences, or must be human-friendly.
When systems chose a base to use, it is not always clear which base to use, as there are many tradeoffs in the decision.
Multibase is here to save programs and programmers from worrying about which encoding is best.

It solves the biggest problem: a program can use multibase to take input or produce output in whichever base is desired.

The important part is that the value is self-describing, letting other programs elsewhere know what encoding it is using.

* Free software: MIT license
* Documentation: https://py-multibase.readthedocs.io.
* Python versions: Python 3.10, 3.11, 3.12, 3.13, 3.14

Installation
============

.. code-block:: shell

    $ pip install py-multibase


Sample Usage
============

.. code-block:: python

    >>> # encoding a buffer
    >>> from multibase import encode, decode
    >>> encode('base58btc', 'hello world')
    b'zStV1DL6CwTryKyV'
    >>> encode('base64', 'hello world')
    b'mGhlbGxvIHdvcmxk'
    >>> # decoding a multibase
    >>> decode('mGhlbGxvIHdvcmxk')
    b'hello world'
    >>> decode(b'zStV1DL6CwTryKyV')
    b'hello world'
    >>> decode(encode('base2', b'hello world'))
    b'hello world'

    >>> # Using reusable Encoder/Decoder classes
    >>> from multibase import Encoder, Decoder
    >>> encoder = Encoder('base64')
    >>> encoded1 = encoder.encode('data1')
    >>> encoded2 = encoder.encode('data2')

    >>> decoder = Decoder()
    >>> decoded = decoder.decode(encoded1)

    >>> # Getting encoding information
    >>> from multibase import get_encoding_info, list_encodings, is_encoding_supported
    >>> info = get_encoding_info('base64')
    >>> print(info.encoding, info.code)
    base64 b'm'
    >>> all_encodings = list_encodings()
    >>> is_encoding_supported('base64')
    True

    >>> # Decode with encoding return
    >>> encoding, data = decode(encoded1, return_encoding=True)
    >>> print(f'Encoded with {encoding}: {data}')


Supported codecs
================

* base2
* base8
* base10
* base16
* base16upper
* base32hex
* base32hexupper
* base32hexpad
* base32hexpadupper
* base32
* base32upper
* base32pad
* base32padupper
* base32z
* base36
* base36upper
* base58flickr
* base58btc
* base64
* base64pad
* base64url
* base64urlpad
* base256emoji
