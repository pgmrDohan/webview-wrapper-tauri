# Notification

Send local push notifications to the user, with support for channels and action buttons.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const {
  isPermissionGranted,
  requestPermission,
  sendNotification,
  registerActionTypes,
  onAction,
  createChannel,
  channels,
} = window.__TAURI__.notification;

// Check and request notification permission
let granted = await isPermissionGranted();
if (!granted) {
  const permission = await requestPermission();
  granted = permission === 'granted';
}

if (granted) {
  // Send a simple notification
  sendNotification({
    title: 'New Message',
    body: 'You have a new message from Alice.',
  });

  // Send with more options
  sendNotification({
    title: 'Download Complete',
    body: 'Your file has been downloaded.',
    icon: 'download-icon',
    channelId: 'downloads',
  });
}

// Create a notification channel (Android)
await createChannel({
  id: 'downloads',
  name: 'Downloads',
  description: 'File download notifications',
  importance: 3, // DEFAULT
  sound: 'default',
  vibration: true,
});

// List existing channels
const allChannels = await channels();
console.log('Channels:', allChannels);

// Register action buttons
await registerActionTypes([
  {
    id: 'message-actions',
    actions: [
      { id: 'reply', title: 'Reply' },
      { id: 'dismiss', title: 'Dismiss', destructive: true },
    ],
  },
]);

// Handle notification action clicks
await onAction((notification) => {
  console.log('Action clicked:', notification.actionTypeId);
  console.log('Data:', notification.data);
});
```

## Permissions

Requires notification permission on both platforms. The app will prompt the user for permission on first use.

On Android 13+, the `POST_NOTIFICATIONS` permission is requested at runtime.
