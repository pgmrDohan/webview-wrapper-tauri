# Sharesheet

Display the native share dialog to share content with other apps.

## Activation

Enable in **Setup: Community Plugins** workflow.

## Usage

```javascript
// Share text
await window.__TAURI__.invoke('plugin:sharesheet|share', {
  text: 'Check out this link!',
  url: 'https://example.com'
});

// Share with title
await window.__TAURI__.invoke('plugin:sharesheet|share', {
  title: 'Share this',
  text: 'Amazing content',
  url: 'https://example.com/content/123'
});
```
