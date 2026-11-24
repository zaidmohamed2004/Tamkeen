# ADR-003: Keep disability data in a separate encrypted Sensitive Store reached only through the Consent Module

In short: disability data goes in its own encrypted database, and only one module is allowed to touch it.

| Field | Content |
|---|---|
| ADR number & title | ADR-003: Keep disability data in a separate encrypted Sensitive Store reached only through the Consent Module |
| Status | Accepted |
| Date & deciders | 2026-11-21; Zaid Mohamed Abdelrahman, Layal Ahmed Moussa, Mark Hany Elia, Sara Raef Abdelsalam, Youssef Sameh Elbendary |
| Context | Law 151/2020 treats health data as sensitive and needs explicit consent; its Executive Regulations (Ministerial Decision 816/2025) add licensing for cross-border transfer and 72-hour breach notification. The Quota Module must still know who is a verified PwD. ASR-1, QAS-3. |
| Alternatives considered | **1. Disability fields inside the profiles collection**<br>Pros: Simplest model and queries.<br>Cons: One forgotten projection leaks the data; every module that reads profiles is in scope for the law.<br>**2. Do not store disability data at all**<br>Pros: Nothing to protect.<br>Cons: Quota Module cannot count verified PwD hires; FR-08 fails.<br>**3. Separate database tamkeen_vault, own DB user, AES-256-GCM field encryption, Consent Module as the only door**<br>Pros: Small, auditable surface; other modules see only a boolean; tamper detection from the GCM auth tag.<br>Cons: Extra module and key management; joins become service calls. |
| Decision | Sensitive data (verified status, encrypted disability status, card files, consents) lives in database tamkeen_vault in the same Atlas cluster, with its own database user whose credentials only the Consent Module loads. Fields are encrypted in the application with AES-256-GCM. Other modules get isVerifiedPwd(uid) as a boolean. Card files are deleted when the verifier decides. |
| Rationale | It meets QAS-3 with the smallest exposure the free tier allows (Atlas Free does not support customer-managed encryption keys), and it makes the 24-hour purge after consent withdrawal a single-module job. |
| Consequences | Positive:<br>+ Employer views can never contain disability data because no employer-facing module can read it.<br>+ Contract tests and an audit trail cover one module.<br>+ Purge after withdrawal is simple (purgeAfter field + scheduled job).<br>Negative:<br>- Key lives in an environment variable; leak or loss is serious (risk R5).<br>- Same cluster as the Main Database, so a cluster-level breach exposes encrypted data (still encrypted).<br>- Real disability data stored abroad would need a PDPC licence; M3 uses synthetic data only (C-B2). |
