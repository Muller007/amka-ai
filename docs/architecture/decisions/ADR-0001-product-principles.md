# ADR-0001: AMKA Product Principles and Architectural Commitments

- **Status:** Accepted
- **Date:** 2026-11-27
- **Decision owners:** AMKA product founder
- **Scope:** All AMKA channels, backend modules, data processing, user experiences, and commercial relationships

## Context

AMKA is intended to help people understand their money, make informed financial decisions, build financial stability, and progressively improve their lives. The product must be credible, accessible, privacy-conscious, and designed to empower users rather than exploit financial vulnerability or create dependency.

The following five decisions are confirmed product direction and must shape system design.

## Decision 1 — One identity per person

AMKA will maintain one internal identity per person, with multiple independently verified channel identities.

Consequences:
- Internal user IDs are stable and are not phone numbers.
- WhatsApp numbers, web credentials, and future app credentials are separate channel identities linked to the user.
- Linking and unlinking channels requires secure verification, audit events, and recovery safeguards.
- Phone-number control does not establish legal identity.
- Number reassignment must never transfer prior financial records to a new number holder.
- Shared business channels require explicit workspace roles and permissions; access to a shared number does not grant access to personal financial records.
- Personal and business workspaces remain distinct, with explicit access grants.

## Decision 2 — AMKA Invest is education-first

AMKA Invest will initially teach financial understanding and decision-making. It is not initially an investment-product marketplace.

Consequences:
- Lessons begin with everyday concepts and first principles.
- Education covers income, expenses, profit, cash flow, saving, debt, resilience, risk, inflation, liquidity, diversification, and compounding.
- Interactive scenarios teach trade-offs without putting real money at risk.
- The system checks understanding through teach-back and practical choices, not clicks alone.
- Educational material is structured, versioned, reviewed, and auditable.
- Education must be distinguished from regulated financial advice and product recommendations.
- Any future regulated service requires separate legal, regulatory, risk, and operational approval.

## Decision 3 — Multimodal accessibility

AMKA will support voice, visual, text, interactive, and practical conversational learning.

Consequences:
- Learning content should be authored independently of a single presentation format where practical.
- Explanations should use plain language, familiar examples, and optional repetition or alternative explanations.
- Language support claims must be backed by evaluation on representative real-world financial language.
- The system must not equate limited literacy or unfamiliarity with financial terminology with limited intelligence or decision-making ability.
- Accessibility and user choice are requirements, not decorative additions.

## Decision 4 — Transparent commercial model

AMKA will disclose fees, commissions, sponsorships, partner relationships, and material conditions. Commercial relationships must not silently influence independent educational content.

Consequences:
- Education, commercial offers, and user decisions are separate product concerns.
- Offers identify the provider, material fees, conditions, risks, and any AMKA compensation.
- Sponsored content is labelled.
- Users can decline commercial offers without losing access to core education.
- Partner access to data is governed by purpose limitation, lawful basis, appropriate consent, and least privilege.
- No sale of identifiable financial records for lender or marketing purposes.
- Commercial recommendation governance and auditability are required before partner offers launch.

## Decision 5 — Empowerment defines success

AMKA aims to improve users' financial capability and independence.

Consequences:
- Success metrics include financial understanding, decision capability, financial visibility, resilience, and informed independence.
- Engagement, revenue, lending volume, and time spent are not sufficient measures of impact.
- A user becoming more capable and needing AMKA less often can be a positive outcome.
- AMKA explains calculations, uncertainty, and trade-offs rather than making opaque decisions for users.
- The product must not use shame, fear, artificial urgency, or dependency to drive engagement or revenue.

## Cross-cutting engineering rules

1. The ledger and deterministic financial services are the source of truth; AI output is a proposal until validated and, where needed, confirmed.
2. Financial data is persistent, attributable, correctable, and auditable.
3. Access is authenticated, authorised, least-privilege, and purpose-limited.
4. Users receive understandable explanations of what data is collected and why.
5. Privacy, security, accessibility, and transparency apply across all modules.
6. The initial implementation should remain a modular monolith unless evidence justifies a more distributed architecture.

## Rejected alternatives

- One account per phone number: rejected because people use multiple numbers and channels.
- Investment marketplace as the initial Invest product: rejected because education and decision capability come first.
- Text-only education: rejected because it excludes users who prefer voice, visual, or practical learning.
- Undisclosed commissions or partner influence: rejected because it undermines trust.
- Engagement and monetisation as sole success measures: rejected because they can conflict with user empowerment.

## Review conditions

Revisit this ADR only if the product owner explicitly changes a decision or new legal, safety, or operational evidence requires a more protective implementation. Any change must preserve AMKA's mission and be documented with rationale and impact.
