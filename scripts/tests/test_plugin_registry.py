import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from plugin_registry import (
    PLUGIN_REGISTRY, get_plugin, get_enabled_plugins,
    get_all_capabilities, get_ios_plist_entries, get_android_permissions
)


def test_registry_has_all_plugins():
    assert len(PLUGIN_REGISTRY) == 29  # 19 official + 10 community


def test_get_plugin():
    plugin = get_plugin("geolocation")
    assert plugin is not None
    assert plugin.crate_name == "tauri-plugin-geolocation"
    assert "NSLocationWhenInUseUsageDescription" in plugin.ios_plist


def test_get_enabled_plugins():
    config = {
        "official": {
            "clipboard": {"enabled": True, "options": {}},
            "haptics": {"enabled": False, "options": {}},
        },
        "community": {
            "fcm": {"enabled": True, "options": {"project_id": "test"}},
        }
    }
    enabled = get_enabled_plugins(config)
    assert len(enabled) == 2
    ids = [p.id for p in enabled]
    assert "clipboard" in ids
    assert "fcm" in ids


def test_get_all_capabilities():
    plugins = [get_plugin("clipboard"), get_plugin("haptics")]
    caps = get_all_capabilities(plugins)
    assert "core:default" in caps
    assert "clipboard-manager:allow-read-text" in caps


def test_get_android_permissions():
    plugins = [get_plugin("geolocation"), get_plugin("haptics")]
    perms = get_android_permissions(plugins)
    assert "android.permission.INTERNET" in perms
    assert "android.permission.ACCESS_FINE_LOCATION" in perms
    assert "android.permission.VIBRATE" in perms


if __name__ == "__main__":
    test_registry_has_all_plugins()
    test_get_plugin()
    test_get_enabled_plugins()
    test_get_all_capabilities()
    test_get_android_permissions()
    print("All tests passed!")
