# HTTP Client

Make HTTP requests from your app without CORS restrictions. Uses the same `fetch` API you already know.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

Configure allowed URLs in the **Setup: Plugin Options** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { fetch } = window.__TAURI__.http;

// GET request
const response = await fetch('https://api.example.com/users');
const users = await response.json();
console.log('Users:', users);

// POST request with JSON body
const createResponse = await fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'Alice',
    email: 'alice@example.com',
  }),
});
const newUser = await createResponse.json();
console.log('Created:', newUser);

// Handle response status
const res = await fetch('https://api.example.com/data');
if (res.ok) {
  const data = await res.json();
  console.log('Data:', data);
} else {
  console.error('Request failed:', res.status, res.statusText);
}
```

## Configuration

Allowed URLs must be configured in the **Setup: Plugin Options** workflow. Only requests matching allowed URL patterns will succeed. Use patterns like:

- `https://api.example.com/*` - allow all paths under a domain
- `https://*.example.com/*` - allow subdomains

## Permissions

No runtime permission needed. URL access is controlled by the `allowed_urls` config.

- **Android**: `android.permission.INTERNET` is automatically added.
- **iOS**: No additional permissions required.

Unlike browser fetch, this plugin bypasses CORS restrictions since requests are made from the native layer rather than the WebView.
