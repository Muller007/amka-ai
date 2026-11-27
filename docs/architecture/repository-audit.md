# AMKA Repository Baseline Audit

**Repository:** `Muller007/amka-ai`  
**Audited branch:** `main`  
**Audited commit:** `0e30c7401cbf9fa6dd325d6dd3c502fff6f48995`  
**Audit type:** Initial static repository inspection  
**Status:** Findings require runtime verification before production conclusions.

## Environment

The owner has confirmed that the WhatsApp integration is connected to the Twilio sandbox for testing. This is a development integration, not confirmation of a production deployment.

Preserve the existing sandbox while changes are developed on a separate branch. Do not commit credentials, webhook secrets, personal data, or real financial records.

## Observed implementation

- Flask application files include `app_v3_finetuned.py`.
- SQLAlchemy model definitions are present in `models.py`.
- Database configuration in `database.py` defaults to `sqlite:///amka.db`, with `DATABASE_URL` override.
- A v3 AI engine exists in `ai_engine_v3_finetuned.py`.
- The inspected v3 webhook references Twilio message delivery.
- The separate `Muller007/amka-finance` repository contains a React frontend. Its inspected `src/App.js` is primarily hard-coded presentation content rather than an authenticated API-backed financial dashboard.

## Findings requiring remediation or verification

### P0 — financial data durability

The inspected v3 application stores transaction state in an in-memory `defaultdict`. This is not durable across process restarts and is not shared across multiple application workers. It must not be treated as a reliable financial record store.

**Required outcome:** persist financial events and transaction state in the database; add tests for restart persistence and duplicate-message handling.

### P0 — webhook authenticity

The inspected webhook code does not visibly validate Twilio's request signature.

**Required outcome:** validate the signature using the official Twilio validation mechanism and the exact externally visible URL and parameters. Reject invalid requests. Add positive and negative tests.

### P0 — access control on financial summaries

The inspected `/user/<phone>/summary` route does not visibly enforce authenticated ownership or a permission check.

**Required outcome:** do not expose financial summaries through a caller-controlled phone-number path. Require an authenticated principal and authorise access to the relevant user/workspace.

### P0 — loan eligibility logic

The inspected v3 application contains a simplistic loan eligibility/score calculation. There is no evidence in the inspected code that this is a validated, fair, legally reviewed credit model.

**Required outcome:** disable or clearly isolate this functionality from user-facing decisions. Do not present its output as a credit score, approval, affordability determination, or lending recommendation.

### P1 — transaction confirmation and provenance

The inspected message-processing flow can interpret and record transaction-like messages without a clear confirmation step.

**Required outcome:** represent model output as a candidate. Validate amount, currency, date, activity, direction, and category. Ask the user to confirm or correct ambiguous candidates before posting. Store source and confirmation provenance.

### P1 — unified identity

The current model design uses a unique phone number on the user record. This conflicts with the approved decision that one person can have multiple independently verified channels.

**Required outcome:** introduce an internal stable user ID and a separate channel identity table. Linking a channel must require proof of control and an authenticated existing session or recovery procedure. Phone verification is not legal identity verification.

### P1 — financial numeric correctness

Financial amounts must not use binary floating-point arithmetic for persisted monetary values or ledger calculations.

**Required outcome:** use integer minor units with explicit currency or an appropriately configured decimal type; define rounding rules and test them.

### P1 — dependency and entrypoint consistency

The repository documentation refers to `app.py`, while the inspected root listing did not show that file. The v3 AI engine uses PyTorch/Transformers-related functionality, but the inspected `requirements.txt` did not list all corresponding runtime dependencies.

**Required outcome:** define one supported application entrypoint and reconcile declared dependencies with imports and deployment commands.

### P1 — Twilio client initialisation

The inspected v3 file references `twilio_client`; its initialisation was not found in that file.

**Required outcome:** trace the actual runtime entrypoint and configuration. Add a startup/configuration test that proves the client is correctly initialised or injected.

### P1 — database migration discipline

A migration workflow was not evident in the inspected repository snapshot.

**Required outcome:** introduce Alembic or an equivalent migration mechanism before making schema changes that affect persistent user or financial data.

### P1 — repository data hygiene

The root listing includes a SQLite database file despite database-file ignore patterns in `.gitignore`.

**Required outcome:** inspect whether the committed database contains only synthetic test data. If it contains personal or financial information, follow an incident-aware removal and credential/data response process; deleting the latest copy alone does not remove Git history.

## Frontend alignment findings

The inspected React frontend includes aspirational lending phases, origination-fee assumptions, numerical growth/accuracy targets, and strong fraud-detection claims. These are not evidence of implemented or validated capabilities.

Before connecting it to the backend:
- remove unsupported guarantees, accuracy claims, and unverified market metrics;
- remove assumptions that lending or commissions are the default commercial path;
- clearly distinguish roadmap hypotheses from available functionality;
- foreground financial education, user control, transparency, and accessible learning;
- ensure every financial view is backed by authenticated, authorised API data.

## Initial recommended sequence

1. Create a reproducible test baseline and verify sandbox configuration.
2. Fix webhook signature validation, response delivery, and configuration.
3. Secure summary endpoints and remove unsafe loan-score output.
4. Replace in-memory financial state with durable persistence.
5. Add idempotency and transaction confirmation.
6. Introduce unified identity and channel identities.
7. Define ledger semantics and exact monetary arithmetic.
8. Build education and commercial-governance modules.

## Audit limitations

This is a static inspection of selected repository files at the commit above. It is not a penetration test, legal/compliance review, runtime test, database-content inspection, or proof that no additional safeguards exist elsewhere. Re-check the current branch before implementation and update this document as findings are verified or resolved.
