# ADR-004: Send email through the Brevo HTTP API using a transactional outbox

| Field | Content |
|---|---|
| ADR number & title | ADR-004: Send email through the Brevo HTTP API using a transactional outbox |
| Status | Accepted (replaces the M1 assumption of SMTP) |
| Date & deciders | 2026-11-22; Zaid Mohamed Abdelrahman, Layal Ahmed Moussa, Mark Hany Elia, Sara Raef Abdelsalam, Youssef Sameh Elbendary |
| Context | M1 assumed SMTP to Brevo. Render's free web services block outbound ports 25, 465 and 587, so SMTP from the API is not possible on our host. Status emails are the main contact channel for deaf users and must not be lost when the API sleeps or restarts. QAS-5, FR-11. |
| Alternatives considered | **1. SMTP relay on port 2525 (Brevo supports it)**<br>Pros: Keeps the M1 design; port 2525 is not on Render's blocked list.<br>Cons: Unencrypted port per Brevo docs; depends on a port that could also be blocked later.<br>**2. Brevo HTTP API called directly inside the request**<br>Pros: Simple; HTTPS only.<br>Cons: If Brevo is slow or down, the user's request fails or the email is lost.<br>**3. Brevo HTTP API from an outbox collection, dispatched with retries**<br>Pros: Email survives restarts and Brevo outages; the user's request never waits on email.<br>Cons: One more collection and a dispatcher loop; emails can be delayed. |
| Decision | Modules write an outbox row in the same transaction as the business change. The Notifications Module dispatches pending rows to POST https://api.brevo.com/v3/smtp/email with the api-key header, retrying with backoff up to 8 attempts. |
| Rationale | It works on Render Free, keeps the request fast, and gives at-least-once delivery that does not depend on the API staying awake. |
| Consequences | Positive:<br>+ No dependency on SMTP ports.<br>+ No lost emails after a crash or spin-down; retries are automatic.<br>+ Same adapter interface lets local runs use a mail catcher.<br>Negative:<br>- Delivery is delayed while the API sleeps (the outbox drains on wake).<br>- At-least-once means a rare duplicate email; the event id is used to suppress repeats.<br>- Brevo Free allows 300 emails a day and adds Brevo branding. |
