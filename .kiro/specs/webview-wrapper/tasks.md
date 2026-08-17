# WebView Wrapper Tauri - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a universal Tauri v2 WebView wrapper template that web developers can fork and configure via GitHub Actions to produce Android/iOS native apps with selected native plugin capabilities.

**Architecture:** Config-driven code generation. `config/` JSON files define what plugins/settings are active. `scripts/generate.py` reads config and generates all `src-tauri/` files at build time. GitHub Actions workflows provide the UI for developers to set config values without touching code.

**Tech Stack:** Python 3.11+ (build scripts), Jinja2 (templates), Rust/Tauri v2 (app framework), GitHub Actions (CI/CD)

**Spec:** `.kiro/specs/webview-wrapper/design.md`

## Global Constraints

- Target platforms: Android + iOS only
- Tauri v2 (latest stable)
- Python 3.11+ for build scripts
- GitHub Actions `workflow_dispatch` max 25 inputs per workflow
- All generated files must produce a valid, buildable Tauri project
- `window.__TAURI__` (withGlobalTauri: true) for IPC
- No code modification required by the end-user developer

---

## Task 1: Project Structure & Config Schemas [foundation]

- id: 1
- depends_on: []

Set up the project directory structure, config JSON schemas, and default config files.

### Sub-tasks:
- 1.1: Create directory structure (`config/`, `config/schemas/`, `scripts/`, `templates/`, `docs/`, `docs/plugins/`, `.github/workflows/`)
- 1.2: Create `config/app.json` with default values (productName, identifier, version, websiteUrl, apiUrl, userAgent, backgroundColor)
- 1.3: Create `config/plugins.json` with all plugins listed (all disabled by default) with their options structure
- 1.4: Create `config/file-association.json` with empty associations array
- 1.5: Create `config/signing.json` with placeholder structure
- 1.6: Create JSON Schema files in `config/schemas/` for validation (app.schema.json, plugins.schema.json, file-association.schema.json, signing.schema.json)
- 1.7: Create `scripts/validate_config.py` that validates all config files against their schemas
- 1.8: Update `.gitignore` to exclude build artifacts but keep config/

## Task 2: Plugin Registry [foundation]

- id: 2
- depends_on: [1]

Create the central plugin registry that maps each plugin to its crate info, capabilities, platform-specific requirements, and initialization code.

### Sub-tasks:
- 2.1: Create `scripts/plugin_registry.py` with the PluginDefinition dataclass
- 2.2: Register all 19 official plugins with: crate_name, crate_version, plugin_init code, capabilities list, ios_plist entries, android_permissions, android_features, tauri_conf_plugin_config, requires_options flag
- 2.3: Register all 10 community plugins with: git_url, branch/tag, plugin_init code, capabilities, ios/android requirements
- 2.4: Add helper functions: get_plugin(id), get_enabled_plugins(config), get_all_capabilities(plugins), get_ios_plist_entries(plugins), get_android_permissions(plugins)
- 2.5: Add unit tests in `scripts/tests/test_plugin_registry.py`

## Task 3: Code Generation Script - Core [core]

- id: 3
- depends_on: [2]

Build the main generate.py script that reads config and generates all Tauri project files using Jinja2 templates.

### Sub-tasks:
- 3.1: Create `scripts/requirements.txt` with jinja2, jsonschema dependencies
- 3.2: Create Jinja2 templates: `templates/Cargo.toml.j2`, `templates/lib.rs.j2`, `templates/tauri.conf.json.j2`, `templates/capabilities.json.j2`
- 3.3: Create `scripts/generate.py` main entry point that: loads config, validates, loads registry, renders templates, writes output files
- 3.4: Implement Cargo.toml generation (base dependencies + conditional plugin dependencies from registry)
- 3.5: Implement lib.rs generation (plugin initialization chain from registry)
- 3.6: Implement tauri.conf.json generation (app settings + plugin configs + file associations + CSP)
- 3.7: Implement capabilities/default.json generation (core permissions + plugin permissions)
- 3.8: Add unit tests in `scripts/tests/test_generate.py` for each generation function

