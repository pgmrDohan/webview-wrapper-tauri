"""
Plugin Registry - Central metadata registry for all supported Tauri plugins.

This module defines the PluginDefinition dataclass and maintains a registry
of all official and community plugins with their crate info, capabilities,
platform requirements, and initialization code.
"""

from dataclasses import dataclass, field


@dataclass
class PluginDefinition:
    id: str
    crate_name: str
    crate_version: str  # semver like "2" or git URL for community
    crate_source: str  # "crates_io" or "git"
    git_url: str = ""  # only for git source
    git_branch: str = ""  # optional branch/tag
    plugin_init: str = ""  # Rust code for .plugin() call
    capabilities: list[str] = field(default_factory=list)
    ios_plist: dict[str, str] = field(default_factory=dict)  # key -> default value
    android_permissions: list[str] = field(default_factory=list)
    android_features: list[str] = field(default_factory=list)
    tauri_conf_plugin_config: dict = field(default_factory=dict)  # goes into tauri.conf.json > plugins
    requires_options: bool = False
    category: str = "official"  # "official" or "community"
    platforms: list[str] = field(default_factory=lambda: ["android", "ios"])


# =============================================================================
# Plugin Registry
# =============================================================================

PLUGIN_REGISTRY: dict[str, PluginDefinition] = {}


def _register(plugin: PluginDefinition) -> None:
    """Register a plugin definition in the global registry."""
    PLUGIN_REGISTRY[plugin.id] = plugin


# -----------------------------------------------------------------------------
# Official Plugins (19)
# -----------------------------------------------------------------------------

_register(PluginDefinition(
    id="barcode-scanner",
    crate_name="tauri-plugin-barcode-scanner",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_barcode_scanner::init()",
    capabilities=["barcode-scanner:default"],
    ios_plist={"NSCameraUsageDescription": "configurable"},
    android_permissions=["android.permission.CAMERA"],
))

_register(PluginDefinition(
    id="clipboard",
    crate_name="tauri-plugin-clipboard-manager",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_clipboard_manager::init()",
    capabilities=[
        "clipboard-manager:allow-read-text",
        "clipboard-manager:allow-write-text",
        "clipboard-manager:allow-clear",
    ],
))

_register(PluginDefinition(
    id="biometric",
    crate_name="tauri-plugin-biometric",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_biometric::init()",
    capabilities=["biometric:default"],
    ios_plist={"NSFaceIDUsageDescription": "configurable"},
))

_register(PluginDefinition(
    id="dialog",
    crate_name="tauri-plugin-dialog",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_dialog::init()",
    capabilities=["dialog:default"],
))

_register(PluginDefinition(
    id="deep-linking",
    crate_name="tauri-plugin-deep-link",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_deep_link::init()",
    capabilities=["deep-link:default", "core:event:default"],
))

_register(PluginDefinition(
    id="store",
    crate_name="tauri-plugin-store",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_store::Builder::default().build()",
    capabilities=["store:default"],
))

_register(PluginDefinition(
    id="persisted-scope",
    crate_name="tauri-plugin-persisted-scope",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_persisted_scope::init()",
    capabilities=[],
))

_register(PluginDefinition(
    id="os-info",
    crate_name="tauri-plugin-os",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_os::init()",
    capabilities=["os:default"],
))

_register(PluginDefinition(
    id="opener",
    crate_name="tauri-plugin-opener",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_opener::init()",
    capabilities=["opener:default"],
))

_register(PluginDefinition(
    id="notification",
    crate_name="tauri-plugin-notification",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_notification::init()",
    capabilities=["notification:default"],
))

_register(PluginDefinition(
    id="nfc",
    crate_name="tauri-plugin-nfc",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_nfc::init()",
    capabilities=["nfc:default"],
    ios_plist={"NFCReaderUsageDescription": "configurable"},
    android_permissions=["android.permission.NFC"],
))

_register(PluginDefinition(
    id="logging",
    crate_name="tauri-plugin-log",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_log::Builder::new().build()",
    capabilities=["log:default"],
))

_register(PluginDefinition(
    id="http-client",
    crate_name="tauri-plugin-http",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_http::init()",
    capabilities=["http:default"],
    android_permissions=["android.permission.INTERNET"],
))

_register(PluginDefinition(
    id="haptics",
    crate_name="tauri-plugin-haptics",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_haptics::init()",
    capabilities=[
        "haptics:allow-vibrate",
        "haptics:allow-impact-feedback",
        "haptics:allow-notification-feedback",
        "haptics:allow-selection-feedback",
    ],
    android_permissions=["android.permission.VIBRATE"],
))

_register(PluginDefinition(
    id="geolocation",
    crate_name="tauri-plugin-geolocation",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_geolocation::init()",
    capabilities=[
        "geolocation:allow-check-permissions",
        "geolocation:allow-request-permissions",
        "geolocation:allow-get-current-position",
        "geolocation:allow-watch-position",
    ],
    ios_plist={"NSLocationWhenInUseUsageDescription": "configurable"},
    android_permissions=[
        "android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.ACCESS_FINE_LOCATION",
    ],
))

_register(PluginDefinition(
    id="file-system",
    crate_name="tauri-plugin-fs",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_fs::init()",
    capabilities=[
        "fs:default",
        "fs:allow-app-read-recursive",
        "fs:allow-app-write-recursive",
    ],
    android_permissions=[
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
    ],
))

_register(PluginDefinition(
    id="stronghold",
    crate_name="tauri-plugin-stronghold",
    crate_version="2",
    crate_source="crates_io",
    plugin_init='tauri_plugin_stronghold::Builder::with_argon2(&app.path().app_local_data_dir().expect("could not resolve app local data path").join("salt.txt")).build()',
    capabilities=["stronghold:default"],
    requires_options=True,
))

