from baseconv import BaseConverter
from morphys import ensure_bytes


class BaseStringConverter(BaseConverter):
    def encode(self, bytes):
        number = int.from_bytes(bytes, byteorder='big', signed=False)
        return ensure_bytes(super(BaseStringConverter, self).encode(number))

    def bytes_to_int(self, bytes):
        length = len(bytes)
        base = len(self.digits)
        value = 0

        for i, x in enumerate(bytes):
            value += self.digits.index(chr(x)) * base ** (length - (i + 1))
        return value

    def decode(self, bytes):
        decoded_int = self.bytes_to_int(bytes)
        # See https://docs.python.org/3.5/library/stdtypes.html#int.to_bytes for more about the magical expression
        # below
        decoded_data = decoded_int.to_bytes((decoded_int.bit_length() + 7) // 8, byteorder='big')
        return decoded_data


class Base16StringConverter(BaseStringConverter):
    def __init__(self):
        self.digits = '0123456789abcdef'

    def encode(self, bytes):
        return ensure_bytes(''.join(['{:02x}'.format(byte) for byte in bytes]))


class IdentityConverter(object):
    def encode(self, x):
        return x

    def decode(self, x):
        return x
