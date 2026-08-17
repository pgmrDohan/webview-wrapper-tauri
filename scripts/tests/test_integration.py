#!/usr/bin/env python3
"""Integration tests for the full generate pipeline."""

import json
import sys
import tempfile
import shutil
from pathlib import Path

# Add scripts dir to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from generate import main as run_generate, load_config, generate_csp, generate_file_associations
from plugin_registry import PLUGIN_REGISTRY, get_plugin, get_enabled_plugins


def test_minimal_config_generation():
    """Test generation with all plugins disabled (default config)."""
    print("Test: Minimal config (no plugins)...")

    # Run generate
    run_generate()

    # Verify Cargo.toml
    cargo_path = PROJECT_ROOT / "src-tauri" / "Cargo.toml"
    assert cargo_path.exists(), "Cargo.toml not generated"
    cargo_content = cargo_path.read_text()
    assert "[package]" in cargo_content
    assert "[dependencies]" in cargo_content
    assert "tauri = " in cargo_content
    # No plugin crates should be present
    assert "tauri-plugin-geolocation" not in cargo_content
    assert "tauri-plugin-clipboard" not in cargo_content

    # Verify lib.rs
    lib_path = PROJECT_ROOT / "src-tauri" / "src" / "lib.rs"
    assert lib_path.exists(), "lib.rs not generated"
    lib_content = lib_path.read_text()
    assert "tauri::Builder::default()" in lib_content
    assert ".run(tauri::generate_context!())" in lib_content

    # Verify tauri.conf.json is valid JSON
    conf_path = PROJECT_ROOT / "src-tauri" / "tauri.conf.json"
    assert conf_path.exists(), "tauri.conf.json not generated"
    conf = json.loads(conf_path.read_text())
    assert conf["productName"] == "My App"
    assert conf["identifier"] == "com.example.myapp"
    assert conf["app"]["withGlobalTauri"] is True

    # Verify capabilities
    caps_path = PROJECT_ROOT / "src-tauri" / "capabilities" / "default.json"
    assert caps_path.exists(), "capabilities not generated"
    caps = json.loads(caps_path.read_text())
    assert "core:default" in caps["permissions"]

    print("  PASSED")


def test_single_plugin_generation():
    """Test generation with one plugin enabled."""
    print("Test: Single plugin (clipboard)...")

    # Temporarily modify config
    plugins_path = PROJECT_ROOT / "config" / "plugins.json"
    original = plugins_path.read_text()

    try:
        config = json.loads(original)
        config["official"]["clipboard"]["enabled"] = True
        plugins_path.write_text(json.dumps(config, indent=2))

        run_generate()

        # Verify Cargo.toml has clipboard
        cargo_content = (PROJECT_ROOT / "src-tauri" / "Cargo.toml").read_text()
        assert "tauri-plugin-clipboard-manager" in cargo_content

        # Verify lib.rs has clipboard init
        lib_content = (PROJECT_ROOT / "src-tauri" / "src" / "lib.rs").read_text()
        assert "clipboard_manager" in lib_content

        # Verify capabilities has clipboard permissions
        caps = json.loads((PROJECT_ROOT / "src-tauri" / "capabilities" / "default.json").read_text())
        assert "clipboard-manager:allow-read-text" in caps["permissions"]

        print("  PASSED")
    finally:
        plugins_path.write_text(original)


def test_multiple_plugins_generation():
    """Test generation with multiple plugins enabled."""
    print("Test: Multiple plugins (geolocation + notification + deep-linking)...")

    plugins_path = PROJECT_ROOT / "config" / "plugins.json"
    original = plugins_path.read_text()

    try:
        config = json.loads(original)
        config["official"]["geolocation"]["enabled"] = True
        config["official"]["notification"]["enabled"] = True
        config["official"]["deep-linking"]["enabled"] = True
        config["official"]["deep-linking"]["options"] = {
            "scheme": "myapp",
            "host": "example.com",
            "pathPrefix": "/open",
            "appLink": True
        }
        plugins_path.write_text(json.dumps(config, indent=2))

        run_generate()

        # Verify Cargo.toml
        cargo_content = (PROJECT_ROOT / "src-tauri" / "Cargo.toml").read_text()
        assert "tauri-plugin-geolocation" in cargo_content
        assert "tauri-plugin-notification" in cargo_content
        assert "tauri-plugin-deep-link" in cargo_content

        # Verify tauri.conf.json has deep-link config
        conf = json.loads((PROJECT_ROOT / "src-tauri" / "tauri.conf.json").read_text())
        assert "deep-link" in conf.get("plugins", {})

        # Verify iOS plist generated
        plist_path = PROJECT_ROOT / "src-tauri" / "Info.ios.plist"
        assert plist_path.exists(), "Info.ios.plist not generated"
        plist_content = plist_path.read_text()
        assert "NSLocationWhenInUseUsageDescription" in plist_content

        # Verify AndroidManifest has permissions
        manifest_path = PROJECT_ROOT / "src-tauri" / "gen" / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
        manifest_content = manifest_path.read_text()
        assert "ACCESS_FINE_LOCATION" in manifest_content

        # Verify entitlements has deep-link
        entitlements_path = PROJECT_ROOT / "src-tauri" / "gen" / "apple" / "webview-wrapper-tauri_iOS" / "webview-wrapper-tauri_iOS.entitlements"
        entitlements_content = entitlements_path.read_text()
        assert "applinks:example.com" in entitlements_content

        print("  PASSED")
    finally:
        plugins_path.write_text(original)


