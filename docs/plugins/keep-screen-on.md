# Keep Screen On

Prevents the device screen from turning off while the app is active.

## Activation

Enable in **Setup: Community Plugins** workflow.

## Usage

```javascript
// Keep screen on
await window.__TAURI__.invoke('plugin:keep-screen-on|enable');

// Allow screen to turn off again
await window.__TAURI__.invoke('plugin:keep-screen-on|disable');
```

## Permissions

- **Android**: WAKE_LOCK permission (auto-added)
- **iOS**: No additional permissions needed
