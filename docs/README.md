# WebView Wrapper Tauri - Documentation

Transform your web application into a native mobile app with native feature support.

## Overview

This template lets you build Android and iOS apps from your existing website. You don't need to learn Rust or native development — configure everything through GitHub Actions workflows and write JavaScript in your web app to use native features.

## How It Works

1. **Your web app** loads in a native WebView (full-screen, no browser chrome)
2. **Native plugins** are available via `window.__TAURI__` JavaScript API
3. **Configuration** is done through GitHub Actions (no code modification needed)
4. **Build** produces signed APK (Android) and IPA (iOS) ready for store submission

## Documentation

- [Getting Started](getting-started.md) - Step-by-step setup guide
- [Signing Guide](signing.md) - Android & iOS code signing
- [Deep Linking](deep-linking.md) - URL scheme & universal links setup
- [File Association](file-association.md) - Custom file type handling
- [Troubleshooting](troubleshooting.md) - Common issues & solutions

## Supported Plugins

### Official (19)
| Plugin | Description |
|--------|------------|
| [Barcode Scanner](plugins/barcode-scanner.md) | Camera-based QR/barcode scanning |
| [Clipboard](plugins/clipboard.md) | Read/write system clipboard |
| [Biometric](plugins/biometric.md) | Fingerprint/Face ID authentication |
| [Dialog](plugins/dialog.md) | Native file/message dialogs |
| [Deep Linking](plugins/deep-linking.md) | URL schemes & universal links |
| [Store](plugins/store.md) | Persistent key-value storage |
| [Persisted Scope](plugins/persisted-scope.md) | Remember file permissions |
| [OS Info](plugins/os-info.md) | Device/OS information |
| [Opener](plugins/opener.md) | Open URLs/files externally |
| [Notification](plugins/notification.md) | Local notifications |
| [NFC](plugins/nfc.md) | NFC tag reading/writing |
| [Logging](plugins/logging.md) | Structured logging |
| [HTTP Client](plugins/http-client.md) | Native HTTP requests |
| [Haptics](plugins/haptics.md) | Vibration/haptic feedback |
| [Geolocation](plugins/geolocation.md) | GPS location services |
| [File System](plugins/file-system.md) | Local file access |
| [Stronghold](plugins/stronghold.md) | Encrypted secret storage |
| [WebSocket](plugins/websocket.md) | WebSocket connections |
| [Upload](plugins/upload.md) | File upload with progress |

### Community (10)
| Plugin | Description |
|--------|------------|
| [FCM](plugins/fcm.md) | Firebase push notifications |
| [BLE](plugins/blec.md) | Bluetooth Low Energy |
| [Prevent Default](plugins/prevent-default.md) | Disable browser behaviors |
| [iOS Photos](plugins/ios-photos.md) | Photo library access |
| [Keep Screen On](plugins/keep-screen-on.md) | Prevent screen timeout |
| [IAP](plugins/iap.md) | In-App Purchases |
| [Sharesheet](plugins/sharesheet.md) | Native share dialog |
| [UDP](plugins/udp.md) | UDP socket communication |
| [Battery Optimization](plugins/android-battery-optimization.md) | Background work |
| [System UI](plugins/system-ui.md) | Status bar, navigation bar, home indicator, orientation control |
