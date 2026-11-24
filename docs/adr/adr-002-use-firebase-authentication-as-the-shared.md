# ADR-002: Use Firebase Authentication as the shared identity provider

| Field | Content |
|---|---|
| ADR number & title | ADR-002: Use Firebase Authentication as the shared identity provider |
| Status | Accepted |
| Date & deciders | 2026-11-20; Zaid Mohamed Abdelrahman, Layal Ahmed Moussa, Mark Hany Elia, Sara Raef Abdelsalam, Youssef Sameh Elbendary |
| Context | Sign-in must be shared with the Tamkeen mobile app (C-T2) and every request must carry a verifiable identity (QAS-3, QAS-4, QAS-8). We must not build password storage ourselves. |
| Alternatives considered | **1. Own JWT with bcrypt password hashes**<br>Pros: Full control, no external dependency.<br>Cons: More security code for students to get right; separate accounts from the mobile app.<br>**2. Self-hosted Keycloak**<br>Pros: Open source, standards-based, strong features.<br>Cons: Heavy Java service; another always-on container that the free tier cannot keep awake.<br>**3. Firebase Authentication (Spark plan)**<br>Pros: Same account as the Flutter app; free; SDKs for web and mobile; local emulator for tests.<br>Cons: External dependency; not open source; Spark limits (3,000 daily active users, 100 new accounts per IP per hour). |
| Decision | Users sign in with Firebase Authentication. The Auth Guard verifies the ID token on every request with firebase-admin. Roles and company membership live in our users and company_members collections, not in token claims. |
| Rationale | It is the only option that gives one account across Tamkeen with no extra container to keep awake, and it keeps credential storage out of our code. |
| Consequences | Positive:<br>+ No password storage in our system.<br>+ Same identity for web and mobile clients (QAS-8).<br>+ Firebase Auth emulator makes tests and load tests independent of Spark limits.<br>Negative:<br>- Vendor lock-in for identity.<br>- Spark limits: 100 accounts per IP per hour can block a class demo from one campus network (risk R8).<br>- Short-lived tokens must be refreshed by both clients. |
