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
    data = ensure_bytes(data, 'utf8')
    try:
        return CODECS_LOOKUP[encoding].code + CODECS_LOOKUP[encoding].converter.encode(data)
    except KeyError:
        raise ValueError('Encoding {} not supported.'.format(encoding))


def get_codec(data):
    try:
        codec = CODECS_LOOKUP[data[:CODE_LENGTH]]
    except KeyError:
        raise ValueError('Can not determine encoding for {}'.format(data))
    else:
        return codec


def is_encoded(data):
    try:
        if get_codec(data):
            return True
    except ValueError:
        return False

    return False


def decode(data):
    data = ensure_bytes(data, 'utf8')
    codec = get_codec(data)
    return codec.converter.decode(data[CODE_LENGTH:])
