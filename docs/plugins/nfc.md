# NFC

Read and write NFC tags using the device's NFC hardware.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

On iOS, the NFC reader usage description is configurable via the **Setup: Plugin Options** workflow.

## Permission Request

NFC availability should be checked before scanning:

```javascript
const { isAvailable, scan } = window.__TAURI__.nfc;

// Check if device supports NFC
const available = await isAvailable();
if (!available) {
  console.log('NFC not supported on this device');
  return;
}

// NFC doesn't require explicit permission request on most devices
// The scan dialog handles user consent implicitly
```

On Android, NFC permission is declared in the manifest and doesn't require a runtime prompt. On iOS, the NFC reading session itself acts as the user consent mechanism.

## Usage

```javascript
// Access via window.__TAURI__
const { isAvailable, scan, write } = window.__TAURI__.nfc;

// Check if NFC is available on this device
const available = await isAvailable();
if (!available) {
  console.log('NFC is not available on this device');
}

// Scan for NFC tags
if (available) {
  try {
    const tag = await scan('ndef', {
      keepSessionAlive: false,
    });
    console.log('Tag ID:', tag.id);
    console.log('Records:', tag.records);

    // Read text from the tag
    for (const record of tag.records) {
      if (record.kind === 'text') {
        console.log('Text:', record.text);
      } else if (record.kind === 'url') {
        console.log('URL:', record.url);
      }
    }
  } catch (error) {
    console.error('Scan cancelled or failed:', error);
  }
}

// Write to an NFC tag
if (available) {
  try {
    await write(
      [{ kind: 'text', text: 'Hello from my app!' }],
      { keepSessionAlive: false }
    );
    console.log('Write successful!');
  } catch (error) {
    console.error('Write failed:', error);
  }
}
```

## Permissions

- **iOS**: Requires NFC capability entitlement and `NFCReaderUsageDescription` (configured via Plugin Options). Only available on iPhone 7 and later.
- **Android**: Requires `android.permission.NFC`. The device must have NFC hardware.
