from hypothesis import given, settings
from hypothesis import strategies as st

from multibase import ENCODINGS, decode, encode


@given(st.binary(max_size=200))
@settings(max_examples=1000)
def test_decode_never_crashes(data):
    """decode() should raise an exception, not crash."""
    try:
        decode(data)
    except Exception:
        pass  # Any exception is fine, just no crashes


@given(st.text(max_size=200))
@settings(max_examples=1000)
def test_decode_string_never_crashes(data):
    try:
        decode(data)
    except Exception:
        pass


@given(st.binary(min_size=1, max_size=100))
@settings(max_examples=500)
def test_roundtrip_never_crashes(data):
    """encode then decode should never crash."""
    for enc in ENCODINGS:
        try:
            encoded = encode(enc.encoding, data)
            decode(encoded)
        except Exception:
            pass
