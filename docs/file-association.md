# File Association Guide

Register your app as a handler for custom file types.

## Configuration

Run **"Setup: File Association"** workflow:
- `extensions`: File extensions without dots (e.g., `myfile,mydata`)
- `mime_type`: MIME type (e.g., `application/x-myfile`)
- `name`: Display name for the file type
- `role`: `Editor` (can modify), `Viewer` (read-only), or `None`
- `rank`: `Owner` (your app created this type), `Default`, or `Alternate`
- `android_intent_actions`: `view`, `send`, or `sendMultiple`

## How It Works

After building, your app will:
- Appear in "Open with" dialogs for matching files
- Be launched when users tap matching files
- Receive the file path via deep link events

## Handling File Opens

```javascript
const { onOpenUrl } = window.__TAURI__.deepLink;

await onOpenUrl((urls) => {
  // urls contains file:// paths when opened via file association
  const filePath = urls[0];
  if (filePath.startsWith('file://')) {
    loadFile(filePath);
  }
});
```

## Multiple File Types

Run the workflow multiple times to add multiple file associations. Use `clear_existing: true` to start fresh.
