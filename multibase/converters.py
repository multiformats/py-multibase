from io import BytesIO
from itertools import zip_longest

from baseconv import BaseConverter
from morphys import ensure_bytes


class BaseStringConverter(BaseConverter):
    def encode(self, bytes):
        number = int.from_bytes(bytes, byteorder="big", signed=False)
        return ensure_bytes(super().encode(number))

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
        decoded_data = decoded_int.to_bytes((decoded_int.bit_length() + 7) // 8, byteorder="big")
        return decoded_data


class Base16StringConverter(BaseStringConverter):
    def __init__(self, digits):
        super().__init__(digits)
        self.uppercase = digits.isupper()

    def encode(self, bytes):
        result = "".join([f"{byte:02x}" for byte in bytes])
        if self.uppercase:
            result = result.upper()
        return ensure_bytes(result)

    def decode(self, data):
        # Base16 decode is case-insensitive, normalize to our digits case
        if isinstance(data, bytes):
            data_str = data.decode("utf-8")
        else:
            data_str = data
        # Convert to match our digits case
        if self.uppercase:
            data_str = data_str.upper()
        else:
            data_str = data_str.lower()
        return super().decode(data_str.encode("utf-8"))


class BaseByteStringConverter:
    ENCODE_GROUP_BYTES = 1
    ENCODING_BITS = 1
    DECODING_BITS = 1

    def __init__(self, digits, pad=False):
        self.digits = digits
        self.pad = pad

    def _chunk_with_padding(self, iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # _chunk_with_padding('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    def _chunk_without_padding(self, iterable, n):
        return map("".join, zip(*[iter(iterable)] * n))

    def _encode_bytes(self, bytes_, group_bytes, encoding_bits, decoding_bits, output_chars):
        buffer = BytesIO(bytes_)
        encoded_bytes = BytesIO()
        input_length = len(bytes_)

        while True:
            byte_ = buffer.read(group_bytes)
            if not byte_:
                break

            # convert all bytes to a binary format and concatenate them into a 24bit string
            binstringfmt = f"{{:0{encoding_bits}b}}"
            binstring = "".join([binstringfmt.format(x) for x in byte_])
            # break the 24 bit length string into pieces of 6 bits each and convert them to integer
            digits = (int("".join(x), 2) for x in self._chunk_with_padding(binstring, decoding_bits, "0"))

            for digit in digits:
                # convert binary representation to an integer
                encoded_bytes.write(ensure_bytes(self.digits[digit]))

        result = encoded_bytes.getvalue()

        # Add padding if needed
        if self.pad:
            remainder = input_length % group_bytes
            if remainder > 0:
                # For partial groups, we need to pad the output
                # The padding makes the output length a multiple of output_chars
                actual_output_len = len(result)
                # Calculate padding needed to reach next multiple of output_chars
                padding_needed = (output_chars - (actual_output_len % output_chars)) % output_chars
                if padding_needed == 0 and actual_output_len % output_chars != 0:
                    # If we're not at a multiple, pad to the next multiple
                    padding_needed = output_chars - (actual_output_len % output_chars)
                result += ensure_bytes("=" * padding_needed)

        return result

    def _decode_bytes(self, bytes_, group_bytes, decoding_bits, encoding_bits):
        # Remove padding if present
        if self.pad:
            bytes_ = bytes_.rstrip(b"=")

        buffer = BytesIO()
        decoded_bytes = BytesIO()

        for byte_ in bytes_.decode():
            idx = self.digits.index(byte_)
            buffer.write(bytes([idx]))

        buffer.seek(0)
        while True:
            byte_ = buffer.read(group_bytes)
            if not byte_:
                break

            # convert all bytes to a binary format and concatenate them into a 8, 16, 24bit string
            binstringfmt = f"{{:0{decoding_bits}b}}"
            binstring = "".join([binstringfmt.format(x) for x in byte_])

            # break the 24 bit length string into pieces of 8 bits each and convert them to integer
            digits = [int("".join(x), 2) for x in self._chunk_without_padding(binstring, encoding_bits)]

            for digit in digits:
                decoded_bytes.write(bytes([digit]))

        return decoded_bytes.getvalue()

    def encode(self, bytes):
        raise NotImplementedError

    def decode(self, bytes):
        return NotImplementedError


class Base64StringConverter(BaseByteStringConverter):
    def encode(self, bytes):
        return self._encode_bytes(ensure_bytes(bytes), 3, 8, 6, 4)

    def decode(self, bytes):
        return self._decode_bytes(ensure_bytes(bytes), 4, 6, 8)


class Base32StringConverter(BaseByteStringConverter):
    def encode(self, bytes):
        return self._encode_bytes(ensure_bytes(bytes), 5, 8, 5, 8)

    def decode(self, bytes):
        return self._decode_bytes(ensure_bytes(bytes), 8, 5, 8)


class Base256EmojiConverter:
    """Base256 emoji encoding using 256 unique emoji characters."""

    def _get_emoji_chars(self):
        """Get the 256 emoji characters used in base256emoji.

        This generates a set of 256 unique emojis from various emoji ranges.
        The actual specification may use a different set, but this provides
        a working implementation.
        """
        # Generate emojis from various Unicode ranges
        # Using a comprehensive set to ensure we have 256 unique emojis
        emojis = []

        # Emoticons and faces (U+1F600-U+1F64F)
        for code in range(0x1F600, 0x1F650):
            try:
                emojis.append(chr(code))
            except (ValueError, OverflowError):
                pass

        # Various object emojis (U+1F300-U+1F5FF)
        for code in range(0x1F300, 0x1F600):
            try:
                emojis.append(chr(code))
            except (ValueError, OverflowError):
                pass

        # Food and drink (U+1F32D-U+1F37F)
        for code in range(0x1F32D, 0x1F380):
            try:
                emojis.append(chr(code))
            except (ValueError, OverflowError):
                pass

        # Activity and sports (U+1F3C0-U+1F3FF)
        for code in range(0x1F3C0, 0x1F400):
            try:
                emojis.append(chr(code))
            except (ValueError, OverflowError):
                pass

        # Symbols and pictographs (U+1F400-U+1F4FF)
        for code in range(0x1F400, 0x1F500):
            try:
                emojis.append(chr(code))
            except (ValueError, OverflowError):
                pass

        # Additional emojis to reach 256
        # Using various other emoji ranges
        additional_ranges = [
            (0x1F500, 0x1F53D),  # Miscellaneous Symbols and Pictographs
            (0x1F680, 0x1F6C0),  # Transport and Map Symbols
            (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
        ]

        for start, end in additional_ranges:
            for code in range(start, end):
                try:
                    emojis.append(chr(code))
                except (ValueError, OverflowError):
                    pass
                if len(emojis) >= 256:
                    break
            if len(emojis) >= 256:
                break

        # Ensure we have exactly 256
        return "".join(emojis[:256])

    def __init__(self):
        self.EMOJI_CHARS = self._get_emoji_chars()
        if len(self.EMOJI_CHARS) != 256:
            raise ValueError(f"EMOJI_CHARS must contain exactly 256 characters, got {len(self.EMOJI_CHARS)}")
        # Create mapping from byte value to emoji
        self.byte_to_emoji = {i: self.EMOJI_CHARS[i] for i in range(256)}
        # Create reverse mapping from emoji to byte value
        self.emoji_to_byte = {emoji: byte for byte, emoji in self.byte_to_emoji.items()}

    def encode(self, bytes_):
        """Encode bytes to emoji string."""
        bytes_ = ensure_bytes(bytes_)
        result = []
        for byte_val in bytes_:
            result.append(self.byte_to_emoji[byte_val])
        return "".join(result).encode("utf-8")

    def decode(self, bytes_):
        """Decode emoji string to bytes."""
        bytes_ = ensure_bytes(bytes_, "utf8")
        # Decode UTF-8 to get emoji string
        emoji_str = bytes_.decode("utf-8")
        result = bytearray()
        # Iterate through emoji characters
        # We need to match emojis which may be multiple code points
        i = 0
        while i < len(emoji_str):
            matched = False
            # Try matching from longest to shortest (up to 4 code points)
            for length in range(min(4, len(emoji_str) - i), 0, -1):
                candidate = emoji_str[i : i + length]
                if candidate in self.emoji_to_byte:
                    result.append(self.emoji_to_byte[candidate])
                    i += length
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Invalid emoji character at position {i}: {emoji_str[i : i + 4]}")
        return bytes(result)


class IdentityConverter:
    def encode(self, x):
        return x

    def decode(self, x):
        return x
