# Persisted Scope

Automatically persists file/directory access permissions across app restarts.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

This plugin works automatically behind the scenes. There is no JavaScript API to call.

When your app grants access to files or directories (e.g., through a file picker), the Persisted Scope plugin remembers those permissions. The next time the app launches, previously granted file access is restored without prompting the user again.

This is especially useful in combination with the **File System** and **Dialog** plugins, where users select files they want the app to access.

## Permissions

No runtime permissions required. This plugin only persists permissions already granted by the user.
