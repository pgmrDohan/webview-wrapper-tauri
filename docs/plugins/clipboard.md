# Clipboard

Read from and write to the system clipboard.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { writeText, readText } = window.__TAURI__.clipboardManager;

// Copy text to clipboard
await writeText('Hello from my app!');

// Read text from clipboard
const text = await readText();
console.log('Clipboard contains:', text);
```

## Permissions

No runtime permissions required. Clipboard access is granted automatically.
