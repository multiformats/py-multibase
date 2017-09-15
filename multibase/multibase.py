from collections import namedtuple
from morphys import ensure_bytes

from .converters import BaseStringConverter, Base16StringConverter, IdentityConverter

Codec = namedtuple('Codec', 'encoding,code,converter')
CODE_LENGTH = 1
CODECS = [
    Codec('identity', b'\x00', IdentityConverter()),
    Codec('base2', b'0', BaseStringConverter('01')),
    Codec('base8', b'7', BaseStringConverter('01234567')),
    Codec('base10', b'9', BaseStringConverter('0123456789')),
    Codec('base16', b'f', Base16StringConverter()),
    Codec('base32hex', b'v', BaseStringConverter('0123456789abcdefghijklmnopqrstuv')),
    Codec('base32', b'b', BaseStringConverter('abcdefghijklmnopqrstuvwxyz234567')),
    Codec('base32z', b'h', BaseStringConverter('ybndrfg8ejkmcpqxot1uwisza345h769')),
    Codec('base58flickr', b'Z', BaseStringConverter('123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')),
    Codec('base58btc', b'z', BaseStringConverter('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')),
    Codec('base64', b'm', BaseStringConverter('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')),
    Codec('base64url', b'u', BaseStringConverter(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_',
        sign='$')
    ),
]

CODECS_LOOKUP = {}
for codec in CODECS:
    CODECS_LOOKUP[codec.encoding] = codec
    CODECS_LOOKUP[codec.code] = codec


def encode(encoding, data):
    """
    Encodes the given data using the encoding that is specified

    :param str encoding: encoding to use, should be one of the supported encoding
    :param data: data to encode
    :type data: str or bytes
    :return: multibase encoded data
    :rtype: bytes
    :raises ValueError: if the encoding is not supported
    """
    data = ensure_bytes(data, 'utf8')
    try:
        return CODECS_LOOKUP[encoding].code + CODECS_LOOKUP[encoding].converter.encode(data)
    except KeyError:
        raise ValueError('Encoding {} not supported.'.format(encoding))


def get_codec(data):
    """
    Returns the codec used to encode the given data

    :param data: multibase encoded data
    :type data: str or bytes
    :return: the :py:obj:`multibase.Codec` object for the data's codec
    :raises ValueError: if the codec is not supported
    """
    try:
        key = ensure_bytes(data[:CODE_LENGTH], 'utf8')
        codec = CODECS_LOOKUP[key]
    except KeyError:
        raise ValueError('Can not determine encoding for {}'.format(data))
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
        if get_codec(data):
            return True
    except ValueError:
        return False

    return False


def decode(data):
    """
    Decode the multibase decoded data
    :param data: multibase encoded data
    :type data: str or bytes
    :return: decoded data
    :rtype: str
    """
    data = ensure_bytes(data, 'utf8')
    codec = get_codec(data)
    return codec.converter.decode(data[CODE_LENGTH:])
