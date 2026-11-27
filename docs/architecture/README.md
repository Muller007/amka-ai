# AMKA Architecture v2.0

**Status:** Target architecture approved for design; implementation is incremental and subject to repository validation.  
**Primary application:** `amka-ai`  
**Related frontend:** `Muller007/amka-finance`

## Mission

AMKA helps people understand their money, make informed financial decisions, build financial stability, and progressively improve their lives.

## Approved product decisions

1. **Unified identity:** one internal AMKA identity per person, with multiple independently verified channel identities.
2. **AMKA Invest is education-first:** teach financial understanding and decision-making; do not begin as an investment-product marketplace.
3. **Accessible learning:** support voice, visual, text, interactive, and practical conversational learning.
4. **Transparent commercial model:** disclose fees, commissions, sponsorships, partner relationships, and material conditions. Educational content remains independent of commercial influence.
5. **Empowerment as success:** measure financial understanding, decision capability, visibility, resilience, and independence—not engagement or revenue alone.

See [ADR-0001: Product principles](decisions/ADR-0001-product-principles.md).

## Architectural principles

- The financial ledger and deterministic domain services are the source of truth; AI is an assistant, not an authority.
- AI may propose structured interpretations. Ambiguous financial events require clarification or user confirmation before posting.
- Financial records must be persistent, traceable, correctable, and attributable to their source.
- A phone number is a channel identifier, not a permanent person identifier.
- Personal and business contexts must be separated by explicit workspaces and permissions.
- Access to financial data is least-privilege and purpose-limited.
- Educational content is structured, versioned, reviewed, and auditable.
- Commercial offers are distinguishable from education and disclose material incentives.
- Security, privacy, accessibility, and user control are cross-cutting requirements.
- Prefer a modular monolith while the product and operating model are being validated. Do not introduce microservices without demonstrated need.

## Target logical modules

- Identity, channel linking, recovery, consent, and access control
- Channel adapters and conversation orchestration
- Transaction interpretation and confirmation
- Financial events, ledger, activities, and reporting
- Deterministic financial intelligence and scenario analysis
- AMKA Invest learning content, delivery, simulations, and comprehension
- Commercial relationships, disclosures, and recommendation governance
- Integrations, notifications, administration, audit, and observability

## Technology direction

The current implementation is Python/Flask with SQLAlchemy and a SQLite default. Preserve working code while stabilising it. PostgreSQL is the target persistent database for multi-user deployment, with schema changes managed through migrations. A framework migration to FastAPI is not a prerequisite; decide only after the domain boundaries and operational requirements are clear.

## Delivery approach

1. Establish a reproducible baseline and protect sandbox credentials/data.
2. Stabilise webhook validation, message delivery, persistence, authentication, and financial correctness.
3. Introduce unified identity and channel verification.
4. Implement durable financial events and ledger semantics.
5. Add deterministic financial intelligence and activity-aware reporting.
6. Build AMKA Invest as an accessible, governed learning engine.
7. Add commercial governance and partner controls.
8. Connect the frontend to authenticated APIs and accessible learning experiences.

## Important boundary

This document describes the approved target direction, not a claim that these capabilities already exist. See [repository audit](repository-audit.md) for observed implementation gaps. Validate every change with tests and a reviewable pull request.
