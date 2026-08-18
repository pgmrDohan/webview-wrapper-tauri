# iOS Photos

Access the iOS photo library to select and retrieve photos.

## Activation

1. Enable in **Setup: Community Plugins** workflow
2. Set photo library usage description in **Setup: Plugin Options** workflow

## Permission Request

Photo library access triggers a permission dialog automatically on first use (iOS only):

```javascript
// The photo picker itself handles permission
// When you call pick_photo, iOS shows the photo library permission dialog
// if it hasn't been granted yet

// The usage description you set in Plugin Options is shown in this dialog
```

No explicit `requestPermissions()` call needed — the photo picker UI handles consent implicitly.

## Usage

```javascript
// Pick a photo from the library
const photo = await window.__TAURI__.invoke('plugin:ios-photos|pick_photo');

if (photo) {
  // photo contains the image data or path
  console.log('Selected photo:', photo);
}

// Pick multiple photos
const photos = await window.__TAURI__.invoke('plugin:ios-photos|pick_photos', {
  limit: 5
});
```

## Permissions

- **iOS**: Photo Library Usage Description (configurable in Plugin Options)
- This plugin is iOS-only
