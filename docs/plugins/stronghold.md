# Stronghold

Encrypted storage for sensitive data like tokens, keys, and secrets. Data is protected by a password-derived encryption key.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { Stronghold } = window.__TAURI__.stronghold;

// Load or create a stronghold vault (password-protected)
const stronghold = await Stronghold.load('vault.hold', 'user-password-here');

// Create a client to organize your secrets
const client = await stronghold.createClient('my-app');

// Get the store for key-value secret storage
const store = client.getStore();

// Store a secret
const encoder = new TextEncoder();
await store.insert('api-token', encoder.encode('sk_live_abc123'));

// Retrieve a secret
const data = await store.get('api-token');
const decoder = new TextDecoder();
const token = decoder.decode(data);
console.log('Token:', token);

// Save changes to disk
await stronghold.save();
```

## Permissions

No runtime permissions required. Data is stored encrypted in the app's private directory using Argon2 key derivation.
