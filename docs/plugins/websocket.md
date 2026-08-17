# WebSocket

Connect to WebSocket servers for real-time bidirectional communication.

## Activation

Enable this plugin in the **Setup: Official Plugins** workflow.

## Usage

```javascript
// Access via window.__TAURI__
const { WebSocket } = window.__TAURI__.websocket;

// Connect to a WebSocket server
const ws = await WebSocket.connect('wss://echo.websocket.org');

// Listen for messages
ws.addListener((message) => {
  if (message.type === 'Text') {
    console.log('Received:', message.data);
  } else if (message.type === 'Binary') {
    console.log('Binary data:', message.data);
  } else if (message.type === 'Close') {
    console.log('Connection closed');
  }
});

// Send a text message
await ws.send('Hello, server!');

// Send a JSON message
await ws.send(JSON.stringify({ type: 'chat', content: 'Hi there!' }));

// Disconnect when done
await ws.disconnect();
```

## Permissions

No runtime permissions required. Network access is handled by the native layer.
