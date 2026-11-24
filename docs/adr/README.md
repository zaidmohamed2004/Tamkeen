# Architecture decisions

These are the main decisions we made while designing Tamkeen for Milestone 2. Each one follows the ADR template from the course brief (Appendix A), so every file has the context, the options we looked at, what we picked and what it costs us.

If you only read one, read ADR-001. It explains the overall structure, and the rest build on it.

| ADR | Decision | Status |
|---|---|---|
| [ADR-001](adr-001-use-a-modular-monolith-api-behind.md) | Use a modular monolith API behind a single-page web app (client-server) | Accepted |
| [ADR-002](adr-002-use-firebase-authentication-as-the-shared.md) | Use Firebase Authentication as the shared identity provider | Accepted |
| [ADR-003](adr-003-keep-disability-data-in-a-separate.md) | Keep disability data in a separate encrypted Sensitive Store reached only through the Consent Module | Accepted |
| [ADR-004](adr-004-send-email-through-the-brevo-http.md) | Send email through the Brevo HTTP API using a transactional outbox | Accepted |
| [ADR-005](adr-005-protect-submissions-with-client-drafts-retry.md) | Protect submissions with client drafts, retry with backoff and idempotency keys | Accepted |
| [ADR-006](adr-006-store-quota-rules-as-versioned-data.md) | Store quota rules as versioned data in the Quota Module | Accepted |
| [ADR-007](adr-007-use-rule-based-explainable-matching-and-an.md) | Use rule-based, explainable matching and an in-process cache for job search | Accepted |
