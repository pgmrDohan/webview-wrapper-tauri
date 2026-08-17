# Android Battery Optimization

Request that the Android system excludes your app from battery optimization, allowing background work to continue uninterrupted.

## Activation

Enable in **Setup: Community Plugins** workflow.

## Usage

```javascript
// Check if battery optimization is disabled for this app
const isIgnoring = await window.__TAURI__.invoke(
  'plugin:android-battery-optimization|is_ignoring_battery_optimizations'
);

if (!isIgnoring) {
  // Request the user to disable battery optimization
  await window.__TAURI__.invoke(
    'plugin:android-battery-optimization|request_ignore_battery_optimizations'
  );
}
```

## Notes

- This is Android-only. On iOS, this plugin does nothing.
- The system will show a dialog asking the user to allow the app to ignore battery optimizations.
- Some Android manufacturers have additional battery management that this cannot control.

## Permissions

- **Android**: `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` (auto-added)
