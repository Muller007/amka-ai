# AMKA — API Documentation
*Wake Up Your Money*

---

## Base URL

```
Production:  https://amka-ai.onrender.com
Development: http://localhost:5000
```

---

## Endpoints

### POST /webhook
Receives incoming WhatsApp messages from Twilio.

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-Twilio-Signature: <signature>
```

**Request Body (Twilio format):**
```
From=whatsapp%3A%2B27XXXXXXXXX
Body=I+sold+R150+today
MediaUrl0=https://... (optional, for voice notes)
```

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>✅ Income recorded: R150</Message>
</Response>
```

---

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "AMKA",
  "version": "1.0.0"
}
```

---

### GET /stats (internal)
Returns aggregate anonymised statistics (for dashboard/policymaker API).

**Response:**
```json
{
  "total_users": 1204,
  "total_transactions": 48320,
  "avg_daily_profit_zar": 287.50,
  "most_active_day": "Tuesday",
  "top_expense_category": "stock"
}
```

---

## Intent Classification

AMKA's NLP engine classifies every message into one of these intents:

| Intent | Trigger Examples | Action |
|--------|-----------------|--------|
| `INCOME` | "I sold", "I earned", "received" | Record income |
| `EXPENSE` | "I spent", "I paid", "bought" | Record expense |
| `QUERY_DAY` | "today", "how did I do today" | Return daily summary |
| `QUERY_WEEK` | "this week", "weekly" | Return weekly summary |
| `QUERY_MONTH` | "this month", "monthly" | Return monthly summary |
| `REPORT` | "report", "credit", "loan report" | Generate credit report |
| `HELP` | "help", "?" | Return help message |
| `UNKNOWN` | Anything else | Return guidance message |

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid Twilio signature |
| 422 | Message could not be parsed |
| 500 | Internal server error |

---

*AMKA — Built in Africa, for Africa.*