# BLE (Bluetooth Low Energy)

Bluetooth Low Energy communication for connecting to BLE peripherals.

## Activation

1. Enable in **Setup: Community Plugins** workflow
2. Set Bluetooth usage description in **Setup: Plugin Options** workflow

## Permission Request

Bluetooth permission must be requested on Android 12+ before scanning:

```javascript
// Bluetooth permission request (Android 12+)
// The exact API depends on the plugin version - check the repo

// General pattern:
// 1. Check if Bluetooth is available and permissions granted
// 2. Request if needed
// 3. Then scan/connect

// On iOS, the system shows a Bluetooth permission dialog automatically
// when you first attempt to scan (triggered by the NSBluetoothAlwaysUsageDescription)
```

On iOS, the permission dialog appears automatically on first BLE operation. The usage description you configured in Plugin Options is displayed in this dialog.

## Usage

```javascript
// BLE plugin API (check repo for latest)
// General pattern: scan → connect → read/write characteristics

// Example: Scan for devices
const devices = await window.__TAURI__.invoke('plugin:blec|scan', {
  timeout: 5000
});

// Connect to device
await window.__TAURI__.invoke('plugin:blec|connect', {
  address: devices[0].address
});

// Read characteristic
const value = await window.__TAURI__.invoke('plugin:blec|read', {
  address: devices[0].address,
  service: 'service-uuid',
  characteristic: 'characteristic-uuid'
});
```

## Permissions

- **iOS**: Bluetooth Always Usage Description (configurable in Plugin Options)
- **Android**: BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_CONNECT, BLUETOOTH_SCAN permissions (auto-added)
