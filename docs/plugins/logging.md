# Logging

Send log messages from your web app to the native logging system.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { trace, debug, info, warn, error } = window.__TAURI__.log;

// Log at different levels
trace('Entering function X');
debug('Variable state: ' + JSON.stringify(data));
info('User logged in successfully');
warn('API response was slow (2.3s)');
error('Failed to fetch user data: ' + err.message);
```

Logs are written to the native platform's logging system:
- **Android**: Logcat
- **iOS**: Unified Logging (Console.app)

## Permissions

No runtime permissions required.
