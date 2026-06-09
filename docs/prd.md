# AMKA — Product Requirements Document
*Wake Up Your Money*

---

## 1. Product Overview

**Product Name:** AMKA
**Tagline:** Wake Up Your Money
**Version:** 1.0 (MVP)
**Last Updated:** June 2026

AMKA is an AI-powered WhatsApp assistant that enables Africa's informal economy workers to track their finances, receive intelligent business insights, and build a financial identity that unlocks access to credit and formal financial services.

---

## 2. Problem Statement

Over 400 million workers in Africa's informal economy generate significant economic value daily but remain financially invisible. Existing financial tools are too complex, inaccessible, or irrelevant to their reality. AMKA bridges this gap using the tool they already use: WhatsApp.

---

## 3. Target Users

**Primary:** Informal micro-entrepreneurs (spaza shops, market traders, street vendors, service providers)
**Secondary:** Smallholder farmers tracking seasonal income
**Tertiary:** Domestic workers and gig economy participants

**User Profile:**
- Owns a basic Android smartphone
- Uses WhatsApp daily
- May have limited formal education
- Transacts in cash
- Speaks a local African language

---

## 4. Core Features (MVP)

### 4.1 Income Tracking
- Record income via natural language message
- Automatic amount extraction from freeform text
- Timestamp and category tagging

### 4.2 Expense Tracking
- Record expenses via natural language message
- Optional category tagging (stock, transport, food, etc.)

### 4.3 Profit Calculation
- On-demand profit calculation (daily, weekly, monthly)
- Real-time balance after each transaction

### 4.4 Business Insights (Phase 2)
- Weekly AI-generated business summaries
- Spending pattern detection and alerts
- Best/worst day analysis
- Stock timing recommendations

### 4.5 Credit Report (Phase 3)
- 30-day financial behaviour summary
- Exportable report for microfinance applications
- Creditworthiness score based on consistency and growth

---

## 5. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Response time | < 3 seconds per message |
| Uptime | 99.5% |
| Data encryption | AES-256 at rest, TLS in transit |
| Supported languages | English, isiZulu, Xhosa, Swahili, Hausa |
| Minimum device | Any WhatsApp-capable Android phone |
| Data usage per interaction | < 1KB |

---

## 6. Success Metrics

- Monthly Active Users (MAU)
- Average messages per user per day
- 30-day user retention rate
- Number of credit reports generated
- Loans facilitated via AMKA credit reports

---

## 7. Out of Scope (v1.0)

- Web or mobile app interface
- Direct bank integrations
- Payment processing
- Multi-user business accounts

---

*AMKA — Built in Africa, for Africa.*