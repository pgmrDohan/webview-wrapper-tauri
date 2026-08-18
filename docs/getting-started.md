# Getting Started

## Prerequisites

- A deployed web application (accessible via HTTPS URL)
- A GitHub account
- (For iOS) Apple Developer account ($99/year)
- (For Android) Google Play Developer account ($25 one-time)

## Step 1: Fork This Repository

Click "Fork" on GitHub to create your own copy.

## Step 2: Configure Your App

Go to the **Actions** tab in your forked repo and run workflows in this order:

### 2.1 App Configuration

Run **"Setup: App Configuration"** workflow:
- `app_name`: Your app's display name
- `identifier`: Reverse domain (e.g., `com.yourcompany.yourapp`)
- `version`: Semantic version (e.g., `1.0.0`)
- `website_url`: Your web app URL (e.g., `https://app.yoursite.com`)
- `api_url`: Your API URL (e.g., `https://api.yoursite.com`)

### 2.2 Select Plugins

Run **"Setup: Official Plugins"** and/or **"Setup: Community Plugins"** workflows:
- Toggle ON the native features you want
- Only enable what you'll actually use (each plugin adds to app size)

### 2.3 Configure Plugin Options (if needed)

If you enabled plugins that require additional configuration (deep-linking, HTTP client, etc.), run **"Setup: Plugin Options"** workflow.

### 2.4 File Association (optional)

If your app handles custom file types, run **"Setup: File Association"** workflow.

## Step 2.5: Add App Assets

### App Icon

Commit your app icon as `assets/icon.png`:
- **Size**: 1024x1024 pixels
- **Format**: PNG (transparency supported)
- The build system automatically generates all required sizes for Android and iOS

### Splash Screen

Commit your splash image as `assets/splash.png`:
- **Size**: 512x512 or 1024x1024 pixels recommended
- **Format**: PNG with transparent background
- The image is centered on a solid background color on both platforms
- Set the background color in the **"Setup: App Configuration"** workflow (`splash_background_color` field)

Both files are optional. If not provided, defaults are used.

## Step 3: Implement Native Features in Your Web App

For each plugin you enabled, add the corresponding JavaScript code to your web app. See the [plugin documentation](plugins/) for examples.

### Safe Area (Required)

To make your app use the full screen, add `viewport-fit=cover` to the `<meta viewport>` tag in your HTML:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

This enables:
- Web content fills the entire screen, extending into the notch/Dynamic Island and home indicator areas
- CSS environment variables provide safe area dimensions:

```css
body {
  /* Top (notch / Dynamic Island area) */
  padding-top: env(safe-area-inset-top);
  /* Bottom (home indicator area) */
  padding-bottom: env(safe-area-inset-bottom);
  /* Left/Right (notch in landscape mode) */
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

Without `viewport-fit=cover`, the system automatically constrains content within the safe area, and all `env()` values will be `0`.

### Native Plugin Usage

Key pattern for most plugins:
```javascript
// 1. Check permission
// 2. Request permission if needed
// 3. Use the feature
```

Since `withGlobalTauri` is enabled, access plugins via:
```javascript
window.__TAURI__.pluginNamespace.functionName()
```

**Tip**: Check if running inside Tauri before calling native APIs:
```javascript
if (window.__TAURI__) {
  // Native features available
  const pos = await window.__TAURI__.geolocation.getCurrentPosition();
} else {
  // Fallback for browser
  navigator.geolocation.getCurrentPosition(callback);
}
```

## Step 4: Configure Signing

Run **"Setup: Signing Configuration"** workflow, then add signing secrets to your repo:

1. Go to Settings > Secrets and variables > Actions
2. Add the required secrets (the workflow will tell you which ones are missing)

See [Signing Guide](signing.md) for detailed instructions.

## Step 5: Build

Run **"Build: Android & iOS"** workflow:
- Enter a version tag (e.g., `v1.0.0`)
- Choose which platforms to build
- Choose build mode:
  - **Debug**: No signing required. Produces test builds:
    - Android: debug APK (installable via USB / `adb install`)
    - iOS: simulator build (run in Xcode Simulator)
  - **Release**: Requires signing configuration. Produces store-ready builds:
    - Android: signed APK for Google Play
    - iOS: signed IPA for App Store / TestFlight

For first-time testing, use **debug** mode. Switch to **release** when ready for distribution.

Once complete, find your builds in the workflow's **Artifacts** section (debug) or **GitHub Releases** page (release).

## Step 6: Distribute

- **Android**: Upload APK to Google Play Console
- **iOS**: Upload IPA via Transporter app to App Store Connect

## Updating Your App

1. Update your web app (no rebuild needed if only web content changed)
2. If you need to change native configuration, re-run the relevant setup workflow
3. Run the build workflow with a new version tag

## Architecture

```
Your Web App (deployed)  <-->  Native WebView Container
         |                           |
   window.__TAURI__  <-->  Tauri IPC Bridge  <-->  Native Plugins
```

The app is essentially a native shell that loads your website. Native features are accessed through the `window.__TAURI__` bridge.
