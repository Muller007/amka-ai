# AMKA — Database Schema
*Wake Up Your Money*

---

## Tables

### users
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| phone_number | VARCHAR(20) UNIQUE | WhatsApp number (E.164 format) |
| language | VARCHAR(10) | Preferred language code (en, zu, xh, sw, ha) |
| created_at | DATETIME | Account creation timestamp |
| last_active | DATETIME | Last interaction timestamp |

### transactions
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| user_id | INTEGER FK → users.id | Owner of transaction |
| type | VARCHAR(10) | 'income' or 'expense' |
| amount | DECIMAL(10,2) | Transaction amount |
| category | VARCHAR(50) | Auto-detected category (stock, transport, food, etc.) |
| raw_message | TEXT | Original user message |
| created_at | DATETIME | Transaction timestamp |

### insights
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| user_id | INTEGER FK → users.id | Target user |
| type | VARCHAR(30) | Insight type (weekly_summary, pattern_alert, etc.) |
| content | TEXT | Insight message content |
| delivered | BOOLEAN | Whether WhatsApp delivery confirmed |
| created_at | DATETIME | Generation timestamp |

### credit_reports
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| user_id | INTEGER FK → users.id | Report subject |
| period_start | DATE | Report start date |
| period_end | DATE | Report end date |
| total_income | DECIMAL(12,2) | Total income in period |
| total_expenses | DECIMAL(12,2) | Total expenses in period |
| net_profit | DECIMAL(12,2) | Net profit in period |
| active_days | INTEGER | Days with at least one transaction |
| consistency_score | INTEGER | 0–100 score based on regularity |
| generated_at | DATETIME | Report generation timestamp |

---

## Indexes

```sql
CREATE INDEX idx_transactions_user_date ON transactions(user_id, created_at);
CREATE INDEX idx_transactions_type ON transactions(type);
CREATE INDEX idx_insights_user ON insights(user_id, delivered);
```

---

## Relationships

```
users (1) ──── (many) transactions
users (1) ──── (many) insights
users (1) ──── (many) credit_reports
```

---

*AMKA — Built in Africa, for Africa.*