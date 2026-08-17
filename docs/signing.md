# Code Signing Guide

## Android Signing

### Generate a Keystore

```bash
keytool -genkey -v \
  -keystore release.keystore \
  -alias release \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

You'll be prompted for passwords and identity information.

### Add Secrets to GitHub

1. Base64-encode your keystore:
   ```bash
   base64 -i release.keystore | pbcopy  # macOS
   base64 -w 0 release.keystore         # Linux
   ```

2. Go to your repo: Settings > Secrets and variables > Actions

3. Add these secrets:
   - `ANDROID_KEYSTORE_BASE64`: The base64-encoded keystore
   - `ANDROID_KEYSTORE_PASSWORD`: Keystore password
   - `ANDROID_KEY_PASSWORD`: Key password

4. Run the **"Setup: Signing Configuration"** workflow with your key alias

### Important Notes
- **Never commit** the keystore file directly to the repo
- **Back up** your keystore securely — if you lose it, you cannot update your app on Google Play
- Use a strong password (12+ characters)

## iOS Signing

### Prerequisites
- Apple Developer account (enrolled in Apple Developer Program)
- Xcode installed on a Mac (for certificate generation)

### Generate Certificate & Profile

1. In Xcode: Preferences > Accounts > Manage Certificates > "+" > Apple Distribution
2. In [Apple Developer Portal](https://developer.apple.com/account/resources/certificates/list):
   - Create an App ID matching your identifier
   - Create a Provisioning Profile (App Store Distribution)
   - Download the profile

3. Export certificate:
   - Open Keychain Access
   - Find your distribution certificate
   - Right-click > Export as .p12

### Add Secrets to GitHub

1. Base64-encode your files:
   ```bash
   base64 -i certificate.p12 | pbcopy
   base64 -i profile.mobileprovision | pbcopy
   ```

2. Add these secrets:
   - `IOS_CERTIFICATE_BASE64`: Base64-encoded .p12 certificate
   - `IOS_CERTIFICATE_PASSWORD`: Certificate export password
   - `IOS_PROVISIONING_PROFILE_BASE64`: Base64-encoded .mobileprovision

3. Run **"Setup: Signing Configuration"** with your Team ID

### Finding Your Team ID
- Go to [Apple Developer Portal](https://developer.apple.com/account) > Membership Details
- Your Team ID is a 10-character alphanumeric string
