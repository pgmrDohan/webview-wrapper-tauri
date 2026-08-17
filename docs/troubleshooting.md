# Troubleshooting

## Build Issues

### "Cargo.toml not found" or build fails immediately
Make sure you've run at least the **"Setup: App Configuration"** workflow before building.

### Android build fails with NDK error
The build workflow sets up NDK r26b. If a plugin requires a different version, check the plugin's documentation.

### iOS build fails with signing error
Ensure all iOS signing secrets are correctly base64-encoded and the provisioning profile matches your bundle identifier.

### "Plugin not found" in build logs
Make sure you enabled the plugin in the setup workflow AND ran the build workflow after that.

## Runtime Issues

### `window.__TAURI__` is undefined
- Your website must be served over HTTPS
- The WebView loads your URL — make sure it's accessible
- Check that `withGlobalTauri: true` is in the generated config

### Plugin functions throw "permission denied"
Most plugins that access device features require runtime permissions. Follow the pattern:
```javascript
const perms = await checkPermissions();
if (perms.status === 'prompt') {
  await requestPermissions();
}
```

### App shows blank white screen
- Verify your website URL is correct and accessible
- Check if there are CSP (Content Security Policy) errors in the logs
- Your API URL must be included in the app configuration for API calls to work

### Deep links not working
- **Android**: Verify `.well-known/assetlinks.json` is accessible and correctly formatted
- **iOS**: Verify `.well-known/apple-app-site-association` is served with correct content-type
- Custom schemes work without server config but aren't verified

### Push notifications not received
- Verify `google-services.json` is committed to the repo (Android)
- Ensure push notification capability is enabled in Apple Developer Portal (iOS)
- Check that the FCM token is being sent to your backend

## Configuration Issues

### Workflow shows "no changes to commit"
The config file already has those values. This is not an error.

### Multiple workflows conflict
Run workflows sequentially (wait for one to complete before starting the next). They modify different files so conflicts are rare, but the git push can fail if runs overlap.

## Getting Help

1. Check the [plugin documentation](plugins/) for specific plugin issues
2. Check the [Tauri v2 docs](https://v2.tauri.app/) for framework-level issues
3. Check the specific community plugin repository for community plugin issues
