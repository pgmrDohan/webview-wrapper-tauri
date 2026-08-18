# In-App Purchases (IAP)

Support for in-app purchases on Android (Google Play Billing) and iOS (StoreKit).

## Activation

1. Enable in **Setup: Community Plugins** workflow
2. Set product IDs in **Setup: Plugin Options** workflow

## Setup

### Android
- Set up products in Google Play Console
- Configure a service account for server-side verification

### iOS
- Set up products in App Store Connect
- Configure in-app purchases for your app

## Backend API Integration

Your backend should verify purchases server-side:

**POST** `/api/iap/verify`

Request body:
```json
{
  "platform": "android" | "ios",
  "receipt": "purchase-receipt-data",
  "productId": "product_id"
}
```

Response:
```json
{
  "valid": true,
  "productId": "product_id",
  "expiresAt": "2025-01-01T00:00:00Z"
}
```

## Usage

```javascript
// Get available products
const products = await window.__TAURI__.invoke('plugin:iap|get_products', {
  productIds: ['premium_monthly', 'premium_yearly']
});

// Purchase a product
const purchase = await window.__TAURI__.invoke('plugin:iap|purchase', {
  productId: 'premium_monthly'
});

// Verify with your backend
const verification = await fetch('https://your-api.com/api/iap/verify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    platform: purchase.platform,
    receipt: purchase.receipt,
    productId: purchase.productId
  })
});

// Restore purchases
const restored = await window.__TAURI__.invoke('plugin:iap|restore_purchases');
```

## Permissions

No permission request needed. The billing permission is declared in the manifest. Purchase consent is handled by the store's payment UI.

- **Android**: `com.android.vending.BILLING` (auto-added)
