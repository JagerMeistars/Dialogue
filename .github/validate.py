#!/usr/bin/env python3
"""CI validation: scan all package JSON and check pack.mcmeta fields."""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JSON_GLOBS = [
    "datapack/**/*.json",
    "resourcepack/**/*.json",
    "mcfont/**/*.json",
]

MCMETA_FILES = [
    "datapack/pack.mcmeta",
    "resourcepack/pack.mcmeta",
]

REQUIRED_PACK_FIELDS = ["pack_format", "min_format", "max_format"]


def scan_json():
    files = []
    for pattern in JSON_GLOBS:
        files.extend(glob.glob(os.path.join(ROOT, pattern), recursive=True))
    files = sorted(set(files))
    errors = []
    for path in files:
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                json.load(fh)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
            errors.append(f"{rel}: {exc}")
    print(f"Scanned {len(files)} JSON file(s).")
    return errors


def check_mcmeta():
    errors = []
    for rel in MCMETA_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            errors.append(f"{rel}: missing")
            continue
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
            errors.append(f"{rel}: {exc}")
            continue
        pack = data.get("pack")
        if not isinstance(pack, dict):
            errors.append(f"{rel}: missing 'pack' object")
            continue
        for field in REQUIRED_PACK_FIELDS:
            if field not in pack:
                errors.append(f"{rel}: missing field '{field}'")
        print(f"Checked {rel}: pack fields OK"
              if all(f in pack for f in REQUIRED_PACK_FIELDS)
              else f"Checked {rel}: has issues")
    return errors


def main():
    errors = scan_json() + check_mcmeta()
    if errors:
        print("\nVALIDATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print("\nAll validations passed.")


if __name__ == "__main__":
    main()
