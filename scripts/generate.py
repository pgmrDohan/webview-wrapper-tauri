#!/usr/bin/env python3
"""
Generate Tauri project files from config.

Reads config/*.json files, validates them, loads the plugin registry,
and renders Jinja2 templates into src-tauri/ project files.
"""

import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# Add scripts dir to path
SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from plugin_registry import get_enabled_plugins, get_all_capabilities, get_plugin, get_ios_plist_entries, get_android_permissions

CONFIG_DIR = PROJECT_ROOT / "config"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
SRC_TAURI_DIR = PROJECT_ROOT / "src-tauri"
CAPABILITIES_DIR = SRC_TAURI_DIR / "capabilities"


def load_config(name: str) -> dict:
    """Load a config JSON file."""
    path = CONFIG_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_csp(app_config: dict) -> str:
    """Generate Content Security Policy from app config."""
    website_url = app_config.get("websiteUrl", "https://example.com")
    api_url = app_config.get("apiUrl", "")

    connect_src = f"'self' {website_url}"
    if api_url:
        connect_src += f" {api_url}"

    csp = (
        f"default-src 'self' {website_url}; "
        f"script-src 'self' 'unsafe-inline' 'unsafe-eval' {website_url}; "
        f"style-src 'self' 'unsafe-inline' {website_url}; "
        f"img-src 'self' asset: https: data: blob:; "
        f"connect-src {connect_src} https: wss:; "
        f"font-src 'self' {website_url} https: data:; "
        f"media-src 'self' {website_url} https: blob:"
    )
    return csp


def generate_plugins_config(plugins, plugins_config: dict, app_config: dict) -> dict:
    """Generate the plugins section of tauri.conf.json."""
    conf = {}

    for plugin in plugins:
        if plugin.id == "deep-linking":
            # Get deep-link config from plugins.json options
            for category in ["official", "community"]:
                if category in plugins_config and "deep-linking" in plugins_config[category]:
                    opts = plugins_config[category]["deep-linking"].get("options", {})
                    scheme = opts.get("scheme", "")
                    host = opts.get("host", "")
                    path_prefix = opts.get("pathPrefix", "")
                    app_link = opts.get("appLink", True)

                    if scheme or host:
                        mobile_entry = {}
                        if scheme:
                            mobile_entry["scheme"] = [scheme] if isinstance(scheme, str) else scheme
                        if host:
                            mobile_entry["host"] = host
                        if path_prefix:
                            mobile_entry["pathPrefix"] = [path_prefix] if isinstance(path_prefix, str) else path_prefix
                        mobile_entry["appLink"] = app_link

                        conf["deep-link"] = {"mobile": [mobile_entry]}

    return conf


def generate_file_associations(fa_config: dict) -> list:
    """Generate file associations for tauri.conf.json bundle."""
    associations = fa_config.get("associations", [])
    if not associations:
        return []

    result = []
    for assoc in associations:
        entry = {}
        if "ext" in assoc:
            entry["ext"] = assoc["ext"] if isinstance(assoc["ext"], list) else [assoc["ext"]]
        if "mimeType" in assoc:
            entry["mimeType"] = assoc["mimeType"]
        if "name" in assoc:
            entry["name"] = assoc["name"]
        if "description" in assoc:
            entry["description"] = assoc["description"]
        if "role" in assoc:
            entry["role"] = assoc["role"]
        if "rank" in assoc:
            entry["rank"] = assoc["rank"]
        if "androidIntentActionFilters" in assoc:
            entry["androidIntentActionFilters"] = assoc["androidIntentActionFilters"]
        result.append(entry)

    return result


def generate_http_capabilities(plugins_config: dict) -> list:
    """Generate HTTP plugin capabilities with URL scope."""
    for category in ["official", "community"]:
        if category in plugins_config and "http-client" in plugins_config[category]:
            opts = plugins_config[category]["http-client"].get("options", {})
            allowed_urls = opts.get("allowed_urls", [])
            if allowed_urls:
                return [{
                    "identifier": "http:default",
                    "allow": [{"url": url} for url in allowed_urls]
                }]
    return ["http:default"]


def get_deep_link_options(plugins_config: dict) -> dict:
    """Extract deep-link options from config."""
    for category in ["official", "community"]:
        if category in plugins_config and "deep-linking" in plugins_config[category]:
            if plugins_config[category]["deep-linking"].get("enabled", False):
                return plugins_config[category]["deep-linking"].get("options", {})
    return {}


def render_template(env: Environment, template_name: str, context: dict) -> str:
    """Render a Jinja2 template with context."""
    template = env.get_template(template_name)
    return template.render(**context)