_register(PluginDefinition(
    id="websocket",
    crate_name="tauri-plugin-websocket",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_websocket::init()",
    capabilities=["websocket:default"],
))

_register(PluginDefinition(
    id="upload",
    crate_name="tauri-plugin-upload",
    crate_version="2",
    crate_source="crates_io",
    plugin_init="tauri_plugin_upload::init()",
    capabilities=["upload:default"],
))

# -----------------------------------------------------------------------------
# Community Plugins (10)
# -----------------------------------------------------------------------------

_register(PluginDefinition(
    id="fcm",
    crate_name="tauri-plugin-fcm",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/srod/tauri-plugin-fcm",
    plugin_init="tauri_plugin_fcm::init()",
    category="community",
))

_register(PluginDefinition(
    id="blec",
    crate_name="tauri-plugin-blec",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/MnlPhlp/tauri-plugin-blec",
    plugin_init="tauri_plugin_blec::init()",
    capabilities=[],
    ios_plist={"NSBluetoothAlwaysUsageDescription": "configurable"},
    android_permissions=[
        "android.permission.BLUETOOTH",
        "android.permission.BLUETOOTH_ADMIN",
        "android.permission.BLUETOOTH_CONNECT",
        "android.permission.BLUETOOTH_SCAN",
    ],
    category="community",
))

_register(PluginDefinition(
    id="drpc",
    crate_name="tauri-plugin-drpc",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/smokingplaya/tauri-plugin-drpc",
    plugin_init="tauri_plugin_drpc::init()",
    category="community",
))

_register(PluginDefinition(
    id="prevent-default",
    crate_name="tauri-plugin-prevent-default",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/ferreira-tb/tauri-plugin-prevent-default",
    plugin_init="tauri_plugin_prevent_default::init()",
    category="community",
))

_register(PluginDefinition(
    id="ios-photos",
    crate_name="tauri-plugin-ios-photos",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/Gbyte-Group/tauri-plugin-ios-photos",
    plugin_init="tauri_plugin_ios_photos::init()",
    ios_plist={"NSPhotoLibraryUsageDescription": "configurable"},
    category="community",
))

_register(PluginDefinition(
    id="keep-screen-on",
    crate_name="tauri-plugin-keep-screen-on",
    crate_version="",
    crate_source="git",
    git_url="https://gitlab.com/cristofa/tauri-plugin-keep-screen-on",
    plugin_init="tauri_plugin_keep_screen_on::init()",
    android_permissions=["android.permission.WAKE_LOCK"],
    category="community",
))

_register(PluginDefinition(
    id="iap",
    crate_name="tauri-plugin-iap",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/Choochmeque/tauri-plugin-iap",
    plugin_init="tauri_plugin_iap::init()",
    android_permissions=["com.android.vending.BILLING"],
    category="community",
))

_register(PluginDefinition(
    id="sharesheet",
    crate_name="tauri-plugin-sharesheet",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/buildyourwebapp/tauri-plugin-sharesheet",
    plugin_init="tauri_plugin_sharesheet::init()",
    category="community",
))

_register(PluginDefinition(
    id="udp",
    crate_name="tauri-plugin-udp",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/kuyoonjo/tauri-plugin-udp",
    plugin_init="tauri_plugin_udp::init()",
    android_permissions=["android.permission.INTERNET"],
    category="community",
))

_register(PluginDefinition(
    id="android-battery-optimization",
    crate_name="tauri-plugin-android-battery-optimization",
    crate_version="",
    crate_source="git",
    git_url="https://github.com/NeoHuncho/tauri-plugin-android-battery-optimization",
    plugin_init="tauri_plugin_android_battery_optimization::init()",
    android_permissions=["android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"],
    category="community",
))


# =============================================================================
# Helper Functions
# =============================================================================

def get_plugin(plugin_id: str) -> PluginDefinition | None:
    """Get a plugin definition by ID."""
    return PLUGIN_REGISTRY.get(plugin_id)


def get_enabled_plugins(config: dict) -> list[PluginDefinition]:
    """Get list of enabled plugins from a plugins.json config dict."""
    enabled = []
    for category in ["official", "community"]:
        if category in config:
            for plugin_id, plugin_config in config[category].items():
                if plugin_config.get("enabled", False):
                    plugin = get_plugin(plugin_id)
                    if plugin:
                        enabled.append(plugin)
    return enabled


def get_all_capabilities(plugins: list[PluginDefinition]) -> list[str]:
    """Collect all capabilities from a list of plugins."""
    caps = ["core:default"]
    for plugin in plugins:
        caps.extend(plugin.capabilities)
    return list(dict.fromkeys(caps))  # deduplicate preserving order


def get_ios_plist_entries(plugins: list[PluginDefinition], config: dict) -> dict[str, str]:
    """Get iOS plist entries, resolving 'configurable' values from plugin options."""
    entries = {}
    for plugin in plugins:
        for key, default_value in plugin.ios_plist.items():
            if default_value == "configurable":
                # Try to get from config options
                for category in ["official", "community"]:
                    if category in config and plugin.id in config[category]:
                        usage_desc = config[category][plugin.id].get("options", {}).get("usage_description", "")
                        if usage_desc:
                            entries[key] = usage_desc
                        else:
                            entries[key] = f"This app needs {key.replace('NS', '').replace('UsageDescription', '')}"
            else:
                entries[key] = default_value
    return entries


def get_android_permissions(plugins: list[PluginDefinition]) -> list[str]:
    """Collect all Android permissions from enabled plugins."""
    perms = ["android.permission.INTERNET"]  # always needed for webview
    for plugin in plugins:
        perms.extend(plugin.android_permissions)
    return list(dict.fromkeys(perms))  # deduplicate preserving order
