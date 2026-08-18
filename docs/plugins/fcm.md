# FCM (Firebase Cloud Messaging)

Push notification support via Firebase Cloud Messaging.

## Activation

1. Enable in **Setup: Community Plugins** workflow
2. Set your Firebase project ID in **Setup: Plugin Options** workflow

## Prerequisites

### Android
- Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
- Download `google-services.json` and place it in `src-tauri/gen/android/app/`
- (This file must be committed to the repo)

### iOS
- Add your iOS app to the Firebase project
- Download `GoogleService-Info.plist`
- Enable Push Notifications capability in Apple Developer Portal

## Backend API Integration

Your backend server needs to:
1. Receive device tokens from the app
2. Send push notifications via Firebase Cloud Messaging API

### Device Token Registration

The app will call your API to register its FCM token. Implement this endpoint:

**POST** `/api/fcm/register`

Request body:
```json
{
  "token": "fcm-device-token-string",
  "platform": "android" | "ios",
  "device_id": "unique-device-identifier"
}
```

Response: `200 OK`

### Sending Notifications (Server-side)

Use Firebase Admin SDK or HTTP API to send notifications:

```
POST https://fcm.googleapis.com/v1/projects/{project_id}/messages:send

{
  "message": {
    "token": "device-token",
    "notification": {
      "title": "Title",
      "body": "Message body"
    },
    "data": {
      "custom_key": "custom_value"
    }
  }
}
```

## Usage (Web App JavaScript)

```javascript
// Note: FCM plugin API depends on the specific plugin version
// Check the plugin repository for the latest API

// Listen for push notifications
window.__TAURI__.event.listen('fcm://notification', (event) => {
  console.log('Push notification received:', event.payload);
});

// Get FCM token
window.__TAURI__.event.listen('fcm://token', (event) => {
  const token = event.payload;
  // Send token to your backend
  fetch('https://your-api.com/api/fcm/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      token: token,
      platform: 'android', // or detect platform
    })
  });
});
```

## Permissions

Push notification permission is requested at runtime on iOS. On Android 13+, the `POST_NOTIFICATIONS` permission is also required at runtime.

FCM token delivery is automatic. Notification display permission is handled by the notification plugin if also enabled.
