# UDP

UDP socket communication for real-time networking.

## Activation

Enable in **Setup: Community Plugins** workflow.

## Usage

```javascript
// Create a UDP socket
const socket = await window.__TAURI__.invoke('plugin:udp|bind', {
  address: '0.0.0.0:0'  // Bind to any available port
});

// Send data
await window.__TAURI__.invoke('plugin:udp|send', {
  id: socket.id,
  address: '192.168.1.100:8080',
  data: Array.from(new TextEncoder().encode('Hello'))
});

// Listen for incoming data
await window.__TAURI__.event.listen('plugin:udp://receive', (event) => {
  const { data, from } = event.payload;
  console.log(`Received from ${from}:`, new TextDecoder().decode(new Uint8Array(data)));
});

// Close socket
await window.__TAURI__.invoke('plugin:udp|close', { id: socket.id });
```

## Permissions

No runtime permission request needed. This plugin works immediately once enabled in the build configuration.

- **Android**: INTERNET permission (auto-added)
