import pytest

from multibase import ENCODINGS, decode, encode

BENCH_DATA = b"Decentralize everything!!!"


@pytest.mark.benchmark
@pytest.mark.parametrize("encoding_info", ENCODINGS, ids=lambda e: e.encoding)
def test_bench_encode(benchmark, encoding_info):
    benchmark(encode, encoding_info.encoding, BENCH_DATA)


@pytest.mark.benchmark
@pytest.mark.parametrize("encoding_info", ENCODINGS, ids=lambda e: e.encoding)
def test_bench_decode(benchmark, encoding_info):
    encoded = encode(encoding_info.encoding, BENCH_DATA)
    benchmark(decode, encoded)


@pytest.mark.benchmark
@pytest.mark.parametrize("encoding_info", ENCODINGS, ids=lambda e: e.encoding)
def test_bench_roundtrip(benchmark, encoding_info):
    def roundtrip():
        return decode(encode(encoding_info.encoding, BENCH_DATA))

    benchmark(roundtrip)
