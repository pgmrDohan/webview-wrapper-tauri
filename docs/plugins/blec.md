# BLE (Bluetooth Low Energy)

Bluetooth Low Energy communication for connecting to BLE peripherals.

## Activation

1. Enable in **Setup: Community Plugins** workflow
2. Set Bluetooth usage description in **Setup: Plugin Options** workflow

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