def test_community_plugin_generation():
    """Test generation with a community plugin (git dependency)."""
    print("Test: Community plugin (fcm)...")

    plugins_path = PROJECT_ROOT / "config" / "plugins.json"
    original = plugins_path.read_text()

    try:
        config = json.loads(original)
        config["community"]["fcm"]["enabled"] = True
        plugins_path.write_text(json.dumps(config, indent=2))

        run_generate()

        # Verify Cargo.toml has git dependency
        cargo_content = (PROJECT_ROOT / "src-tauri" / "Cargo.toml").read_text()
        assert "tauri-plugin-fcm" in cargo_content
        assert "git = " in cargo_content
        assert "github.com/srod/tauri-plugin-fcm" in cargo_content

        print("  PASSED")
    finally:
        plugins_path.write_text(original)


def test_file_association_generation():
    """Test file association config generation."""
    print("Test: File associations...")

    fa_path = PROJECT_ROOT / "config" / "file-association.json"
    original = fa_path.read_text()

    try:
        config = {
            "associations": [{
                "ext": ["myfile", "mydata"],
                "mimeType": "application/x-myfile",
                "name": "My File",
                "role": "Editor",
                "rank": "Owner",
                "androidIntentActionFilters": ["view", "send"]
            }]
        }
        fa_path.write_text(json.dumps(config, indent=2))

        run_generate()

        # Verify tauri.conf.json has file associations
        conf = json.loads((PROJECT_ROOT / "src-tauri" / "tauri.conf.json").read_text())
        assert len(conf["bundle"]["fileAssociations"]) == 1
        assert conf["bundle"]["fileAssociations"][0]["ext"] == ["myfile", "mydata"]

        # Verify AndroidManifest has intent filters
        manifest_path = PROJECT_ROOT / "src-tauri" / "gen" / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
        manifest_content = manifest_path.read_text()
        assert "android.intent.action.VIEW" in manifest_content
        assert "android.intent.action.SEND" in manifest_content

        print("  PASSED")
    finally:
        fa_path.write_text(original)


def test_stronghold_special_handling():
    """Test that stronghold uses setup() pattern in lib.rs."""
    print("Test: Stronghold special handling...")

    plugins_path = PROJECT_ROOT / "config" / "plugins.json"
    original = plugins_path.read_text()

    try:
        config = json.loads(original)
        config["official"]["stronghold"]["enabled"] = True
        plugins_path.write_text(json.dumps(config, indent=2))

        run_generate()

        lib_content = (PROJECT_ROOT / "src-tauri" / "src" / "lib.rs").read_text()
        assert "setup" in lib_content or ".setup(" in lib_content
        assert "stronghold" in lib_content
        assert "salt.txt" in lib_content

        print("  PASSED")
    finally:
        plugins_path.write_text(original)


def test_all_plugins_enabled():
    """Test generation with ALL plugins enabled."""
    print("Test: All plugins enabled...")

    plugins_path = PROJECT_ROOT / "config" / "plugins.json"
    original = plugins_path.read_text()

    try:
        config = json.loads(original)
        for category in ["official", "community"]:
            for plugin_id in config[category]:
                config[category][plugin_id]["enabled"] = True
        plugins_path.write_text(json.dumps(config, indent=2))

        run_generate()

        # Verify Cargo.toml has many dependencies
        cargo_content = (PROJECT_ROOT / "src-tauri" / "Cargo.toml").read_text()
        # Should have all 29 plugins
        for plugin_id, plugin_def in PLUGIN_REGISTRY.items():
            assert plugin_def.crate_name in cargo_content, f"Missing crate: {plugin_def.crate_name}"

        # Verify capabilities has many permissions
        caps = json.loads((PROJECT_ROOT / "src-tauri" / "capabilities" / "default.json").read_text())
        assert len(caps["permissions"]) > 10  # Many permissions

        # Verify lib.rs has all plugin inits
        lib_content = (PROJECT_ROOT / "src-tauri" / "src" / "lib.rs").read_text()
        assert ".plugin(" in lib_content

        print("  PASSED")
    finally:
        plugins_path.write_text(original)


def test_cargo_toml_valid_toml():
    """Verify generated Cargo.toml is valid TOML."""
    print("Test: Cargo.toml TOML validity...")

    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("  SKIPPED (no TOML parser available)")
            return

    run_generate()

    cargo_path = PROJECT_ROOT / "src-tauri" / "Cargo.toml"
    with open(cargo_path, "rb") as f:
        parsed = tomllib.load(f)

    assert "package" in parsed
    assert "dependencies" in parsed
    assert parsed["package"]["edition"] == "2021"

    print("  PASSED")


def test_tauri_conf_valid_json():
    """Verify generated tauri.conf.json is valid JSON with required fields."""
    print("Test: tauri.conf.json validity...")

    run_generate()

    conf_path = PROJECT_ROOT / "src-tauri" / "tauri.conf.json"
    conf = json.loads(conf_path.read_text())

    # Required top-level fields
    assert "$schema" in conf
    assert "productName" in conf
    assert "version" in conf
    assert "identifier" in conf
    assert "build" in conf
    assert "app" in conf
    assert "bundle" in conf

    # App config
    assert conf["app"]["withGlobalTauri"] is True
    assert len(conf["app"]["windows"]) == 1
    assert "security" in conf["app"]

    print("  PASSED")


if __name__ == "__main__":
    print("=" * 60)
    print("Running integration tests...")
    print("=" * 60)

    test_minimal_config_generation()
    test_single_plugin_generation()
    test_multiple_plugins_generation()
    test_community_plugin_generation()
    test_file_association_generation()
    test_stronghold_special_handling()
    test_all_plugins_enabled()
    test_cargo_toml_valid_toml()
    test_tauri_conf_valid_json()

    print("\n" + "=" * 60)
    print("All integration tests PASSED!")
    print("=" * 60)
