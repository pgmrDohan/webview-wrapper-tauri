#!/usr/bin/env python3
"""Tests for the generate script."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate import generate_csp, generate_plugins_config, generate_file_associations, generate_http_capabilities, get_deep_link_options
from plugin_registry import get_plugin, get_enabled_plugins, get_all_capabilities


def test_generate_csp_with_api_url():
    """CSP should include both websiteUrl and apiUrl in connect-src."""
    config = {"websiteUrl": "https://myapp.com", "apiUrl": "https://api.myapp.com"}
    csp = generate_csp(config)
    assert "https://myapp.com" in csp
    assert "https://api.myapp.com" in csp
    assert "connect-src" in csp
    assert "default-src" in csp
    assert "script-src" in csp


def test_generate_csp_without_api_url():
    """CSP should work without apiUrl."""
    config = {"websiteUrl": "https://myapp.com", "apiUrl": ""}
    csp = generate_csp(config)
    assert "https://myapp.com" in csp
    assert "connect-src 'self' https://myapp.com" in csp


def test_generate_file_associations():
    """File associations should be generated correctly."""
    config = {
        "associations": [
            {"ext": ["pdf", "doc"], "mimeType": "application/pdf", "name": "Document", "role": "Viewer"}
        ]
    }
    result = generate_file_associations(config)
    assert len(result) == 1
    assert result[0]["ext"] == ["pdf", "doc"]
    assert result[0]["mimeType"] == "application/pdf"
    assert result[0]["role"] == "Viewer"


def test_generate_empty_file_associations():
    """Empty associations should return empty list."""
    config = {"associations": []}
    result = generate_file_associations(config)
    assert result == []


def test_generate_file_associations_string_ext():
    """Single string ext should be wrapped in a list."""
    config = {
        "associations": [
            {"ext": "pdf", "mimeType": "application/pdf"}
        ]
    }
    result = generate_file_associations(config)
    assert result[0]["ext"] == ["pdf"]


def test_generate_plugins_config_no_deep_link():
    """No deep-link config when plugin is not enabled."""
    plugins_config = {
        "official": {"clipboard": {"enabled": True, "options": {}}},
        "community": {}
    }
    enabled = get_enabled_plugins(plugins_config)
    result = generate_plugins_config(enabled, plugins_config, {})
    assert result == {}


def test_generate_plugins_config_deep_link():
    """Deep-link config should be generated when deep-linking is enabled with options."""
    plugins_config = {
        "official": {
            "deep-linking": {
                "enabled": True,
                "options": {"scheme": "myapp", "host": "open.myapp.com", "pathPrefix": "/link", "appLink": True}
            }
        },
        "community": {}
    }
    enabled = get_enabled_plugins(plugins_config)
    result = generate_plugins_config(enabled, plugins_config, {})
    assert "deep-link" in result
    assert result["deep-link"]["mobile"][0]["scheme"] == ["myapp"]
    assert result["deep-link"]["mobile"][0]["host"] == "open.myapp.com"


def test_generate_http_capabilities_with_urls():
    """HTTP capabilities should include URL scope when allowed_urls specified."""
    plugins_config = {
        "official": {
            "http-client": {"enabled": True, "options": {"allowed_urls": ["https://api.example.com", "https://cdn.example.com"]}}
        },
        "community": {}
    }
    result = generate_http_capabilities(plugins_config)
    assert len(result) == 1
    assert result[0]["identifier"] == "http:default"
    assert len(result[0]["allow"]) == 2


def test_generate_http_capabilities_no_urls():
    """HTTP capabilities should fallback to simple string when no URLs specified."""
    plugins_config = {
        "official": {
            "http-client": {"enabled": True, "options": {"allowed_urls": []}}
        },
        "community": {}
    }
    result = generate_http_capabilities(plugins_config)
    assert result == ["http:default"]


def test_get_all_capabilities_includes_core():
    """Capabilities should always include core:default."""
    capabilities = get_all_capabilities([])
    assert "core:default" in capabilities


def test_get_all_capabilities_with_plugins():
    """Capabilities should include plugin-specific permissions."""
    clipboard = get_plugin("clipboard")
    capabilities = get_all_capabilities([clipboard])
    assert "core:default" in capabilities
    assert "clipboard-manager:allow-read-text" in capabilities
    assert "clipboard-manager:allow-write-text" in capabilities


def test_deep_link_options_enabled():
    """Deep link options should be extracted when deep-linking is enabled."""
    config = {
        "official": {
            "deep-linking": {"enabled": True, "options": {"scheme": "myapp", "host": "example.com", "pathPrefix": "/open", "appLink": True}}
        },
        "community": {}
    }
    opts = get_deep_link_options(config)
    assert opts["scheme"] == "myapp"
    assert opts["host"] == "example.com"
    assert opts["pathPrefix"] == "/open"
    assert opts["appLink"] is True


def test_deep_link_options_disabled():
    """Deep link options should return empty dict when plugin is disabled."""
    config = {
        "official": {
            "deep-linking": {"enabled": False, "options": {"scheme": "myapp", "host": "example.com"}}
        },
        "community": {}
    }
    opts = get_deep_link_options(config)
    assert opts == {}


def test_deep_link_options_missing():
    """Deep link options should return empty dict when plugin is not in config."""
    config = {
        "official": {"clipboard": {"enabled": True, "options": {}}},
        "community": {}
    }
    opts = get_deep_link_options(config)
    assert opts == {}


def test_platform_generation_android_features():
    """Android features should be populated based on enabled plugins."""
    from plugin_registry import get_android_permissions
    plugins_config = {
        "official": {
            "nfc": {"enabled": True, "options": {"usage_description": "Read NFC tags"}},
            "geolocation": {"enabled": True, "options": {"usage_description": "Location access"}}
        },
        "community": {}
    }
    enabled = get_enabled_plugins(plugins_config)
    android_perms = get_android_permissions(enabled)

    # Check that NFC and location permissions are present
    assert "android.permission.NFC" in android_perms
    assert "android.permission.ACCESS_FINE_LOCATION" in android_perms
    assert "android.permission.ACCESS_COARSE_LOCATION" in android_perms
    assert "android.permission.INTERNET" in android_perms

    # Check feature detection logic
    has_nfc = any(p.id == "nfc" for p in enabled)
    has_geo = any(p.id == "geolocation" for p in enabled)
    assert has_nfc is True
    assert has_geo is True

    android_features = []
    if has_nfc:
        android_features.append("android.hardware.nfc")
    if has_geo:
        android_features.append("android.hardware.location.gps")
    assert "android.hardware.nfc" in android_features
    assert "android.hardware.location.gps" in android_features


def test_platform_generation_ios_plist_entries():
    """iOS plist entries should include usage descriptions from enabled plugins."""
    from plugin_registry import get_ios_plist_entries
    plugins_config = {
        "official": {
            "geolocation": {"enabled": True, "options": {"usage_description": "We need your location"}},
            "nfc": {"enabled": True, "options": {"usage_description": "Read NFC tags"}}
        },
        "community": {}
    }
    enabled = get_enabled_plugins(plugins_config)
    entries = get_ios_plist_entries(enabled, plugins_config)
    assert "NSLocationWhenInUseUsageDescription" in entries
    assert entries["NSLocationWhenInUseUsageDescription"] == "We need your location"
    assert "NFCReaderUsageDescription" in entries
    assert entries["NFCReaderUsageDescription"] == "Read NFC tags"


if __name__ == "__main__":
    test_generate_csp_with_api_url()
    test_generate_csp_without_api_url()
    test_generate_file_associations()
    test_generate_empty_file_associations()
    test_generate_file_associations_string_ext()
    test_generate_plugins_config_no_deep_link()
    test_generate_plugins_config_deep_link()
    test_generate_http_capabilities_with_urls()
    test_generate_http_capabilities_no_urls()
    test_get_all_capabilities_includes_core()
    test_get_all_capabilities_with_plugins()
    test_deep_link_options_enabled()
    test_deep_link_options_disabled()
    test_deep_link_options_missing()
    test_platform_generation_android_features()
    test_platform_generation_ios_plist_entries()
    print("All generate tests passed!")
