#!/usr/bin/env python3
"""Tests for the generate script."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate import generate_csp, generate_plugins_config, generate_file_associations, generate_http_capabilities
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
    print("All generate tests passed!")
