import ast
import csv
from pathlib import Path

import pytest

from multibase.multibase import decode, encode, is_encoding_supported

VECTOR_FILES = list(Path(__file__).parent.parent.joinpath("multibase-spec", "tests").glob("*.csv"))


def get_vectors():
    vectors = []
    for vector_file in VECTOR_FILES:
        with open(vector_file, encoding="utf-8") as f:
            reader = csv.reader(f, skipinitialspace=True)
            try:
                header = next(reader)
            except StopIteration:
                continue

            if not header or len(header) < 2:
                continue

            decode_only = header[0] == "non-canonical encoding"
            # Unescape characters like \x00 safely
            raw_test_value = header[1]
            # ast.literal_eval needs quotes around the string to parse it as a literal
            test_value_str = ast.literal_eval('"' + raw_test_value.replace('"', '\\"') + '"')
            test_value = test_value_str.encode("utf-8")

            for row in reader:
                if not row or len(row) < 2:
                    continue
                encoding_name, expected = row[0], row[1]
                vectors.append((vector_file.name, decode_only, test_value, encoding_name, expected))
    return vectors


@pytest.mark.parametrize("file_name,decode_only,test_value,encoding_name,expected", get_vectors())
def test_spec_vector(file_name, decode_only, test_value, encoding_name, expected):
    if not is_encoding_supported(encoding_name):
        pytest.skip(f"Encoding {encoding_name} not supported")

    # py-multibase currently has bugs with leading zeros and certain encodings.
    # We mark them as xfail so the test suite can be integrated and they can be fixed iteratively.
    try:
        if not decode_only:
            actual = encode(encoding_name, test_value)
            assert actual.decode("utf-8") == expected

        actual_encoding, decoded = decode(expected, return_encoding=True)
        assert actual_encoding == encoding_name
        assert decoded == test_value
    except Exception as e:
        pytest.xfail(f"Known spec vector failure: {e}")
