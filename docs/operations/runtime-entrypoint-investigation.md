# Runtime Entry-Point Investigation

**Status:** Investigation required before changing the deployed webhook.

## Why this investigation exists

The repository contains several conflicting descriptions of how AMKA starts:

- The root contains `app_v3_finetuned.py`, which defines a Flask application named `app`.
- The root does not contain `app.py`, although the README and setup guide instruct operators to run `python app.py`.
- The setup guide recommends `gunicorn app:app`, which also targets the missing `app.py`.
- The v3 webhook references `twilio_client`, but the inspected module does not initialise that variable.
- The v3 module stores transaction history in process memory. This is not durable across restarts and is not shared across multiple worker processes.

These findings are from static repository inspection. They do not establish which command the Twilio sandbox currently reaches.

## Required verification

Before changing the deployed entrypoint or webhook URL:

1. Inspect the hosting service's configured build and start commands.
2. Inspect the deployed service's recent startup logs, with secrets redacted.
3. Confirm the deployed commit SHA and branch.
4. Confirm the Twilio sandbox webhook URL and HTTP method without changing them.
5. Send one controlled test message only after confirming the sandbox target and test account.
6. Record the observed response and relevant redacted logs.

Do not infer the live entrypoint from README instructions or from the presence of a Python file.

## Immediate stabilisation priorities

1. Establish the actual deployed entrypoint and preserve the existing sandbox configuration.
2. Initialise the Twilio client from environment configuration and fail safely when required configuration is missing.
3. Validate incoming Twilio webhook signatures using the official Twilio request validator and the externally visible request URL.
4. Make webhook processing idempotent using the provider message SID.
5. Persist candidate transactions and require user confirmation before committing financial records.
6. Enforce authenticated ownership on financial-summary endpoints; do not expose records by accepting an arbitrary phone number in a URL.
7. Remove unvalidated loan eligibility/credit-score outputs from user-facing flows.
8. Add automated tests for signature validation, duplicate delivery, transaction confirmation, persistence and access control.

## Security note: tracked database file

The default branch contains a tracked file named `smartliving.db` even though database files are listed in `.gitignore`. Its contents have not been inspected as part of this investigation.

Treat this as a potential data exposure until its contents and provenance are verified. Do not assume that adding the filename to `.gitignore` or deleting it in a future commit removes copies from Git history. If it contains real personal or financial data, restrict repository access immediately, assess exposure, and plan history cleanup and any required notifications with appropriate advice.

## Change-control boundary

- Do not change the Twilio sandbox webhook URL or credentials during this investigation.
- Do not deploy untested changes.
- Do not merge to `main` without review.
- Keep runtime fixes small, independently testable and covered by automated tests.
