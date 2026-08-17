# OS Info

Get information about the device's operating system.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { platform, version, type, arch } = window.__TAURI__.os;

// Get the platform
const p = await platform();
console.log('Platform:', p); // 'android', 'ios'

// Get OS version
const v = await version();
console.log('Version:', v); // e.g., '14.0' (iOS) or '13' (Android API level)

// Get OS type
const t = await type();
console.log('Type:', t); // 'android', 'ios'

// Get CPU architecture
const a = await arch();
console.log('Architecture:', a); // 'aarch64', 'x86_64', etc.
```

## Permissions

No runtime permissions required. OS information is always accessible.
