import base64
from io import BytesIO
from itertools import zip_longest

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


class BaseByteStringConverter(object):
    ENCODE_GROUP_BYTES = 1
    ENCODING_BITS = 1
    DECODING_BITS = 1

    def __init__(self, digits):
        self.digits = digits
        self.GROUP_SIZE = self.ENCODE_GROUP_BYTES * self.ENCODING_BITS
        self.DECODE_GROUP_BYTES = self.GROUP_SIZE // self.DECODING_BITS

    def grouper(self, iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    def _bytes_to_base64(self, bytes_):
        buffer = BytesIO(bytes_)
        encoded_bytes = BytesIO()
        while True:
            byte_ = buffer.read(self.ENCODE_GROUP_BYTES)
            if not byte_:
                break

            # convert all bytes to a binary format and concatenate them into a 24bit string
            binstringfmt = '{{:0{}b}}'.format(self.ENCODING_BITS)
            binstring = ''.join([binstringfmt.format(x) for x in byte_])
            # break the 24 bit length string into pieces of 6 bits each
            digits = (int(''.join(x), 2) for x in self.grouper(binstring, self.DECODING_BITS, '0'))

            for digit in digits:
                # convert binary representation to an integer
                encoded_bytes.write(ensure_bytes(self.digits[digit]))

        return encoded_bytes.getvalue()

    def _base64_to_bytes(self, base64_bytes):
        buffer = BytesIO()
        outbuffer = BytesIO()

        for byte_ in base64_bytes.decode():
            idx = self.digits.index(byte_)
            buffer.write(bytes([idx]))

        buffer.seek(0)
        while True:
            byte_ = buffer.read(self.DECODE_GROUP_BYTES)
            if not byte_:
                break

            # convert all bytes to a binary format and concatenate them into a 8, 16, 24bit string
            binstringfmt = '{{:0{}b}}'.format(self.DECODING_BITS)
            binstring = ''.join([binstringfmt.format(x) for x in byte_])

            # break the 24 bit length string into pieces of 8 bits each
            digits = [int(''.join(x), 2) for x in map(''.join, zip(*[iter(binstring)] * self.ENCODING_BITS))]

            for digit in digits:
                outbuffer.write(bytes([digit]))

        return outbuffer.getvalue()

    def encode(self, bytes):
        return self._bytes_to_base64(ensure_bytes(bytes))

    def decode(self, bytes):
        return self._base64_to_bytes(ensure_bytes(bytes))


class Base64StringConverter(BaseByteStringConverter):
    ENCODE_GROUP_BYTES = 3
    ENCODING_BITS = 8
    DECODING_BITS = 6


class Base32StringConverter(BaseByteStringConverter):
    ENCODE_GROUP_BYTES = 4
    ENCODING_BITS = 8
    DECODING_BITS = 5


class IdentityConverter(object):
    def encode(self, x):
        return x

    def decode(self, x):
        return x
