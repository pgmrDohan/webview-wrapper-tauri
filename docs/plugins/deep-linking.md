# Deep Linking

Handle custom URL schemes and universal/app links to open your app from external sources.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

Also configure your deep link scheme, host, and path prefix in the **Setup: Plugin Options** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { getCurrent, onOpenUrl } = window.__TAURI__.deepLink;

// Check if the app was opened via a deep link
const initialUrls = await getCurrent();
if (initialUrls && initialUrls.length > 0) {
  console.log('App opened with URL:', initialUrls[0]);
  handleDeepLink(initialUrls[0]);
}

// Listen for deep link events while the app is running
await onOpenUrl((urls) => {
  console.log('Received deep link:', urls);
  handleDeepLink(urls[0]);
});

// Handle the deep link in your app
function handleDeepLink(url) {
  const parsed = new URL(url);
  console.log('Scheme:', parsed.protocol);
  console.log('Host:', parsed.hostname);
  console.log('Path:', parsed.pathname);
  console.log('Params:', parsed.searchParams.toString());
}
```

## Configuration

Configure deep link settings in the **Setup: Plugin Options** workflow:

- **Scheme**: Your custom URL scheme (e.g., `myapp`)
- **Host**: The host for universal links (e.g., `example.com`)
- **Path Prefix**: Optional path prefix for matching (e.g., `/open`)

This configures both Android Intent Filters and iOS Associated Domains.

## Permissions

No runtime permissions required. Deep links are handled at the OS level.

For universal links (iOS) and app links (Android), you also need to host a verification file on your server. See [Deep Linking Server Setup](../deep-linking.md) for details.
