.PHONY: test generate validate clean

# Run all tests
test:
	@bash scripts/run_tests.sh

# Generate project files from config
generate:
	@python3 scripts/generate.py

# Validate config files
validate:
	@python3 scripts/validate_config.py

# Install Python dependencies
setup:
	@pip3 install -r scripts/requirements.txt

# Clean generated files (restore to template state)
clean:
	@echo "Restoring src-tauri to default state..."
	@git checkout -- src-tauri/Cargo.toml src-tauri/src/lib.rs src-tauri/src/main.rs src-tauri/tauri.conf.json src-tauri/capabilities/default.json 2>/dev/null || true
	@rm -f src-tauri/Info.ios.plist
