# AMKA — System Architecture
*Wake Up Your Money*

---

## Overview

AMKA is a webhook-driven, stateless backend that processes incoming WhatsApp messages, applies NLP to extract financial intent, persists data, and returns intelligent responses — all within a single conversational interface.

---

## High-Level Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   User      │────▶│  WhatsApp    │────▶│  Twilio         │
│  (WhatsApp) │◀────│  (Message)   │◀────│  Webhook        │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                                                   ▼
                                        ┌─────────────────┐
                                        │  AMKA Backend   │
                                        │  (Flask/FastAPI)│
                                        └────────┬────────┘
                                                 │
                          ┌──────────────────────┼──────────────────────┐
                          ▼                      ▼                      ▼
                 ┌────────────────┐   ┌──────────────────┐   ┌─────────────────┐
                 │  NLP Engine    │   │  Database        │   │  Insights       │
                 │  (Claude API + │   │  (PostgreSQL)    │   │  Engine         │
                 │   Whisper)     │   │                  │   │  (ML patterns)  │
                 └────────────────┘   └──────────────────┘   └─────────────────┘
```

---

## Component Breakdown

### 1. Twilio WhatsApp Webhook
- Receives incoming messages (text + voice)
- Sends outgoing responses
- Handles message status callbacks

### 2. AMKA Backend (Flask → FastAPI)
- `/webhook` — POST endpoint receiving Twilio payloads
- Orchestrates NLP → DB → Response pipeline
- Stateless — all state lives in the database

### 3. NLP Engine (`ai_engine.py`)
- Intent classification: INCOME | EXPENSE | QUERY | REPORT | UNKNOWN
- Amount extraction from freeform text
- Multilingual understanding via Claude API
- Voice transcription via OpenAI Whisper

### 4. Database Layer (`database.py`, `models.py`)
- SQLAlchemy ORM
- MVP: SQLite (local dev)
- Production: PostgreSQL on Render

### 5. Insights Engine
- Runs on scheduled basis (daily/weekly)
- Detects spending patterns, anomalies, best/worst periods
- Generates proactive WhatsApp alerts

---

## Data Flow

```
1. Message arrives at /webhook
2. Extract: user phone number, message body (or audio URL)
3. If audio: transcribe via Whisper API
4. Classify intent via NLP engine
5. Extract financial data (amount, category, date)
6. Write to database
7. Query database for context (today's total, streak, etc.)
8. Generate response via Claude API
9. Return response to Twilio → WhatsApp
```

---

## Deployment

| Environment | Stack |
|-------------|-------|
| Local dev | Flask + SQLite + ngrok |
| Staging | FastAPI + PostgreSQL + Render |
| Production | FastAPI + PostgreSQL + Render (auto-deploy from main branch) |

---

## Security

- All API keys stored as environment variables (never hardcoded)
- TLS enforced on all endpoints
- Database credentials rotated quarterly
- Twilio webhook signature validation enabled

---

*AMKA — Built in Africa, for Africa.*