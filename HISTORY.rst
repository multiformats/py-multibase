History
=======

.. towncrier release notes start

py-multibase v2.0.0 (2025-12-17)
--------------------------------

Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Added release documentation to contributing docs. (`#23 <https://github.com/multiformats/py-multibase/issues/23>`__)
- Fixed Read the Docs build failures by updating deprecated Sphinx settings and adding API documentation generation. (`#31 <https://github.com/multiformats/py-multibase/issues/31>`__)


Features
~~~~~~~~

- Added complete multibase encoding support and enhanced API features.

  **New Encodings (10 total):**
  - base16upper (prefix F) - Uppercase hexadecimal encoding
  - base32upper (prefix B) - Uppercase base32 encoding
  - base32pad (prefix c) - Base32 with RFC 4648 padding
  - base32padupper (prefix C) - Base32 uppercase with padding
  - base32hexupper (prefix V) - Base32hex uppercase variant
  - base32hexpad (prefix t) - Base32hex with RFC 4648 padding
  - base32hexpadupper (prefix T) - Base32hex uppercase with padding
  - base64pad (prefix M) - Base64 with RFC 4648 padding
  - base64urlpad (prefix U) - Base64url with padding
  - base256emoji (prefix 🚀) - Emoji-based encoding

  **API Enhancements:**
  - Added ``Encoder`` and ``Decoder`` classes for reusable encoding/decoding
  - Added ``decode(return_encoding=True)`` parameter to return encoding type along with decoded data
  - Added structured exception classes: ``UnsupportedEncodingError``, ``InvalidMultibaseStringError``, ``DecodingError``
  - Added encoding metadata functions: ``get_encoding_info()``, ``list_encodings()``, ``is_encoding_supported()``
  - Added decoder composition support via ``Decoder.or_()`` method

  This brings py-multibase to 100% encoding coverage (24/24 encodings) matching reference implementations (go-multibase, rust-multibase, js-multiformats). (`#20 <https://github.com/multiformats/py-multibase/issues/20>`__)


Internal Changes - for py-multibase Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Modernized project infrastructure: migrated to pyproject.toml, replaced Travis CI with GitHub Actions, updated Python support to 3.10-3.14, replaced flake8 with ruff, and added pre-commit hooks. This is an internal change that does not affect the public API. (`#18 <https://github.com/multiformats/py-multibase/issues/18>`__)
- Dropped ``coverage`` and ``codecov`` references, no longer using it. (`#23 <https://github.com/multiformats/py-multibase/issues/23>`__)
- Updated pyupgrade to v3.21.2 to fix Python 3.14 compatibility in linting checks. (`#24 <https://github.com/multiformats/py-multibase/issues/24>`__)
- Fixed release process by adding automated release targets to Makefile, adding doctest support to documentation builds, fixing version string configuration, and creating comprehensive package test script. This aligns the release process with py-multihash PR 31 improvements. (`#26 <https://github.com/multiformats/py-multibase/issues/26>`__)


1.0.3 (2020-10-26)
------------------
* Add base36 and base36 upper encodings
* Fix issue with base16 encoding

1.0.0 (2018-10-19)
------------------

* Re-implement encoding for base32 and base64, as the implementation was buggy
* Add extensive tests for all encodings

0.1.0 (2017-09-02)
------------------

* First release on PyPI.
