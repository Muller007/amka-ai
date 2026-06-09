# AMKA — User Flow & Conversation Design
*Wake Up Your Money*

---

## Onboarding Flow

```
User sends first message to AMKA WhatsApp number
         │
         ▼
AMKA: "👋 Sawubona! I'm AMKA — your personal business assistant.
       I help you track your money using simple WhatsApp messages.

       To get started, just tell me:
       • What you earned: 'I sold R200 today'
       • What you spent: 'I spent R50 on transport'
       • Your balance: just say 'profit' or 'balance'

       What language do you prefer?
       1. English  2. isiZulu  3. Xhosa  4. Swahili  5. Hausa"
         │
         ▼
User selects language → AMKA confirms and stores preference
```

---

## Core Interaction Flows

### Recording Income
```
User:  "I sold R150 of tomatoes"
         │
         ▼ (NLP: INCOME intent, amount=150, category=produce)
         │
AMKA:  "✅ Income recorded: R150
        📊 Today so far: R150 income | R0 expenses | R150 profit"
```

### Recording Expense
```
User:  "spent 40 on transport"
         │
         ▼ (NLP: EXPENSE intent, amount=40, category=transport)
         │
AMKA:  "✅ Expense recorded: R40
        📊 Today so far: R150 income | R40 expenses | R110 profit"
```

### Querying Balance
```
User:  "how am I doing?"
         │
         ▼ (NLP: QUERY intent)
         │
AMKA:  "📈 Your week so far:
        Income:   R1,240
        Expenses: R380
        Profit:   R860 ✨

        Best day: Tuesday (R320 profit)
        💡 Tip: Your Tuesday income is consistently highest.
           Consider stocking up on Mondays."
```

### Requesting Credit Report
```
User:  "I need my financial report"
         │
         ▼ (NLP: REPORT intent)
         │
AMKA:  "📋 Generating your 30-day AMKA Financial Report...

        Period: 10 May – 9 June 2026
        Total Income:   R12,400
        Total Expenses: R4,200
        Net Profit:     R8,200
        Active Days:    24/30
        Consistency Score: 87/100

        This report can be shared with microfinance institutions.
        Reply 'send report' to receive it as a PDF."
```

---

## Error Handling

```
User:  "hdhsjdksdj"
         │
         ▼ (NLP: UNKNOWN intent)
         │
AMKA:  "🤔 I didn't quite catch that. Try:
        • 'I earned R100' — to record income
        • 'I spent R50' — to record an expense
        • 'profit' — to see your balance
        • 'help' — for all commands"
```

---

## Voice Note Flow

```
User sends voice note: "Ngithengise izinto ezenza imali engu-R200"
         │
         ▼ (Whisper transcription → Zulu text)
         │
         ▼ (Claude API: multilingual NLP → INCOME, R200)
         │
AMKA:  "✅ Understood! Income recorded: R200
        (Transcribed from your voice note 🎤)"
```

---

*AMKA — Built in Africa, for Africa.*