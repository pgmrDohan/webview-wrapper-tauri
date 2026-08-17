# Store

Persistent key-value storage for app data that survives app restarts.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { load } = window.__TAURI__.store;

// Load (or create) a store
const store = await load('settings.json', { autoSave: true });

// Set values
await store.set('username', 'john_doe');
await store.set('theme', 'dark');
await store.set('notifications', { enabled: true, sound: true });

// Get values
const username = await store.get('username');
const theme = await store.get('theme');
console.log(`User: ${username}, Theme: ${theme}`);

// Check all keys
const keys = await store.keys();
console.log('Stored keys:', keys);

// Get all entries
const entries = await store.entries();
console.log('All data:', entries);

// Delete a key
await store.delete('theme');

// Manually save (if autoSave is disabled)
await store.save();
```

## Permissions

No runtime permissions required. Data is stored in the app's private directory.
