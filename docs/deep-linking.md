# Deep Linking Guide

Deep links allow your app to be opened from URLs.

## Two Types

### Custom URL Scheme (e.g., `myapp://`)
- No server configuration needed
- Not verified (any app can claim the scheme)
- Works on both Android and iOS

### App Links / Universal Links (e.g., `https://yourdomain.com/open`)
- Requires server configuration
- Verified ownership (only your app handles these URLs)
- Opens directly without disambiguation dialog

## Configuration

1. Run **"Setup: Plugin Options"** workflow with:
   - `deep_link_scheme`: Your custom scheme (e.g., `myapp`)
   - `deep_link_host`: Your domain (e.g., `app.example.com`)
   - `deep_link_path_prefix`: Path prefix (e.g., `/open`)
   - `deep_link_app_link`: `true` for verified links

## Server Setup (for App Links / Universal Links)

### Android: Digital Asset Links

Host this file at `https://yourdomain.com/.well-known/assetlinks.json`:

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.yourcompany.yourapp",
    "sha256_cert_fingerprints": ["YOUR_CERT_FINGERPRINT"]
  }
}]
```

Get your fingerprint:
```bash
keytool -list -v -keystore release.keystore -alias release | grep SHA256
```

### iOS: Apple App Site Association

Host this file at `https://yourdomain.com/.well-known/apple-app-site-association`:

```json
{
  "applinks": {
    "details": [{
      "appIDs": ["TEAMID.com.yourcompany.yourapp"],
      "components": [{
        "/": "/open/*",
        "comment": "Matches URLs with /open/ path"
      }]
    }]
  }
}
```

Replace `TEAMID` with your Apple Developer Team ID.

## Handling Deep Links in Your Web App

```javascript
// Using withGlobalTauri
const { getCurrent, onOpenUrl } = window.__TAURI__.deepLink;

// Check if app was opened via deep link
const urls = await getCurrent();
if (urls) {
  handleDeepLink(urls[0]);
}

// Listen for deep links while app is running
await onOpenUrl((urls) => {
  handleDeepLink(urls[0]);
});

function handleDeepLink(url) {
  const parsed = new URL(url);
  // Route based on path
  if (parsed.pathname.startsWith('/open/')) {
    // Handle open action
  }
}
```

## Testing

- **Android**: `adb shell am start -a android.intent.action.VIEW -d "myapp://test"`
- **iOS Simulator**: `xcrun simctl openurl booted "myapp://test"`
