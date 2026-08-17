#!/usr/bin/env python3
"""Validate all config files against their JSON schemas."""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("Error: jsonschema package not installed.")
    print("Install it with: pip install jsonschema")
    sys.exit(1)

# Project root is one level up from scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SCHEMAS_DIR = CONFIG_DIR / "schemas"

# Mapping of config files to their schema files
CONFIG_SCHEMA_MAP = {
    "app.json": "app.schema.json",
    "plugins.json": "plugins.schema.json",
    "file-association.json": "file-association.schema.json",
    "signing.json": "signing.schema.json",
}


def load_json(path: Path) -> dict:
    """Load and parse a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_config(config_name: str, schema_name: str) -> list[str]:
    """Validate a config file against its schema. Returns list of errors."""
    config_path = CONFIG_DIR / config_name
    schema_path = SCHEMAS_DIR / schema_name
    errors = []

    if not config_path.exists():
        errors.append(f"Config file not found: {config_path}")
        return errors

    if not schema_path.exists():
        errors.append(f"Schema file not found: {schema_path}")
        return errors

    try:
        config = load_json(config_path)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in {config_name}: {e}")
        return errors

    try:
        schema = load_json(schema_path)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in schema {schema_name}: {e}")
        return errors

    # Validate config against schema
    validator = Draft7Validator(schema)
    for error in validator.iter_errors(config):
        path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "(root)"
        errors.append(f"  [{path}] {error.message}")

    return errors


def main():
    """Run validation for all config files."""
    print("Validating config files...")
    print("=" * 50)

    all_valid = True

    for config_name, schema_name in CONFIG_SCHEMA_MAP.items():
        errors = validate_config(config_name, schema_name)

        if errors:
            print(f"\n FAIL: {config_name}")
            for error in errors:
                print(f"  {error}")
            all_valid = False
        else:
            print(f"\n PASS: {config_name}")

    print("\n" + "=" * 50)

    if all_valid:
        print("All config files are valid.")
        sys.exit(0)
    else:
        print("Validation failed. Please fix the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
