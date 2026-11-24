# ADR-007: Use rule-based, explainable matching and an in-process cache for job search

| Field | Content |
|---|---|
| ADR number & title | ADR-007: Use rule-based, explainable matching and an in-process cache for job search |
| Status | Accepted |
| Date & deciders | 2026-11-23; Zaid Mohamed Abdelrahman, Layal Ahmed Moussa, Mark Hany Elia, Sara Raef Abdelsalam, Youssef Sameh Elbendary |
| Context | QAS-6 needs 95% of searches under 1.5 s with 100 concurrent users, but Atlas Free allows 100 operations per second and 0.5 GB of storage. FR-10 needs a match score with plain reasons. Sending profiles to an external AI service would move sensitive data abroad. |
| Alternatives considered | **1. LLM or embedding-based matching through a cloud AI API**<br>Pros: Smarter matching.<br>Cons: Sends personal data abroad; cannot explain itself in plain words; free quotas are small.<br>**2. No cache, database query per search**<br>Pros: Always fresh.<br>Cons: 100 concurrent users would hit the 100 ops/s throttle.<br>**3. Rule-based score (accommodations cover needs + skill overlap) and Search Cache with 60 s TTL, paginated to 20**<br>Pros: Explainable; cheap; keeps load under the Atlas throttle.<br>Cons: Less clever matching; results can be up to 60 s stale. |
| Decision | The Matching Module computes score and reasons from accommodations and skills. The Jobs Module reads search pages through a read-through Search Cache (in-memory LRU, 60 s TTL, 500 entries), with compound indexes on city, remote and accommodations. |
| Rationale | It is the only option that meets QAS-6 within the free database limits while keeping matching explainable and data in our system. |
| Consequences | Positive:<br>+ Most repeated searches never reach the database.<br>+ Reasons are readable aloud by screen readers.<br>+ No personal data leaves the platform.<br>Negative:<br>- Cache is per instance and lost on restart (first searches after wake are slower).<br>- New jobs can take up to 60 s to appear in search.<br>- Matching quality is basic; can be improved later behind the same interface. |
