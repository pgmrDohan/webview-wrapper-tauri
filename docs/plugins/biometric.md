# Biometric Authentication

Authenticate users with fingerprint, Face ID, or device credentials.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

On iOS, the Face ID usage description is configurable via the **Setup: Plugin Options** workflow.

## Permission Request

Biometric does not require a runtime permission request. Instead, check if biometric hardware is available:

```javascript
const { checkStatus } = window.__TAURI__.biometric;

const status = await checkStatus();
if (!status.isAvailable) {
  console.log('Biometric not available:', status.error);
  // Fallback to password-based auth
  return;
}

// Biometric is available - proceed with authenticate()
```

The actual biometric prompt (Face ID / fingerprint) appears when you call `authenticate()`. On iOS, the Face ID usage description (configured in Plugin Options) is shown the first time.

## Usage

```javascript
// Access via window.__TAURI__
const { checkStatus, authenticate } = window.__TAURI__.biometric;

// Check if biometric authentication is available
const status = await checkStatus();
console.log('Available:', status.isAvailable);
console.log('Type:', status.biometryType); // 'faceId', 'touchId', 'fingerprint', etc.

if (status.isAvailable) {
  // Authenticate the user
  try {
    await authenticate('Confirm your identity to continue', {
      allowDeviceCredential: true,  // Allow PIN/password fallback
      cancelTitle: 'Cancel',
      fallbackTitle: 'Use password',
    });
    console.log('Authentication successful!');
  } catch (error) {
    console.error('Authentication failed:', error);
  }
}
```

## Permissions

- **iOS**: Requires `NSFaceIDUsageDescription` in Info.plist (configured via Plugin Options).
- **Android**: No additional permissions required. Uses the device's built-in biometric prompt.
