# Geolocation

Access the device's GPS/location services to get the user's position.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

On iOS, the location usage description is configurable via the **Setup: Plugin Options** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { checkPermissions, requestPermissions, getCurrentPosition, watchPosition } = window.__TAURI__.geolocation;

// Check and request location permission
let perms = await checkPermissions();
if (perms.location === 'prompt') {
  perms = await requestPermissions(['location']);
}

if (perms.location === 'granted') {
  // Get current position
  const pos = await getCurrentPosition();
  console.log('Latitude:', pos.coords.latitude);
  console.log('Longitude:', pos.coords.longitude);
  console.log('Accuracy:', pos.coords.accuracy, 'meters');

  // Watch position changes
  const watchId = await watchPosition(
    { enableHighAccuracy: true },
    (position, error) => {
      if (error) {
        console.error('Watch error:', error);
        return;
      }
      console.log('Moved to:', position.coords.latitude, position.coords.longitude);
    }
  );

  // Stop watching later
  // clearWatch(watchId);
}
```

## Permissions

Requires runtime location permission. Follow the check → request → use pattern.

- **iOS**: `NSLocationWhenInUseUsageDescription` is configurable in Plugin Options.
- **Android**: `ACCESS_COARSE_LOCATION` and `ACCESS_FINE_LOCATION` are automatically added.
