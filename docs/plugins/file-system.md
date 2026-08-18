# File System

Read and write files on the device's file system.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { readTextFile, writeTextFile, readFile, writeFile, exists, mkdir, readDir, remove } = window.__TAURI__.fs;

// Write a text file to the app's data directory
await writeTextFile('notes.txt', 'Hello, world!', {
  baseDir: BaseDirectory.AppData,
});

// Read a text file
const content = await readTextFile('notes.txt', {
  baseDir: BaseDirectory.AppData,
});
console.log('File content:', content);

// Check if a file exists
const fileExists = await exists('notes.txt', {
  baseDir: BaseDirectory.AppData,
});
console.log('Exists:', fileExists);

// Create a directory
await mkdir('my-folder', {
  baseDir: BaseDirectory.AppData,
  recursive: true,
});

// List directory contents
const entries = await readDir('my-folder', {
  baseDir: BaseDirectory.AppData,
});
for (const entry of entries) {
  console.log(entry.name, entry.isDirectory ? '(dir)' : '(file)');
}

// Write binary data
const bytes = new Uint8Array([72, 101, 108, 108, 111]);
await writeFile('data.bin', bytes, {
  baseDir: BaseDirectory.AppData,
});

// Read binary data
const data = await readFile('data.bin', {
  baseDir: BaseDirectory.AppData,
});

// Remove a file
await remove('notes.txt', {
  baseDir: BaseDirectory.AppData,
});
```

### BaseDirectory Options

Use these constants for the `baseDir` option:

```javascript
const { BaseDirectory } = window.__TAURI__.path;

// Common directories:
// BaseDirectory.AppData    - App's private data directory
// BaseDirectory.AppCache   - App's cache directory
// BaseDirectory.Document   - Documents directory
// BaseDirectory.Download   - Downloads directory
```

## Permissions

No runtime permission prompt on mobile (access is sandboxed to app directories by default). If you need access to shared storage directories, the user grants access through the file picker dialog.

- **Android**: `READ_EXTERNAL_STORAGE` and `WRITE_EXTERNAL_STORAGE` are added for broader access on older Android versions.
- **iOS**: Access is sandboxed to the app container.
