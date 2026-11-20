API Reference
-------------

.. py:currentmodule:: multibase

Encoding **names** (for example ``"base16"``) are used by :func:`encode`,
:func:`is_encoding_supported`, :func:`get_encoding_info`, and :class:`Encoder`.
Multibase **prefix codes** (for example ``b"f"``) are resolved from encoded
data by :func:`get_codec` and :func:`decode`, not passed as encoding names.

.. autofunction:: encode

.. autofunction:: decode

.. autofunction:: get_codec

.. autofunction:: is_encoded

.. autofunction:: is_encoding_supported

.. autofunction:: get_encoding_info

.. autoclass:: Encoder
   :members:
