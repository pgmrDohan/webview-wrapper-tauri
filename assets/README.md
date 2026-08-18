# App Assets

Place your app assets in this folder.

## Required Files

### `icon.png`
- **Size**: 1024x1024 pixels (will be auto-resized for all platforms)
- **Format**: PNG with transparency support
- **Usage**: App icon shown on home screen, app switcher, etc.

### `splash.png`
- **Size**: Recommended 512x512 or larger (centered on screen)
- **Format**: PNG with transparent background
- **Usage**: Shown on app launch screen, centered with the splash background color

## Configuration

Set the splash background color in the **"Setup: App Configuration"** workflow via the `splash_background_color` input.

## Notes

- These files are processed during build time
- The build system generates all required sizes automatically
- Icon: generates iOS/Android icon sets from your single PNG
- Splash: places your image centered on a solid background for both platforms
