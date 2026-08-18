# WebView Wrapper Tauri

Turn your existing website into a native Android & iOS app with native feature support — no Rust or native development knowledge required.

## Features

- 🌐 **Load your website** as a full-screen native app
- 📱 **29 native plugins** available (camera, GPS, biometrics, NFC, push notifications, and more)
- 🔧 **Zero code modification** — configure everything via GitHub Actions
- 🏗️ **Automated builds** — CI/CD produces signed APK & IPA
- 📖 **Complete documentation** — JS code examples for every plugin

## Quick Start

1. **Fork** this repository
2. Go to **Actions** tab → Run **"Setup: App Configuration"**
3. Run **"Setup: Official Plugins"** to enable desired features
4. Implement the JS calls in your web app (see [docs](docs/))
5. Run **"Build: Android & iOS"** → Download from Releases

📖 **[Full Getting Started Guide →](docs/getting-started.md)**

## Supported Plugins

### Official Plugins
| Plugin | Description | Platform |
|--------|-------------|----------|
| Barcode Scanner | QR/barcode scanning via camera | Android, iOS |
| Clipboard | Read/write system clipboard | Android, iOS |
| Biometric | Fingerprint/Face ID authentication | Android, iOS |
| Dialog | Native file/message dialogs | Android, iOS |
| Deep Linking | URL schemes & universal links | Android, iOS |
| Store | Persistent key-value storage | Android, iOS |
| Persisted Scope | Remember file permissions | Android, iOS |
| OS Info | Device/OS information | Android, iOS |
| Opener | Open URLs/files externally | Android, iOS |
| Notification | Local notifications | Android, iOS |
| NFC | NFC tag reading/writing | Android, iOS |
| Logging | Structured native logging | Android, iOS |
| HTTP Client | Native HTTP requests (bypass CORS) | Android, iOS |
| Haptics | Vibration/haptic feedback | Android, iOS |
| Geolocation | GPS/location services | Android, iOS |
| File System | Local file read/write | Android, iOS |
| Stronghold | Encrypted secret storage | Android, iOS |
| WebSocket | Native WebSocket connections | Android, iOS |
| Upload | File upload with progress | Android, iOS |

### Community Plugins
| Plugin | Description | Platform |
|--------|-------------|----------|
| FCM | Firebase Cloud Messaging | Android, iOS |
| BLE | Bluetooth Low Energy | Android, iOS |
| Prevent Default | Disable browser behaviors | Android, iOS |
| iOS Photos | Photo library access | iOS |
| Keep Screen On | Prevent screen timeout | Android, iOS |
| IAP | In-App Purchases | Android, iOS |
| Sharesheet | Native share dialog | Android, iOS |
| UDP | UDP socket communication | Android, iOS |
| Battery Optimization | Disable battery optimization | Android |

## How It Works

```
┌──────────────────┐     ┌───────────────────────┐
│  Your Web App    │     │  GitHub Actions        │
│  (deployed URL)  │     │  (setup workflows)     │
└────────┬─────────┘     └───────────┬───────────┘
         │                           │
         │                           ▼
         │              ┌────────────────────────┐
         │              │  config/ (JSON files)   │
         │              └───────────┬────────────┘
         │                          │
         │                          ▼
         │              ┌────────────────────────┐
         │              │  scripts/generate.py    │
         │              │  (code generation)      │
         │              └───────────┬────────────┘
         │                          │
         ▼                          ▼
┌──────────────────────────────────────────────────┐
│          Tauri v2 Native App                      │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ WebView  │  │  IPC     │  │   Native      │  │
│  │ (your    │◄─┤  Bridge  ├──┤   Plugins     │  │
│  │  site)   │  │          │  │   (selected)  │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
└──────────────────────────────────────────────────┘
```

## Configuration Workflows

| Workflow | Purpose |
|----------|---------|
| Setup: App Configuration | App name, URL, identifier |
| Setup: Official Plugins | Enable/disable official plugins |
| Setup: Community Plugins | Enable/disable community plugins |
| Setup: Plugin Options | Plugin-specific settings |
| Setup: File Association | Custom file type handling |
| Setup: Signing Configuration | Code signing setup |
| Build: Android & iOS | Compile and release |

## Documentation

- [Getting Started](docs/getting-started.md)
- [Signing Guide](docs/signing.md)
- [Deep Linking](docs/deep-linking.md)
- [File Association](docs/file-association.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Plugin Docs](docs/plugins/)

## Development

```bash
# Install dependencies
make setup

# Run tests
make test

# Generate project files from config
make generate

# Validate config
make validate
```

## Tech Stack

- **[Tauri v2](https://v2.tauri.app/)** - Native app framework
- **[Rust](https://www.rust-lang.org/)** - Native backend (auto-generated)
- **Python 3.11+** - Build scripts and code generation
- **Jinja2** - Template engine for code generation
- **GitHub Actions** - CI/CD and configuration UI

## License

MIT
