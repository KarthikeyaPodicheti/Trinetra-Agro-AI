# OTP Webhook Setup

This project uses `OTP_WEBHOOK_URL` for OTP delivery in `AUTH_MODE=otp`.

## 1) Run local OTP gateway (quick test)

```bash
python otp_gateway.py --host 127.0.0.1 --port 8081
```

By default (`OTP_PROVIDER=console`), OTP codes are printed in terminal.

## 2) Configure app `.env`

```env
REQUIRE_LOGIN=true
AUTH_MODE=otp
OTP_WEBHOOK_URL=http://127.0.0.1:8081/send-otp
OTP_ALLOW_DEV_FALLBACK=false
```

If you set token protection on gateway:

```env
OTP_GATEWAY_BEARER_TOKEN=your_token
OTP_WEBHOOK_BEARER_TOKEN=your_token
```

## 3) Use real SMS provider

### Fast2SMS

Set these where `otp_gateway.py` runs:

```env
OTP_PROVIDER=fast2sms
FAST2SMS_API_KEY=your_fast2sms_key
```

### Twilio

Set these where `otp_gateway.py` runs:

```env
OTP_PROVIDER=twilio
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_FROM_NUMBER=+1...
```

## 4) Production checklist
- Keep `OTP_ALLOW_DEV_FALLBACK=false`
- Keep `OTP_DEBUG_PANEL=false`
- Use HTTPS endpoint for `OTP_WEBHOOK_URL`
- Add bearer token (`OTP_WEBHOOK_BEARER_TOKEN`)
- Restrict network access to gateway endpoint
- Enable request logging and alerting

## 4.1) Dev OTP panel (local testing only)

To see the latest OTP directly in Streamlit login screen:

```env
OTP_DEBUG_PANEL=true
```

This is only for local testing and must remain `false` in production.

## 5) Start with production runner (Windows)

```powershell
./start_production.ps1 -CheckOnly
./start_production.ps1 -StartGateway
```
