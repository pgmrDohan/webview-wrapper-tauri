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
echo "=================================="
echo "All tests passed!"
echo "=================================="
