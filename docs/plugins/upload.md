# Upload

Upload files to a remote server with progress tracking.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { upload } = window.__TAURI__.upload;

// Upload a file with progress tracking
await upload(
  'https://api.example.com/upload',
  '/path/to/file.jpg',
  (progress) => {
    const percent = Math.round((progress.sent / progress.total) * 100);
    console.log(`Upload progress: ${percent}%`);
  },
  {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'multipart/form-data',
  }
);

console.log('Upload complete!');
```

## Permissions

No runtime permissions required. You may need the **File System** or **Dialog** plugin to obtain the file path for upload.
