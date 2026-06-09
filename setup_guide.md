# AMKA — Complete Setup & Implementation Guide
*Wake Up Your Money*

---

##  What You've Got

This package contains everything you need to rebrand and deploy AMKA:

### Code Files
- `app.py` — Main Flask application with Twilio webhook
- `ai_engine.py` — AI intent classification & NLP engine
- `models.py` — SQLAlchemy database models (User, Transaction, Insight, CreditReport)
- `database.py` — Database configuration & session management
- `requirements.txt` — Python dependencies
- `.env.example` — Environment variables template
- `.gitignore` — Git ignore configuration

### Documentation
- `README.md` — Professional project README with badges and tables
- `GITHUB_REBRAND_GUIDE.md` — Step-by-step GitHub rename instructions
- `docs/prd.md` — Product Requirements Document
- `docs/architecture.md` — System architecture with ASCII diagrams
- `docs/api_docs.md` — API endpoints and intent classification
- `docs/user_flow.md` — User conversation flows
- `docs/database_schema.md` — Database schema and relationships
- `docs/privacy_policy.md` — Privacy policy
- `docs/terms.md` — Terms of service

### Competition Submission
- `AMKA_Competition_Submission.docx` — Professional competition submission with AMKA branding

---

## 🚀 Quick Start (5 steps)

### Step 1: Clone or Pull Latest Code

If you haven't cloned yet:
```bash
git clone https://github.com/Muller007/smart-living-ai.git
cd smart-living-ai
```

If you already have it:
```bash
cd your_project_folder
git pull origin main
```

### Step 2: Copy All Files from This Package

Copy all files from this package (code + docs) into your project folder:
```
AMKA-Rebrand/
├── app.py
├── ai_engine.py
├── models.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── GITHUB_REBRAND_GUIDE.md
└── docs/
    ├── prd.md
    ├── architecture.md
    ├── api_docs.md
    ├── user_flow.md
    ├── database_schema.md
    ├── privacy_policy.md
    └── terms.md
```

Replace existing files if they exist.

### Step 3: Update Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in your actual credentials:
```env
TWILIO_ACCOUNT_SID=your_actual_sid
TWILIO_AUTH_TOKEN=your_actual_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
CLAUDE_API_KEY=your_actual_key
OPENAI_API_KEY=your_actual_key
DATABASE_URL=sqlite:///amka.db
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Rename on GitHub

Follow the **GITHUB_REBRAND_GUIDE.md** to rename your repo from `smart-living-ai` → `amka-ai`.

---

## 🔧 Running AMKA Locally

### Initialize the database
```bash
python database.py
# Creates amka.db with all tables
```

### Test the AI engine
```bash
python ai_engine.py
# Tests intent classification on sample messages
```

### Start the Flask server
```bash
python app.py
# Server runs on http://localhost:5000
```

### Expose with ngrok (for Twilio)
In a new terminal:
```bash
ngrok http 5000
# Copy the ngrok URL (e.g., https://abc123.ngrok.io)
```

### Connect to Twilio WhatsApp

1. Go to https://twilio.com/console
2. Go to **Messaging → Try it out → Send a WhatsApp message**
3. Paste your ngrok URL + `/webhook` as the webhook URL
4. Example: `https://abc123.ngrok.io/webhook`
5. Send a WhatsApp message to the sandbox number — AMKA should respond!

---

## 📋 File-by-File Explanation

### `app.py`
Main Flask application. Handles:
- Incoming WhatsApp messages via `/webhook` endpoint
- Routes to appropriate intent handlers (INCOME, EXPENSE, QUERY_DAY, QUERY_WEEK, QUERY_MONTH, REPORT)
- Stores transactions in database
- Calculates profit/loss summaries
- Sends responses back via Twilio

**Key functions:**
- `webhook()` — Main entry point
- `handle_income()` — Record income transaction
- `handle_expense()` — Record expense transaction
- `handle_query_day/week/month()` — Return financial summaries
- `handle_report()` — Generate credit report
- `send_whatsapp_message()` — Send response via Twilio

### `ai_engine.py`
NLP and AI engine. Handles:
- Intent classification (INCOME | EXPENSE | QUERY | REPORT | HELP | UNKNOWN)
- Financial data extraction (amount, category)
- Voice note transcription via Whisper API
- Message generation

**Key methods:**
- `classify_intent()` — Uses Claude API to understand user messages
- `transcribe_voice_note()` — Uses Whisper API to convert speech to text
- `get_onboarding_message()` — Welcome message for new users
- `get_help_message()` — Help command response

### `models.py`
SQLAlchemy ORM models. Defines database structure:
- `User` — User account with phone number, language preference
- `Transaction` — Income/expense entries
- `Insight` — AI-generated insights sent to users
- `CreditReport` — Generated financial reports

### `database.py`
Database configuration:
- Creates SQLite or PostgreSQL connection
- Initializes all tables
- Provides session management

### `requirements.txt`
Python dependencies. Main packages:
- Flask — Web framework
- twilio — WhatsApp integration
- anthropic — Claude API
- openai — Whisper API + GPT
- sqlalchemy — Database ORM

---

## 🌍 Deployment to Render

### Step 1: Push to GitHub
```bash
git add .
git commit -m "rebrand: Smart Living AI → AMKA"
git push origin main
```

### Step 2: Connect to Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo (amka-ai)
4. Configure:
   - **Name:** amka-ai
   - **Environment:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
5. Add environment variables (same as .env)
6. Click "Deploy"

### Step 3: Update Twilio Webhook
1. Go to Twilio Console
2. Copy your Render URL (e.g., `https://amka-ai.onrender.com`)
3. Paste in Twilio sandbox: `https://amka-ai.onrender.com/webhook`
4. Test with a WhatsApp message

---

## 🧪 Testing Checklist

- [ ] Local Flask server runs without errors
- [ ] `python database.py` creates amka.db
- [ ] `python ai_engine.py` classifies test messages correctly
- [ ] Ngrok tunnel is active and responding
- [ ] WhatsApp sandbox webhook is connected
- [ ] Test message "I sold R150" records income
- [ ] Test message "I spent R50" records expense
- [ ] Test message "profit" returns daily summary
- [ ] Twilio logs show no errors

---

## 🎯 Next Steps (Before Competition Submission)

1. **Test everything locally** — Make sure the MVP works
2. **Record a demo video** — 2 minutes showing AMKA working on WhatsApp
3. **Upgrade to Phase 2 features** (optional but recommended):
   - Add multilingual NLP (support more African languages)
   - Add voice note transcription (Whisper)
   - Migrate to PostgreSQL
4. **Submit the competition document** — Use `AMKA_Competition_Submission.docx`
5. **Deploy to Render** — Make sure your live app is accessible

---

## 📞 Support

Questions? Check:
- GitHub Issues: github.com/Muller007/amka-ai/issues
- Documentation: Check the `docs/` folder
- Code comments: Every function is documented

---

*AMKA — Wake Up Your Money*
*Built in Africa, for Africa*

---

## Important Reminders

- **Keep `.env` out of Git** — Never commit your API keys
- **Test locally first** — Before pushing to Render
- **Backup your database** — Especially before migrations
- **Monitor Twilio logs** — To debug webhook issues
- **Update README** — Keep it current as you add features

Good luck! 🚀