"""Top-level package for py-multibase."""

__author__ = """Dhruv Baldawa"""
__email__ = "dhruv@dhruvb.com"
__version__ = "2.0.0"

from .exceptions import (  # noqa: F401
    DecodingError,
    InvalidMultibaseStringError,
    MultibaseError,
    UnsupportedEncodingError,
)
from .multibase import (  # noqa: F401
    ENCODINGS,
    ComposedDecoder,
    Decoder,
    Encoder,
    Encoding,
    decode,
    encode,
    get_codec,
    get_encoding_info,
    is_encoded,
    is_encoding_supported,
    list_encodings,
)
