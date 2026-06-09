# ⚡ AMKA
### *Wake Up Your Money*
#### AI-Powered Financial Intelligence for Africa's Informal Economy

---

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![WhatsApp](https://img.shields.io/badge/WhatsApp-API-25D366?style=flat-square&logo=whatsapp)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-MVP%20Live-brightgreen?style=flat-square)

**[Overview](#-overview) · [Problem](#-problem) · [Solution](#-solution) · [Tech Stack](#-tech-stack) · [Setup](#-setup) · [Roadmap](#-roadmap)**

</div>

---

## 🧠 Overview

**AMKA** is an AI-powered WhatsApp assistant that wakes up the financial lives of Africa's 400 million informal economy workers.

No app to install. No spreadsheet to learn. No bank account required.

Users simply send a WhatsApp message — in plain language, in their own language — and AMKA handles everything behind the scenes: tracking income, recording expenses, calculating profit, and generating intelligent business insights over time.

> *"AMKA" means "wake up" in Swahili. Because millions of African businesses have been financially invisible for too long.*

---

## 🎯 Problem

Across Africa, **over 85% of workers are in the informal sector** — spaza shop owners, market traders, street vendors, boda-boda drivers. They generate enormous economic value every single day, yet remain locked out of formal financial systems because their activity has never been recorded.

Existing tools fail them completely:

| Tool | Why It Fails |
|------|-------------|
| Banking apps | Require formal bank accounts |
| Accounting software | Designed for businesses with accountants |
| Spreadsheets | Require literacy, numeracy, and discipline under survival pressure |
| Most fintech | English-only, app-only, data-heavy |

The result: decisions made on guesswork. No credit access. No insurance. No investment. Permanently locked out — not from lack of activity, but from lack of recorded evidence.

**AMKA changes that.**

---

## 💡 Solution

AMKA lives inside WhatsApp — Africa's most-used communication platform. Users interact the same way they message a friend:

```
User:  "I sold R150 of tomatoes today"
AMKA:  ✅ Income recorded: R150
       📊 Today's total: R150 income | R0 expenses | R150 profit

User:  "spent 40 on transport"
AMKA:  ✅ Expense recorded: R40
       📊 Today: R150 income | R40 expenses | R110 profit

User:  "how am I doing this week?"
AMKA:  📈 Week summary:
       Income:   R1,240
       Expenses: R380
       Profit:   R860 ✨
       Best day: Tuesday (R320 profit)
       Tip: Your Tuesday sales are 40% higher — consider stocking more on Mondays.
```

---

## ✨ Key Features

- 💬 **Natural language tracking** — no commands to memorise
- 📊 **Real-time profit & loss** — on demand, instantly
- 🌍 **Multilingual** — isiZulu, Xhosa, Swahili, Hausa, English
- 🎤 **Voice note support** — speak your transactions if you can't type
- 🤖 **AI-powered insights** — weekly summaries, pattern detection, proactive alerts
- 📋 **Credit report generation** — 30-day financial behaviour report for microfinance applications
- 📱 **Zero install** — works on any WhatsApp-enabled phone

---

## ⚙️ How It Works

```
User → WhatsApp → Twilio Webhook → AMKA Backend → NLP Engine → Database → Insights → Response
```

1. User sends a WhatsApp message (text or voice)
2. NLP engine classifies intent and extracts data
3. Data is stored with timestamp, category, and user ID
4. AI generates a contextual response
5. Over time, patterns emerge and proactive insights are pushed

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-----------|
| Messaging | Twilio WhatsApp Business API |
| Backend | Python (Flask → FastAPI) |
| AI / NLP | Claude API (intent classification + multilingual) |
| Voice | OpenAI Whisper API |
| Database (MVP) | SQLite + SQLAlchemy |
| Database (Prod) | PostgreSQL on Render |
| Deployment | Render |

---

## 📁 Project Structure

```
amka-ai/
├── app.py                  # Main Flask application & webhook handler
├── ai_engine.py            # NLP intent classification & AI insights
├── models.py               # SQLAlchemy data models
├── database.py             # Database connection & session management
├── requirements.txt        # Python dependencies
├── .gitignore
│
└── docs/
    ├── prd.md              # Product Requirements Document
    ├── architecture.md     # System architecture & design decisions
    ├── api_docs.md         # API endpoint documentation
    ├── user_flow.md        # User journey & conversation flows
    ├── database_schema.md  # Database schema & relationships
    ├── privacy_policy.md   # Privacy policy
    └── terms.md            # Terms of service
```

---

## 🔧 Setup

### Prerequisites
- Python 3.10+
- Twilio account (WhatsApp sandbox)
- ngrok (for local development)

### 1. Clone the repository

```bash
git clone https://github.com/Muller007/amka-ai.git
cd amka-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your Twilio credentials
```

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 4. Run the server

```bash
python app.py
```

### 5. Expose with ngrok

```bash
ngrok http 5000
```

### 6. Connect to WhatsApp

- Paste your ngrok URL + `/webhook` into Twilio sandbox settings
- Send "join <sandbox-keyword>" from your WhatsApp
- Start messaging AMKA

---

## 🧪 Example Conversations

| User Says | AMKA Responds |
|-----------|--------------|
| `I sold 150` | Income recorded ✅ · Profit today: R150 |
| `spent 50 on stock` | Expense recorded ✅ · Profit today: R100 |
| `profit` | Income: R150 · Expenses: R50 · Profit: R100 |
| `how was my week` | Full weekly summary with insights |
| `give me my report` | 30-day credit-ready financial report |

---

## 🚀 Roadmap

| Phase | Status | Milestone |
|-------|--------|-----------|
| MVP | ✅ Live | WhatsApp tracking, profit calculation, SQLite |
| Phase 2 | 🔄 In Progress | Multilingual NLP, voice notes, PostgreSQL |
| Phase 3 | 📅 Q4 2026 | AI insights engine, creditworthiness reports |
| Phase 4 | 📅 2027 | Microfinance API integrations |
| Phase 5 | 📅 2027–28 | Continental scale, 10 languages, 10 countries |

---

## 🌍 Why AMKA Matters

- **400M+** informal economy workers across Africa
- **85%+** of sub-Saharan employment is informal
- **$0** access to credit for most — not from lack of activity, but lack of record
- **1 WhatsApp message** is all it takes to start building that record

AMKA doesn't just track money. It builds the financial identity that unlocks everything else.

---

## 👤 Founder

**Kwanele Mlalazi**
BSc Computer Science · MSc Financial Engineering (WorldQuant University, 2026)
AI/ML Engineer · South Africa

> *"Africa's problems will be solved by Africans who understand their texture — the language they speak, the infrastructure they must run on, the trust they must earn."*

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 📬 Contact

Interested in collaboration, partnerships, or piloting AMKA in your community?

👉 Open an issue or connect via GitHub

---

## ⭐ Support the Project

If AMKA resonates with you:

⭐ Star the repo · 🍴 Fork it · 📢 Share it

---

<div align="center">

*"Wake up your money."*

**AMKA** · Built in South Africa · For Africa

</div>