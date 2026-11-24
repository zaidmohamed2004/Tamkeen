# ADR-005: Protect submissions with client drafts, retry with backoff and idempotency keys

In short: the free server sleeps, so the app saves your answers on your device and retries safely without ever sending an application twice.

| Field | Content |
|---|---|
| ADR number & title | ADR-005: Protect submissions with client drafts, retry with backoff and idempotency keys |
| Status | Accepted |
| Date & deciders | 2026-11-22; Zaid Mohamed Abdelrahman, Layal Ahmed Moussa, Mark Hany Elia, Sara Raef Abdelsalam, Youssef Sameh Elbendary |
| Context | The free API sleeps after 15 minutes idle and takes about a minute to wake. QAS-5 requires 0 lost and 0 duplicated applications and a completed submit within 90 seconds of wake. Users with cognitive or visual disabilities must not be left guessing (QAS-1, QAS-2). |
| Alternatives considered | **1. Keep the API awake only (Uptime Monitor ping)**<br>Pros: No client changes.<br>Cons: Does not cover restarts, deploys or exhausted free hours; a lost request is still lost.<br>**2. Paid always-on instance**<br>Pros: Removes cold starts.<br>Cons: Breaks the free-tier constraint C-T3.<br>**3. Draft Store in the browser + API Client retry with exponential backoff + Idempotency-Key checked by an Idempotency Filter**<br>Pros: Covers sleep, restart and network drops; retries cannot create duplicates; user always sees a status message.<br>Cons: More client code; idempotency_keys collection with a 24 h TTL index. |
| Decision | The Web App saves every form to the Draft Store (IndexedDB) with a UUID Idempotency-Key, retries POSTs after timeouts and 5xx with backoff (2, 4, 8, 16, 30, 30 s, up to 120 s) while polling GET /health, and announces progress through an aria-live region. The Idempotency Filter stores the response per key for 24 h and replays it on repeats. We also keep the Uptime Monitor ping to reduce cold starts. |
| Rationale | Only this option meets every response measure of QAS-5 without paying for hosting, and it improves usability by never losing a user's answers. |
| Consequences | Positive:<br>+ 0 lost and 0 duplicated applications by design.<br>+ Same mechanism protects every POST, not only applications.<br>+ Clear spoken feedback during waits.<br>Negative:<br>- More moving parts in the client; needs good tests.<br>- A key reused with a different body must be rejected (409), which the client must handle.<br>- Drafts on a shared device could be seen by the next user; drafts are cleared on sign-out. |
