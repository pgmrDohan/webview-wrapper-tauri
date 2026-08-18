# System UI

Control native system UI elements including status bar, navigation bar, home indicator, orientation, and screen modes from JavaScript.

## Activation

Enable in **Setup: Community Plugins** workflow.

## Usage

### Status Bar Style

```javascript
// Set light content (white text/icons - use on dark backgrounds)
await window.__TAURI__.invoke('plugin:system-ui|set_status_bar_style', { style: 'light' });

// Set dark content (black text/icons - use on light backgrounds)
await window.__TAURI__.invoke('plugin:system-ui|set_status_bar_style', { style: 'dark' });
```

### Status Bar Visibility

```javascript
// Hide the status bar
await window.__TAURI__.invoke('plugin:system-ui|set_status_bar_visible', { visible: false });

// Show the status bar
await window.__TAURI__.invoke('plugin:system-ui|set_status_bar_visible', { visible: true });
```

### Navigation Bar Style

```javascript
// Set light navigation bar content (Android: white icons)
await window.__TAURI__.invoke('plugin:system-ui|set_navigation_bar_style', { style: 'light' });

// Set dark navigation bar content (Android: dark icons)
await window.__TAURI__.invoke('plugin:system-ui|set_navigation_bar_style', { style: 'dark' });
```

### Home Indicator (iOS only)

```javascript
// Auto-hide the home indicator
await window.__TAURI__.invoke('plugin:system-ui|set_home_indicator_auto_hidden', { hidden: true });

// Show the home indicator
await window.__TAURI__.invoke('plugin:system-ui|set_home_indicator_auto_hidden', { hidden: false });
```

### Edge-to-Edge Mode

```javascript
// Enable edge-to-edge (content extends behind system bars)
await window.__TAURI__.invoke('plugin:system-ui|set_edge_to_edge', { enabled: true });

// Disable edge-to-edge (content stays within safe area)
await window.__TAURI__.invoke('plugin:system-ui|set_edge_to_edge', { enabled: false });
```

### Immersive Mode

```javascript
// Enable immersive mode (hide all system bars, swipe to reveal)
await window.__TAURI__.invoke('plugin:system-ui|set_immersive_mode', { enabled: true });

// Disable immersive mode (show all system bars)
await window.__TAURI__.invoke('plugin:system-ui|set_immersive_mode', { enabled: false });
```

### Screen Orientation

```javascript
// Lock to portrait
await window.__TAURI__.invoke('plugin:system-ui|set_orientation', { orientation: 'portrait' });

// Lock to landscape
await window.__TAURI__.invoke('plugin:system-ui|set_orientation', { orientation: 'landscape' });

// Allow auto-rotation
await window.__TAURI__.invoke('plugin:system-ui|set_orientation', { orientation: 'auto' });
```

## Platform Notes

| Feature | Android | iOS |
|---------|---------|-----|
| Status Bar Style | ✅ | ✅ |
| Status Bar Visibility | ✅ | ✅ |
| Navigation Bar Style | ✅ | No-op (no nav bar) |
| Home Indicator | No-op | ✅ |
| Edge-to-Edge | ✅ | ✅ |
| Immersive Mode | ✅ | ✅ |
| Orientation Lock | ✅ | ✅ |

## Permissions

No runtime permissions required on either platform.