## Task 4: Code Generation - Platform-Specific Files [core]

- id: 4
- depends_on: [3]

Extend the generate script to produce iOS and Android platform-specific configuration files.

### Sub-tasks:
- 4.1: Create `templates/Info.ios.plist.j2` for iOS usage descriptions
- 4.2: Implement iOS plist generation (merge usage descriptions from enabled plugins into existing Info.plist)
- 4.3: Implement iOS entitlements generation (NFC capability, Associated Domains for deep-link)
- 4.4: Create `templates/AndroidManifest.xml.j2` for Android permissions and intent filters
- 4.5: Implement AndroidManifest.xml generation (merge permissions, features, intent-filters from enabled plugins)
- 4.6: Implement deep-link specific config generation (tauri.conf.json plugins.deep-link section)
- 4.7: Implement file-association config merging into tauri.conf.json bundle section
- 4.8: Add tests for platform-specific generation with multiple plugin combinations

## Task 5: Setup Common Workflow [workflows]

- id: 5
- depends_on: [1]

Create the workflow for basic app configuration (name, URL, identifier, etc).

### Sub-tasks:
- 5.1: Create `.github/workflows/setup-common.yml` with workflow_dispatch inputs (app_name, identifier, version, website_url, api_url, user_agent, background_color)
- 5.2: Implement workflow job that reads inputs, updates `config/app.json`, and commits
- 5.3: Add input validation step (URL format, identifier format com.xxx.xxx)
- 5.4: Add commit and push step with proper git configuration

## Task 6: Setup Plugins Workflows [workflows]

- id: 6
- depends_on: [1]

Create workflows for plugin selection (official + community split due to input limits).

### Sub-tasks:
- 6.1: Create `.github/workflows/setup-plugins.yml` with boolean inputs for each official plugin (19 toggles)
- 6.2: Create `.github/workflows/setup-plugins-community.yml` with boolean inputs for each community plugin (10 toggles)
- 6.3: Implement workflow jobs that update `config/plugins.json` enabled flags and commit
- 6.4: Create `.github/workflows/setup-plugin-options.yml` with string inputs for plugin-specific options (deep_link_scheme, deep_link_host, http_allowed_urls, drpc_app_id, fcm_project_id, geolocation_description, biometric_description, camera_description, nfc_description, iap_product_ids, blec_description, photo_description)
- 6.5: Implement options workflow that merges input values into corresponding plugin options in `config/plugins.json`

## Task 7: Setup File Association & Signing Workflows [workflows]

- id: 7
- depends_on: [1]

Create workflows for file association configuration and signing setup.

### Sub-tasks:
- 7.1: Create `.github/workflows/setup-file-association.yml` with inputs (extensions, mime_type, name, description, role, rank, android_intent_actions)
- 7.2: Implement file association workflow that generates/updates `config/file-association.json`
- 7.3: Create `.github/workflows/setup-signing.yml` with inputs (android_key_alias, ios_team_id)
- 7.4: Implement signing workflow that updates `config/signing.json` and validates required secrets exist
- 7.5: Add validation step that checks if referenced GitHub Secrets are accessible (using secrets context)

## Task 8: Build Workflow [workflows]

- id: 8
- depends_on: [3, 4, 5, 6, 7]

Create the main build workflow that generates source files and builds APK/IPA.

### Sub-tasks:
- 8.1: Create `.github/workflows/build.yml` with workflow_dispatch inputs (version_tag, build_android, build_ios)
- 8.2: Implement Android build job: checkout → install Python deps → run generate.py → setup Rust toolchain → setup Android SDK/NDK → run `cargo tauri android build` → sign APK → upload to Release
- 8.3: Implement iOS build job: checkout → install Python deps → run generate.py → setup Rust toolchain → setup Xcode → run `cargo tauri ios build` → sign IPA → upload to Release
- 8.4: Add GitHub Release creation step with version tag and build artifacts
- 8.5: Add error handling and build log artifact upload on failure

## Task 9: Documentation - Getting Started & Architecture [docs]

- id: 9
- depends_on: [5, 6, 7, 8]

Write the main documentation that guides developers through the entire process.

