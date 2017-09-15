============
py-multibase
============



.. image:: https://img.shields.io/pypi/v/py-multibase.svg
        :target: https://pypi.python.org/pypi/py-multibase

.. image:: https://img.shields.io/travis/multiformats/py-multibase.svg
        :target: https://travis-ci.org/multiformats/py-multibase

.. image:: https://codecov.io/gh/multiformats/py-multibase/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/multiformats/py-multibase

.. image:: https://readthedocs.org/projects/py-multibase/badge/?version=latest
        :target: https://py-multibase.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/multiformats/py-multibase/shield.svg
     :target: https://pyup.io/repos/github/multiformats/py-multibase/
     :alt: Updates


Multibase implementation for Python


* Free software: MIT license
* Documentation: https://py-multibase.readthedocs.io.

Installation
------------

    $ pip install py-multibase


Sample Usage
------------

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


Supported codecs
----------------

* base2
* base8
* base10
* base16
* base16
* base16
* base32hex
* base32
* base32z
* base58flickr
* base58btc
* base64
* base64url
