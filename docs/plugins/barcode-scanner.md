# Barcode Scanner

Scan barcodes and QR codes using the device camera.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

On iOS, the camera usage description is configurable via the **Setup: Plugin Options** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { scan, cancel, checkPermissions, requestPermissions } = window.__TAURI__.barcodeScanner;

// Check and request camera permission
let perms = await checkPermissions();
if (perms.camera === 'prompt') {
  perms = await requestPermissions();
}

if (perms.camera === 'granted') {
  // Scan a QR code (full screen)
  const result = await scan({ formats: ['QR_CODE'] });
  console.log('Scanned:', result.content);

  // Scan in windowed mode (shows camera preview in a smaller area)
  const windowed = await scan({ windowed: true, formats: ['QR_CODE', 'EAN_13'] });
  console.log('Scanned:', windowed.content);
}

// Cancel an ongoing scan
await cancel();
```

## Permissions

Requires camera permission at runtime. The app will prompt the user for access on first use.

- **iOS**: Camera usage description shown to the user is configurable in Plugin Options.
- **Android**: `android.permission.CAMERA` is automatically added.