### Sub-tasks:
- 9.1: Create `docs/README.md` with project overview, supported plugins list, architecture diagram
- 9.2: Create `docs/getting-started.md` with step-by-step guide (Fork → Configure → Build)
- 9.3: Create `docs/signing.md` with Android keystore generation guide and iOS certificate guide
- 9.4: Create `docs/deep-linking.md` with server-side setup guide (.well-known files)
- 9.5: Create `docs/file-association.md` with file association configuration guide
- 9.6: Create `docs/troubleshooting.md` with common issues and solutions
- 9.7: Update root `README.md` with project introduction and quick-start

## Task 10: Plugin Documentation - Official Plugins [docs]

- id: 10
- depends_on: [2]

Write per-plugin documentation showing JS usage code for each official plugin.

### Sub-tasks:
- 10.1: Create docs for simple plugins: `docs/plugins/clipboard.md`, `docs/plugins/haptics.md`, `docs/plugins/os-info.md`, `docs/plugins/dialog.md`, `docs/plugins/store.md`, `docs/plugins/logging.md`, `docs/plugins/opener.md`
- 10.2: Create docs for iOS-config plugins: `docs/plugins/barcode-scanner.md`, `docs/plugins/biometric.md`, `docs/plugins/geolocation.md`, `docs/plugins/nfc.md`
- 10.3: Create docs for options-required plugins: `docs/plugins/deep-linking.md`, `docs/plugins/http-client.md`, `docs/plugins/notification.md`, `docs/plugins/file-system.md`, `docs/plugins/websocket.md`, `docs/plugins/upload.md`, `docs/plugins/stronghold.md`, `docs/plugins/persisted-scope.md`

## Task 11: Plugin Documentation - Community Plugins [docs]

- id: 11
- depends_on: [2]

Write per-plugin documentation for community plugins including API integration guides.

### Sub-tasks:
- 11.1: Create `docs/plugins/fcm.md` with full FCM integration guide (google-services.json, token registration API spec, push notification handling)
- 11.2: Create `docs/plugins/blec.md` (BLE communication guide)
- 11.3: Create `docs/plugins/drpc.md` (Discord Rich Presence setup)
- 11.4: Create `docs/plugins/prevent-default.md`, `docs/plugins/keep-screen-on.md`, `docs/plugins/sharesheet.md`, `docs/plugins/udp.md`, `docs/plugins/android-battery-optimization.md`
- 11.5: Create `docs/plugins/ios-photos.md` (iOS photo library access)
- 11.6: Create `docs/plugins/iap.md` (In-App Purchase integration guide with product ID setup)

## Task 12: Integration Testing & Validation [testing]

- id: 12
- depends_on: [3, 4, 8]

Create comprehensive tests that validate the entire pipeline from config to generated output.

### Sub-tasks:
- 12.1: Create `scripts/tests/test_integration.py` with test scenarios: minimal config (no plugins), single plugin, all plugins enabled
- 12.2: Add Cargo.toml syntax validation (parse generated TOML)
- 12.3: Add tauri.conf.json validation (parse JSON, check required fields)
- 12.4: Add capabilities.json schema validation
- 12.5: Create `scripts/tests/fixtures/` with sample config combinations
- 12.6: Add GitHub Actions workflow syntax validation using actionlint (if available) or YAML schema check
- 12.7: Create a `Makefile` or `scripts/run_tests.sh` for running all tests

## Task 13: Final Cleanup & Polish [polish]

- id: 13
- depends_on: [9, 10, 11, 12]

Final cleanup, remove boilerplate, ensure repo is fork-ready.

### Sub-tasks:
- 13.1: Remove boilerplate code from `src-tauri/src/lib.rs` (greet function)
- 13.2: Update `src-tauri/tauri.conf.json` to clean default state (remove example.com placeholders since generate.py handles this)
- 13.3: Update `.gitignore` with final patterns
- 13.4: Ensure all documentation links are valid (no broken references)
- 13.5: Add LICENSE file review (ensure it's appropriate for template usage)
- 13.6: Final README.md with badges, feature list, supported plugins table, and quick-start
