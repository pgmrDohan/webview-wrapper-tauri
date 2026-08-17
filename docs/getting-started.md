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

## Step 3: Implement Native Features in Your Web App

For each plugin you enabled, add the corresponding JavaScript code to your web app. See the [plugin documentation](plugins/) for examples.

### Safe Area (필수)

앱이 전체 화면을 사용하려면 HTML의 `<meta viewport>` 태그에 `viewport-fit=cover`를 추가하세요:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

이렇게 하면:
- 웹 콘텐츠가 노치/Dynamic Island/홈 인디케이터 영역까지 전체 화면을 채움
- CSS 환경 변수로 safe area 크기를 알 수 있음:

```css
body {
  /* 상단 (노치/Dynamic Island 영역) */
  padding-top: env(safe-area-inset-top);
  /* 하단 (홈 인디케이터 영역) */
  padding-bottom: env(safe-area-inset-bottom);
  /* 좌우 (가로 모드에서 노치) */
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

`viewport-fit=cover`가 없으면 시스템이 자동으로 safe area 내부에만 콘텐츠를 배치하며, `env()` 값은 모두 `0`이 됩니다.

### Native Plugin 호출

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

Once complete, find your APK/IPA in the GitHub Releases page.

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
