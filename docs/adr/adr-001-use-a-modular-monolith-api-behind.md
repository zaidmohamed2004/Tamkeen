# ADR-001: Use a modular monolith API behind a single-page web app (client-server)

In short: one API with clear modules inside it, plus a separate web app. It's the only setup that fits our free hosting and still keeps the sensitive parts walled off.

| Field | Content |
|---|---|
| ADR number & title | ADR-001: Use a modular monolith API behind a single-page web app (client-server) |
| Status | Accepted |
| Date & deciders | 2026-11-20; Zaid Mohamed Abdelrahman, Layal Ahmed Moussa, Mark Hany Elia, Sara Raef Abdelsalam, Youssef Sameh Elbendary |
| Context | We need one structure that serves the web app and the Tamkeen mobile app (ASR-3), keeps disability data behind a clear boundary (ASR-1), and still wakes up fast on a free host that sleeps after 15 minutes idle (ASR-5). The team is five part-time students (C-O1) on free tiers only (C-T3). Drivers: QAS-3, QAS-5, QAS-7, QAS-8. |
| Alternatives considered | **1. Layered monolith (one app, layers only)**<br>Pros: Simplest to start; one deploy; one cold start.<br>Cons: No module boundaries, so sensitive fields and company checks spread across the code (bad for ASR-1, ASR-4).<br>**2. Modular monolith (one deployable, modules that own their data)**<br>Pros: One process to wake and keep warm; clear boundaries; modules can be split out later.<br>Cons: One failure point; boundaries only hold if we enforce them in code review and lint rules.<br>**3. Service-based or microservices (3+ deployables)**<br>Pros: Strong isolation; Sensitive Store could live in its own service.<br>Cons: Three sleeping services means three cold starts, and 750 free instance hours cannot keep more than one awake; hire-to-quota becomes a distributed transaction. |
| Decision | One Tamkeen API deployable built as a modular monolith (Express 5, Node.js 22), plus a separate React web app. Each business module owns its collections; other modules call its service interface, never its collections. |
| Rationale | It scored highest in the weighted style matrix (80 of 100, section 2.2). It is the only option that meets ASR-5 on the free tier while still giving the boundaries ASR-1 and ASR-4 need. |
| Consequences | Positive:<br>+ One instance to wake and keep warm; fits 750 free hours a month.<br>+ Module boundaries match the Data view ownership matrix and can be checked automatically (dependency-cruiser rule in M3).<br>+ Easy to plug into the wider Tamkeen platform through the same REST API.<br>Negative:<br>- A crash takes the whole API down (mitigated by drafts and retries, ADR-005).<br>- Boundary rules need tooling and review discipline.<br>- Scaling is all-or-nothing until a module is split out. |
