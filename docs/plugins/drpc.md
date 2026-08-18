# Discord Rich Presence (DRPC)

Display custom status information on Discord.

## Activation

1. Enable in **Setup: Community Plugins** workflow
2. Set your Discord Application ID in **Setup: Plugin Options** workflow

## Setup

1. Create an application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Note the Application ID
3. Set up Rich Presence assets (images) in the portal
4. Enter the Application ID in the Plugin Options workflow

## Usage

```javascript
// Set Rich Presence activity
await window.__TAURI__.invoke('plugin:drpc|set_activity', {
  state: "Playing",
  details: "Level 5",
  largeImage: "logo",
  largeText: "My App",
  smallImage: "status",
  smallText: "Online",
  startTimestamp: Date.now()
});

// Clear Rich Presence
await window.__TAURI__.invoke('plugin:drpc|clear_activity');
```

## Notes

- Discord must be running on the device for Rich Presence to work
- This plugin is primarily useful for desktop; mobile support may be limited

## Permissions

No runtime permission request needed. This plugin works immediately once enabled in the build configuration.
