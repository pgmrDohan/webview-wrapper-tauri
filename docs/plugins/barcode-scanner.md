# Barcode Scanner

Scan barcodes and QR codes using the device camera.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

On iOS, the camera usage description is configurable via the **Setup: Plugin Options** workflow.

## Permission Request

Camera permission must be requested before scanning:

```javascript
const { checkPermissions, requestPermissions } = window.__TAURI__.barcodeScanner;

// Check current permission state
const status = await checkPermissions();

if (status.camera === 'prompt' || status.camera === 'prompt-with-rationale') {
  // Request permission - OS dialog appears at this moment
  const result = await requestPermissions();
  if (result.camera !== 'granted') {
    console.log('Camera permission denied');
    return;
  }
}

if (status.camera === 'denied') {
  // User previously denied - direct them to app settings
  const { openAppSettings } = window.__TAURI__.barcodeScanner;
  await openAppSettings();
  return;
}

// Permission granted - now safe to scan
```

You control when this dialog appears. Call `requestPermissions()` only when the user initiates a scan action.

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
