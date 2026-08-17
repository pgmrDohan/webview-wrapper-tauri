# Opener

Open URLs in the default browser or files with the system's default app.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { openUrl, openPath } = window.__TAURI__.opener;

// Open a URL in the default browser
await openUrl('https://example.com');

// Open a URL with a specific app (optional)
await openUrl('https://maps.google.com/?q=Tokyo', 'com.google.android.apps.maps');

// Open a file with the system's default application
await openPath('/path/to/document.pdf');
```

## Permissions

No runtime permissions required. The OS handles launching the appropriate app.