def main():
    """Main generation entry point."""
    print("Loading config files...")
    app_config = load_config("app.json")
    plugins_config = load_config("plugins.json")
    fa_config = load_config("file-association.json")

    print("Resolving enabled plugins...")
    enabled_plugins = get_enabled_plugins(plugins_config)
    print(f"  Enabled plugins: {[p.id for p in enabled_plugins]}")

    print("Generating capabilities...")
    capabilities = get_all_capabilities(enabled_plugins)

    # Handle http-client special case (URL scoped capabilities)
    http_plugin = get_plugin("http-client")
    http_caps_extra = []
    if http_plugin in enabled_plugins:
        # Remove simple "http:default" and replace with scoped version
        capabilities = [c for c in capabilities if c != "http:default"]
        http_caps = generate_http_capabilities(plugins_config)
        # If http_caps contains dicts (scoped), add them separately
        for cap in http_caps:
            if isinstance(cap, dict):
                http_caps_extra.append(cap)
            else:
                capabilities.append(cap)

    # Merge string capabilities with any object capabilities
    final_capabilities = capabilities + http_caps_extra

    print("Setting up Jinja2 environment...")
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Generate CSP
    csp = generate_csp(app_config)

    # Generate plugins config for tauri.conf.json
    tauri_plugins_config = generate_plugins_config(enabled_plugins, plugins_config, app_config)

    # Generate file associations
    file_associations = generate_file_associations(fa_config)

    # Context for templates
    context = {
        "app": app_config,
        "plugins": enabled_plugins,
        "capabilities": final_capabilities,
        "csp": csp,
        "plugins_config": tauri_plugins_config,
        "file_associations": file_associations,
    }

    # Render and write Cargo.toml
    print("Generating Cargo.toml...")
    cargo_content = render_template(env, "Cargo.toml.j2", context)
    (SRC_TAURI_DIR / "Cargo.toml").write_text(cargo_content, encoding="utf-8")

    # Compute lib name from identifier (dots→underscores, dashes→underscores)
    lib_name = app_config["identifier"].replace(".", "_").replace("-", "_") + "_lib"

    # Render and write lib.rs
    print("Generating src/lib.rs...")
    src_dir = SRC_TAURI_DIR / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    lib_content = render_template(env, "lib.rs.j2", context)
    (src_dir / "lib.rs").write_text(lib_content, encoding="utf-8")

    # Render and write main.rs
    print("Generating src/main.rs...")
    main_context = {"lib_name": lib_name}
    main_content = render_template(env, "main.rs.j2", main_context)
    (src_dir / "main.rs").write_text(main_content, encoding="utf-8")

    # Render and write tauri.conf.json
    print("Generating tauri.conf.json...")
    tauri_conf_content = render_template(env, "tauri.conf.json.j2", context)
    (SRC_TAURI_DIR / "tauri.conf.json").write_text(tauri_conf_content, encoding="utf-8")

    # Render and write capabilities
    print("Generating capabilities/default.json...")
    CAPABILITIES_DIR.mkdir(parents=True, exist_ok=True)
    caps_content = render_template(env, "capabilities.json.j2", context)
    (CAPABILITIES_DIR / "default.json").write_text(caps_content, encoding="utf-8")

    # =========================================================================
    # Platform-specific file generation
    # =========================================================================
    ios_plist_entries = get_ios_plist_entries(enabled_plugins, plugins_config)
    android_perms = get_android_permissions(enabled_plugins)

    # Deep-link config
    deep_link_opts = get_deep_link_options(plugins_config)
    has_deep_link = any(p.id == "deep-linking" for p in enabled_plugins)
    has_nfc = any(p.id == "nfc" for p in enabled_plugins)

    # Android features
    android_features = []
    if has_nfc:
        android_features.append("android.hardware.nfc")
    if any(p.id == "geolocation" for p in enabled_plugins):
        android_features.append("android.hardware.location.gps")

    platform_context = {
        "app": app_config,
        "ios_plist_entries": ios_plist_entries,
        "android_permissions": android_perms,
        "android_features": android_features,
        "has_nfc": has_nfc,
        "has_deep_link": has_deep_link,
        "deep_link_host": deep_link_opts.get("host", ""),
        "deep_link_scheme": deep_link_opts.get("scheme", ""),
        "deep_link_path_prefix": deep_link_opts.get("pathPrefix", ""),
        "deep_link_app_link": deep_link_opts.get("appLink", True),
        "file_associations": file_associations,
    }

    # Generate iOS Info.plist (only if there are entries)
    if ios_plist_entries:
        print("Generating Info.ios.plist...")
        plist_content = render_template(env, "Info.ios.plist.j2", platform_context)
        (SRC_TAURI_DIR / "Info.ios.plist").write_text(plist_content, encoding="utf-8")

    # Generate iOS entitlements (only if NFC or deep-link with host)
    if has_nfc or (has_deep_link and deep_link_opts.get("host")):
        print("Generating iOS entitlements...")
        entitlements_content = render_template(env, "entitlements.plist.j2", platform_context)
        entitlements_path = SRC_TAURI_DIR / "gen" / "apple" / "webview-wrapper-tauri_iOS" / "webview-wrapper-tauri_iOS.entitlements"
        entitlements_path.parent.mkdir(parents=True, exist_ok=True)
        entitlements_path.write_text(entitlements_content, encoding="utf-8")

    # Generate AndroidManifest.xml (always, since we always have INTERNET)
    print("Generating AndroidManifest.xml...")
    manifest_content = render_template(env, "AndroidManifest.xml.j2", platform_context)
    manifest_path = SRC_TAURI_DIR / "gen" / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(manifest_content, encoding="utf-8")

    print("\nGeneration complete!")
    print(f"  Cargo.toml: {SRC_TAURI_DIR / 'Cargo.toml'}")
    print(f"  lib.rs: {src_dir / 'lib.rs'}")
    print(f"  tauri.conf.json: {SRC_TAURI_DIR / 'tauri.conf.json'}")
    print(f"  capabilities: {CAPABILITIES_DIR / 'default.json'}")
    if ios_plist_entries:
        print(f"  Info.ios.plist: {SRC_TAURI_DIR / 'Info.ios.plist'}")
    if has_nfc or (has_deep_link and deep_link_opts.get("host")):
        print(f"  iOS entitlements: {SRC_TAURI_DIR / 'gen' / 'apple' / 'webview-wrapper-tauri_iOS' / 'webview-wrapper-tauri_iOS.entitlements'}")
    print(f"  AndroidManifest.xml: {manifest_path}")


if __name__ == "__main__":
    main()
