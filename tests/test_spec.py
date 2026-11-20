import csv
from pathlib import Path

from multibase.multibase import ENCODINGS


def test_spec_encodings():
    spec_path = Path(__file__).parent.parent / "multibase-spec" / "multibase.csv"
    if not spec_path.exists():
        # Fallback if the submodule is not checked out locally
        return

    spec_encodings = {}
    with open(spec_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if not row:
                continue
            row = [col.strip() for col in row]
            if len(row) >= 5:
                unicode_str, character, encoding_name, description, status = row[:5]
                if encoding_name == "none":
                    continue
                spec_encodings[encoding_name] = {
                    "character": character,
                    "status": status,
                }

    supported_names = set()
    for enc in ENCODINGS:
        if enc.encoding == "identity":
            continue

        assert enc.encoding in spec_encodings, f"Encoding '{enc.encoding}' not in spec"
        spec_char = spec_encodings[enc.encoding]["character"]

        assert enc.code.decode("utf-8") == spec_char, (
            f"Prefix mismatch for '{enc.encoding}': expected '{spec_char}', got '{enc.code.decode('utf-8')}'"
        )

        supported_names.add(enc.encoding)

    for name, data in spec_encodings.items():
        if data["status"] == "final":
            assert name in supported_names, f"Missing final encoding from spec: '{name}'"
