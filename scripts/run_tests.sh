#!/usr/bin/env bash
set -e

echo "=================================="
echo "Running all tests"
echo "=================================="

cd "$(dirname "$0")/.."

# Install dependencies if needed
pip3 install -q jinja2 jsonschema 2>/dev/null || true

echo ""
echo "--- Config Validation ---"
python3 scripts/validate_config.py

echo ""
echo "--- Plugin Registry Tests ---"
python3 scripts/tests/test_plugin_registry.py

echo ""
echo "--- Generate Unit Tests ---"
python3 scripts/tests/test_generate.py

echo ""
echo "--- Integration Tests ---"
python3 scripts/tests/test_integration.py

echo ""
echo "--- Restoring default state ---"
git checkout -- src-tauri/Cargo.toml src-tauri/src/lib.rs src-tauri/src/main.rs src-tauri/tauri.conf.json src-tauri/capabilities/default.json src-tauri/gen/ 2>/dev/null || true
rm -f src-tauri/Info.ios.plist

echo ""
echo "=================================="
echo "All tests passed!"
echo "=================================="
