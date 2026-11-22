History
=======

.. towncrier release notes start

py-multibase v2.1.0 (2026-11-22)
--------------------------------

Bugfixes
~~~~~~~~

- Fix integer-based encodings dropping leading ``0x00`` bytes on encode and decode, and add round-trip tests covering every supported encoding with random, all-zero, all-ones and leading-zero data. (`#40 <https://github.com/multiformats/py-multibase/issues/40>`__)
- Name-based APIs (``encode``, ``is_encoding_supported``, ``get_encoding_info``, and ``Encoder``) no longer treat multibase prefix bytes as encoding names. Prefix codes continue to be resolved via ``get_codec`` / ``decode``. (`#44 <https://github.com/multiformats/py-multibase/issues/44>`__)


Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Aligned local documentation builds with Read the Docs by using ``python -m sphinx.ext.apidoc`` for the ``multibase`` package. (`#31 <https://github.com/multiformats/py-multibase/issues/31>`__)


Features
~~~~~~~~

- Add ``encoder_by_name()``, which constructs an :class:`~multibase.Encoder` from an encoding name or its single-character prefix, and export it from the ``multibase`` package. (`#39 <https://github.com/multiformats/py-multibase/issues/39>`__)
- Add a read-only ``Encoder.code`` property exposing the multibase prefix byte of an encoder's encoding. (`#47 <https://github.com/multiformats/py-multibase/issues/47>`__)


Internal Changes - for py-multibase Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add ``pytest-benchmark`` benchmarks for encoding, decoding and round-tripping every supported encoding. (`#42 <https://github.com/multiformats/py-multibase/issues/42>`__)
- Add Hypothesis-based fuzz tests that exercise the decoder with arbitrary binary and text input. (`#43 <https://github.com/multiformats/py-multibase/issues/43>`__)
- Remove the unused ``six`` runtime dependency; ``py-multibase`` requires Python 3.10 or newer. (`#45 <https://github.com/multiformats/py-multibase/issues/45>`__)
- Renamed converter parameters that shadowed the builtin ``bytes`` and corrected the Base16 decode comment (no behavior change). (`#62 <https://github.com/multiformats/py-multibase/issues/62>`__)
- Adopt pinned ``pyrefly==1.5.0`` typechecking alongside mypy for tooling parity with sibling packages. (`#64 <https://github.com/multiformats/py-multibase/issues/64>`__)


Miscellaneous Changes
~~~~~~~~~~~~~~~~~~~~~

- `#41 <https://github.com/multiformats/py-multibase/issues/41>`__, `#46 <https://github.com/multiformats/py-multibase/issues/46>`__


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
