# Stripe M2 Reader Setup

This HTML page allows restaurants to connect their Stripe M2 readers through a simple web interface.

## ⚠️ Important: Must Run on Web Server

**The HTML file CANNOT be opened directly (file:// URLs).** It must be served from a web server due to Stripe Terminal SDK requirements.

## Quick Start

### Option 1: Use Provided Server Scripts

**Windows:**
```bash
# Double-click start-server.bat
# OR run in Command Prompt:
start-server.bat
```

**macOS/Linux:**
```bash
# In Terminal:
./start-server.sh
# OR:
python3 serve.py
```

### Option 2: Use Python HTTP Server
```bash
# Python 3:
python3 -m http.server 8000

# Python 2:
python -m SimpleHTTPServer 8000
```

### Option 3: Use Node.js
```bash
# Install and run:
npx http-server -p 8000 --cors
```

## Configuration Required

Before testing, update the HTML file configuration:

```javascript
const CONFIG = {
    STRIPE_PUBLISHABLE_KEY: 'pk_live_your_actual_key',  // Replace
    WEBHOOK_URL: 'https://hook.us1.make.com/registration-webhook',  // Replace
    CONNECTION_TOKEN_URL: 'https://hook.us1.make.com/token-webhook',  // Replace
    TEST_MODE: true  // Set to false for production
};
```

## Test URL Format

### Test Mode (Default - Uses Simulated Readers)
```
http://localhost:8000/index.html?restaurant=Test%20Restaurant&location_id=tml_1234567890&row_id=ROW-123&regemail=test%40test.com
```

### Test Mode (Explicit)
```
http://localhost:8000/index.html?restaurant=Test%20Restaurant&location_id=tml_1234567890&row_id=ROW-123&regemail=test%40test.com&test=true
```

### Production Mode (Real Readers + Webhooks)
```
http://localhost:8000/index.html?restaurant=Mario%27s%20Pizza&location_id=tml_1234567890&row_id=ROW-456&regemail=owner%40mariospizza.com&test=false
```

### URL Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `restaurant` | Yes | Restaurant name (URL encoded) | `Mario%27s%20Pizza` |
| `location_id` | Yes* | Stripe Terminal location ID | `tml_1234567890` |
| `row_id` | Yes | Database row/record ID | `ROW-456` |
| `regemail` | Yes | Restaurant email (URL encoded) | `owner%40mariospizza.com` |
| `test` | No | Override test mode (true/false) | `true` or `false` |

*For test mode, location_id can be empty

## Required Make Scenarios

### 1. Connection Token Webhook
- **Purpose:** Generate Stripe connection tokens
- **URL:** Use for `CONNECTION_TOKEN_URL`
- **Response:** `{"secret": "pst_xxx"}`

### 2. Registration Event Webhook  
- **Purpose:** Handle reader connection success/failure
- **URL:** Use for `WEBHOOK_URL`
- **Response:** Any JSON (optional)

## Testing Modes

### Test Mode Control

**Default:** Test mode is ON by default (`TEST_MODE: true` in code)

**URL Override:** Add `&test=false` to use production mode
**URL Override:** Add `&test=true` to force test mode

### Test Mode (test=true or default)
- ✅ Uses simulated readers (no hardware needed)
- ✅ Uses manual connection token 
- ✅ Logs webhook calls without sending (or sends to test webhooks)
- ✅ Shows yellow test mode banner
- ✅ Perfect for development and demo

### Production Mode (test=false)
- ✅ Uses real M2 readers via Bluetooth
- ✅ Calls actual Make webhooks
- ✅ Full end-to-end integration
- ✅ No test mode banner
- ✅ Ready for restaurant use

## Troubleshooting

### "`onFetchConnectionToken` failure" Error
**Most Common Issue:** This means your Make webhook for connection tokens is not working properly.

**Quick Checks:**
1. **Test your webhook URL directly:**
   ```bash
   curl -X POST https://your-make-webhook-url \
     -H "Content-Type: application/json" \
     -d '{"test": true}'
   ```
   
2. **Expected Response:** Should return JSON like:
   ```json
   {"secret": "pst_xxxxx"}
   ```

3. **Common Problems:**
   - ❌ Webhook returns HTML error page instead of JSON
   - ❌ Missing CORS headers in Make response
   - ❌ Wrong Stripe secret key in Make scenario
   - ❌ Make scenario not active/published
   - ❌ Webhook URL typo in HTML config

4. **Fix Steps:**
   - Check Make scenario execution history
   - Verify Stripe secret key is correct
   - Add CORS headers to Make response
   - Test webhook independently

### "Cookies are disabled" Error
- ❌ Opening HTML file directly
- ✅ Run on web server (http://localhost:8000)

### "Invalid ConnectionToken" Error
- ❌ Make webhook returning HTML instead of JSON
- ❌ Wrong Stripe secret key in Make
- ✅ Check Make scenario execution history

### CORS Errors
- ❌ Missing Access-Control-Allow-Origin header
- ✅ Add CORS headers to Make webhook response

### No Readers Found
- ❌ `simulated: false` without real M2 reader
- ✅ Use `simulated: true` for testing

## File Structure

```
/
├── index.html              # Main setup page
├── serve.py                # Python server script
├── start-server.bat        # Windows launcher
├── start-server.sh         # macOS/Linux launcher
└── README.md              # This file
```

## Support

1. **Check browser console** (F12) for detailed error logs
2. **Verify Make scenarios** are running and returning proper JSON
3. **Test connection token webhook** manually with curl
4. **Ensure CORS headers** are set in Make responses

## Production Deployment

1. Set `TEST_MODE: false`
2. Use `simulated: false` for real readers
3. Deploy to proper web hosting (not localhost)
4. Use HTTPS for production
5. Replace test Stripe keys with live keys
