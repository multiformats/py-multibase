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

        # Add padding if needed (RFC 4648)
        if self.pad:
            remainder = input_length % group_bytes
            if remainder > 0:
                # For partial groups, we need to pad the output
                # The padding makes the output length a multiple of output_chars
                chars_produced = len(result)
                # Calculate padding needed to reach next multiple of output_chars
                padding_needed = output_chars - (chars_produced % output_chars)
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
    """Base256 emoji encoding using 256 unique emoji characters.

    This implementation uses the exact same hardcoded emoji alphabet as
    js-multiformats and go-multibase reference implementations to ensure
    full compatibility. The alphabet is curated from Unicode emoji frequency
    data, excluding modifier-based emojis (such as flags) that are bigger
    than one single code point.
    """

    # Hardcoded emoji alphabet matching js-multiformats and go-multibase
    # This is the exact same alphabet used in reference implementations
    # Source: js-multiformats/src/bases/base256emoji.ts and go-multibase/base256emoji.go
    _EMOJI_ALPHABET = (
        "🚀🪐☄🛰🌌"  # Space
        "🌑🌒🌓🌔🌕🌖🌗🌘"  # Moon
        "🌍🌏🌎"  # Earth
        "🐉"  # Dragon
        "☀"  # Sun
        "💻🖥💾💿"  # Computer
        # Rest from Unicode emoji frequency data (most used first)
        "😂❤😍🤣😊🙏💕😭😘👍"
        "😅👏😁🔥🥰💔💖💙😢🤔"
        "😆🙄💪😉☺👌🤗💜😔😎"
        "😇🌹🤦🎉💞✌✨🤷😱😌"
        "🌸🙌😋💗💚😏💛🙂💓🤩"
        "😄😀🖤😃💯🙈👇🎶😒🤭"
        "❣😜💋👀😪😑💥🙋😞😩"
        "😡🤪👊🥳😥🤤👉💃😳✋"
        "😚😝😴🌟😬🙃🍀🌷😻😓"
        "⭐✅🥺🌈😈🤘💦✔😣🏃"
        "💐☹🎊💘😠☝😕🌺🎂🌻"
        "😐🖕💝🙊😹🗣💫💀👑🎵"
        "🤞😛🔴😤🌼😫⚽🤙☕🏆"
        "🤫👈😮🙆🍻🍃🐶💁😲🌿"
        "🧡🎁⚡🌞🎈❌✊👋😰🤨"
        "😶🤝🚶💰🍓💢🤟🙁🚨💨"
        "🤬✈🎀🍺🤓😙💟🌱😖👶"
        "🥴▶➡❓💎💸⬇😨🌚🦋"
        "😷🕺⚠🙅😟😵👎🤲🤠🤧"
        "📌🔵💅🧐🐾🍒😗🤑🌊🤯"
        "🐷☎💧😯💆👆🎤🙇🍑❄"
        "🌴💣🐸💌📍🥀🤢👅💡💩"
        "👐📸👻🤐🤮🎼🥵🚩🍎🍊"
        "👼💍📣🥂"
    )

    def __init__(self):
        # Verify alphabet length
        if len(self._EMOJI_ALPHABET) != 256:
            raise ValueError(f"EMOJI_ALPHABET must contain exactly 256 characters, got {len(self._EMOJI_ALPHABET)}")
        # Create mapping from byte value to emoji character
        self.byte_to_emoji = {i: self._EMOJI_ALPHABET[i] for i in range(256)}
        # Create reverse mapping from emoji character to byte value
        # This matches the approach in js-multiformats and go-multibase
        self.emoji_to_byte = {emoji: byte for byte, emoji in self.byte_to_emoji.items()}

    def encode(self, bytes_) -> bytes:
        """Encode bytes to emoji string.

        :param bytes_: Bytes to encode
        :type bytes_: bytes or str
        :return: UTF-8 encoded emoji string
        :rtype: bytes
        """
        bytes_ = ensure_bytes(bytes_)
        result = []
        for byte_val in bytes_:
            result.append(self.byte_to_emoji[byte_val])
        return "".join(result).encode("utf-8")

    def decode(self, bytes_) -> bytes:
        """Decode emoji string to bytes.

        Decodes character-by-character, matching the behavior of js-multiformats
        and go-multibase reference implementations. Each emoji in the alphabet
        is a single Unicode code point, so we can safely iterate character by
        character.

        :param bytes_: UTF-8 encoded emoji string
        :type bytes_: bytes or str
        :return: Decoded bytes
        :rtype: bytes
        :raises ValueError: if an invalid emoji character is encountered
        """
        bytes_ = ensure_bytes(bytes_, "utf8")
        # Decode UTF-8 to get emoji string
        emoji_str = bytes_.decode("utf-8")
        result = bytearray()
        # Iterate character by character (Python string iteration handles
        # single code point emojis correctly, matching js-multiformats and go-multibase)
        for char in emoji_str:
            if char not in self.emoji_to_byte:
                raise ValueError(f"Non-base256emoji character: {char}")
            result.append(self.emoji_to_byte[char])
        return bytes(result)


class IdentityConverter:
    def encode(self, x):
        return x

    def decode(self, x):
        return x
