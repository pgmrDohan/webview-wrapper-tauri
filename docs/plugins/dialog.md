# Dialog

Show native dialog boxes for alerts, confirmations, and file picking.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { ask, confirm, message, open, save } = window.__TAURI__.dialog;

// Show a yes/no question dialog
const answer = await ask('Do you want to save changes?', {
  title: 'Unsaved Changes',
  kind: 'warning',
});
console.log('User chose:', answer); // true or false

// Show a confirmation dialog (OK/Cancel)
const confirmed = await confirm('Are you sure you want to delete this item?', {
  title: 'Confirm Delete',
  kind: 'warning',
});

// Show an informational message
await message('Operation completed successfully!', {
  title: 'Success',
  kind: 'info',
});

// Open a file picker
const filePath = await open({
  multiple: false,
  filters: [
    { name: 'Images', extensions: ['png', 'jpg', 'jpeg'] },
    { name: 'All Files', extensions: ['*'] },
  ],
});
if (filePath) {
  console.log('Selected file:', filePath);
}

// Open a save dialog
const savePath = await save({
  defaultPath: 'document.txt',
  filters: [
    { name: 'Text Files', extensions: ['txt'] },
  ],
});
if (savePath) {
  console.log('Save to:', savePath);
}
```

## Permissions

No runtime permissions required. Dialogs are shown using native system UI.
