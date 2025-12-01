from collections import namedtuple

from morphys import ensure_bytes

from .converters import (
    Base16StringConverter,
    Base32StringConverter,
    Base64StringConverter,
    Base256EmojiConverter,
    BaseStringConverter,
    IdentityConverter,
)
from .exceptions import (
    DecodingError,
    InvalidMultibaseStringError,
    UnsupportedEncodingError,
)

Encoding = namedtuple("Encoding", "encoding,code,converter")
CODE_LENGTH = 1
ENCODINGS = [
    Encoding("identity", b"\x00", IdentityConverter()),
    Encoding("base2", b"0", BaseStringConverter("01")),
    Encoding("base8", b"7", BaseStringConverter("01234567")),
    Encoding("base10", b"9", BaseStringConverter("0123456789")),
    Encoding("base16", b"f", Base16StringConverter("0123456789abcdef")),
    Encoding("base16upper", b"F", Base16StringConverter("0123456789ABCDEF")),
    Encoding("base32hex", b"v", Base32StringConverter("0123456789abcdefghijklmnopqrstuv")),
    Encoding("base32hexupper", b"V", Base32StringConverter("0123456789ABCDEFGHIJKLMNOPQRSTUV")),
    Encoding("base32hexpad", b"t", Base32StringConverter("0123456789abcdefghijklmnopqrstuv", pad=True)),
    Encoding("base32hexpadupper", b"T", Base32StringConverter("0123456789ABCDEFGHIJKLMNOPQRSTUV", pad=True)),
    Encoding("base32", b"b", Base32StringConverter("abcdefghijklmnopqrstuvwxyz234567")),
    Encoding("base32upper", b"B", Base32StringConverter("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")),
    Encoding("base32pad", b"c", Base32StringConverter("abcdefghijklmnopqrstuvwxyz234567", pad=True)),
    Encoding("base32padupper", b"C", Base32StringConverter("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", pad=True)),
    Encoding("base32z", b"h", BaseStringConverter("ybndrfg8ejkmcpqxot1uwisza345h769")),
    Encoding("base36", b"k", BaseStringConverter("0123456789abcdefghijklmnopqrstuvwxyz")),
    Encoding("base36upper", b"K", BaseStringConverter("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")),
    Encoding("base58flickr", b"Z", BaseStringConverter("123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ")),
    Encoding("base58btc", b"z", BaseStringConverter("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")),
    Encoding("base64", b"m", Base64StringConverter("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")),
    Encoding(
        "base64pad",
        b"M",
        Base64StringConverter("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", pad=True),
    ),
    Encoding(
        "base64url",
        b"u",
        Base64StringConverter("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"),
    ),
    Encoding(
        "base64urlpad",
        b"U",
        Base64StringConverter("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_", pad=True),
    ),
    Encoding("base256emoji", "🚀".encode(), Base256EmojiConverter()),
]

ENCODINGS_LOOKUP = {}
for codec in ENCODINGS:
    ENCODINGS_LOOKUP[codec.encoding] = codec
    ENCODINGS_LOOKUP[codec.code] = codec


def encode(encoding, data):
    """
    Encodes the given data using the encoding that is specified

    :param str encoding: encoding to use, should be one of the supported encoding
    :param data: data to encode
    :type data: str or bytes
    :return: multibase encoded data
    :rtype: bytes
    :raises UnsupportedEncodingError: if the encoding is not supported
    """
    data = ensure_bytes(data, "utf8")
    try:
        return ENCODINGS_LOOKUP[encoding].code + ENCODINGS_LOOKUP[encoding].converter.encode(data)
    except KeyError:
        raise UnsupportedEncodingError(f"Encoding {encoding} not supported.")


def get_codec(data):
    """
    Returns the codec used to encode the given data

    :param data: multibase encoded data
    :type data: str or bytes
    :return: the :py:obj:`multibase.Encoding` object for the data's codec
    :raises InvalidMultibaseStringError: if the codec is not supported
    """
    data = ensure_bytes(data, "utf8")
    # Check for base256emoji first (4-byte UTF-8 prefix)
    if len(data) >= 4:
        emoji_prefix = data[:4]
        if emoji_prefix in ENCODINGS_LOOKUP:
            return ENCODINGS_LOOKUP[emoji_prefix]

    # Check for single-byte prefixes
    try:
        key = data[:CODE_LENGTH]
        codec = ENCODINGS_LOOKUP[key]
    except KeyError:
        raise InvalidMultibaseStringError(f"Can not determine encoding for {data}")
    else:
        return codec


def is_encoded(data):
    """
    Checks if the given data is encoded or not

    :param data: multibase encoded data
    :type data: str or bytes
    :return: if the data is encoded or not
    :rtype: bool
    """
    try:
        get_codec(data)
        return True
    except (ValueError, InvalidMultibaseStringError):
        return False


