# Haptics

Trigger haptic feedback (vibration) on the device for tactile responses.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { vibrate, impactFeedback, notificationFeedback, selectionFeedback } = window.__TAURI__.haptics;

// Simple vibration (duration in milliseconds)
await vibrate(100);

// Impact feedback (physical tap feeling)
await impactFeedback('light');   // Subtle tap
await impactFeedback('medium');  // Moderate tap
await impactFeedback('heavy');   // Strong tap

// Notification feedback (indicates outcome)
await notificationFeedback('success');  // Positive outcome
await notificationFeedback('warning');  // Caution
await notificationFeedback('error');    // Failure

// Selection feedback (light tick for selection changes)
await selectionFeedback();
```

## Permissions

- **Android**: `android.permission.VIBRATE` is automatically added.
- **iOS**: No additional permissions required. Uses the Taptic Engine.