def is_encoding_supported(encoding):
    """
    Check if an encoding is supported.

    :param encoding: encoding name to check
    :type encoding: str
    :return: True if encoding is supported, False otherwise
    :rtype: bool
    """
    return encoding in ENCODINGS_LOOKUP


def list_encodings():
    """
    List all supported encodings.

    :return: list of encoding names
    :rtype: list
    """
    return [enc.encoding for enc in ENCODINGS]


def get_encoding_info(encoding):
    """
    Get information about a specific encoding.

    :param encoding: encoding name
    :type encoding: str
    :return: Encoding namedtuple with encoding, code, and converter
    :rtype: Encoding
    :raises UnsupportedEncodingError: if encoding is not supported
    """
    if encoding not in ENCODINGS_LOOKUP:
        raise UnsupportedEncodingError(f"Encoding {encoding} not supported.")
    return ENCODINGS_LOOKUP[encoding]


def decode(data, return_encoding=False):
    """
    Decode the multibase decoded data

    :param data: multibase encoded data
    :type data: str or bytes
    :param return_encoding: if True, return tuple (encoding, decoded_data)
    :type return_encoding: bool
    :return: decoded data, or tuple (encoding, decoded_data) if return_encoding=True
    :rtype: bytes or tuple
    :raises InvalidMultibaseStringError: if the data is not multibase encoded
    :raises DecodingError: if decoding fails
    """
    data = ensure_bytes(data, "utf8")
    try:
        codec = get_codec(data)
        # Handle base256emoji which has a 4-byte prefix
        prefix_length = len(codec.code)
        decoded = codec.converter.decode(data[prefix_length:])
        if return_encoding:
            return (codec.encoding, decoded)
        return decoded
    except (InvalidMultibaseStringError, UnsupportedEncodingError):
        # Re-raise these specific exceptions as-is since they already provide
        # appropriate context about what went wrong (invalid format or unsupported encoding)
        raise
    except Exception as e:
        # Wrap all other exceptions (e.g., converter errors, invalid data)
        # in DecodingError to provide consistent error handling
        raise DecodingError(f"Failed to decode multibase data: {e}") from e


class Encoder:
    """Reusable encoder for a specific encoding."""

    def __init__(self, encoding):
        """
        Initialize an encoder for a specific encoding.

        :param encoding: encoding name to use
        :type encoding: str
        :raises UnsupportedEncodingError: if encoding is not supported
        """
        if encoding not in ENCODINGS_LOOKUP:
            raise UnsupportedEncodingError(f"Encoding {encoding} not supported.")
        self.encoding = encoding
        self._codec = ENCODINGS_LOOKUP[encoding]

    def encode(self, data):
        """
        Encode data using this encoder's encoding.

        :param data: data to encode
        :type data: str or bytes
        :return: multibase encoded data
        :rtype: bytes
        """
        data = ensure_bytes(data, "utf8")
        return self._codec.code + self._codec.converter.encode(data)


class Decoder:
    """Reusable decoder for multibase data."""

    def __init__(self):
        """Initialize a decoder."""
        pass

    def decode(self, data, return_encoding=False):
        """
        Decode multibase encoded data.

        :param data: multibase encoded data
        :type data: str or bytes
        :param return_encoding: if True, return tuple (encoding, decoded_data)
        :type return_encoding: bool
        :return: decoded data, or tuple (encoding, decoded_data) if return_encoding=True
        :rtype: bytes or tuple
        :raises InvalidMultibaseStringError: if the data is not multibase encoded
        :raises DecodingError: if decoding fails
        """
        return decode(data, return_encoding=return_encoding)

    def or_(self, other_decoder):
        """
        Compose this decoder with another, trying this one first.

        This allows trying multiple decoders in sequence.

        :param other_decoder: another decoder to try if this one fails
        :type other_decoder: Decoder
        :return: a composed decoder
        :rtype: ComposedDecoder
        """
        return ComposedDecoder([self, other_decoder])


class ComposedDecoder:
    """A decoder that tries multiple decoders in sequence."""

    def __init__(self, decoders):
        """
        Initialize a composed decoder.

        :param decoders: list of decoders to try in order
        :type decoders: list
        """
        self.decoders = decoders

    def decode(self, data, return_encoding=False):
        """
        Try to decode with each decoder in sequence.

        :param data: multibase encoded data
        :type data: str or bytes
        :param return_encoding: if True, return tuple (encoding, decoded_data)
        :type return_encoding: bool
        :return: decoded data, or tuple (encoding, decoded_data) if return_encoding=True
        :rtype: bytes or tuple
        :raises DecodingError: if all decoders fail
        """
        last_error = None
        for decoder in self.decoders:
            try:
                return decoder.decode(data, return_encoding=return_encoding)
            except (InvalidMultibaseStringError, DecodingError) as e:
                last_error = e
                continue
        raise DecodingError(f"All decoders failed. Last error: {last_error}") from last_error
