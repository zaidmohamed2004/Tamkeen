# ADR-006: Store quota rules as versioned data in the Quota Module

| Field | Content |
|---|---|
| ADR number & title | ADR-006: Store quota rules as versioned data in the Quota Module |
| Status | Accepted |
| Date & deciders | 2026-11-23; Zaid Mohamed Abdelrahman, Layal Ahmed Moussa, Mark Hany Elia, Sara Raef Abdelsalam, Youssef Sameh Elbendary |
| Context | Article 22 of Law 10/2018 sets 5% for employers with 20 or more workers, but rounding is not specified and the rule may change. QAS-7 requires a rule change in 10 minutes with no code change and no redeploy, and past months must keep their results. |
| Alternatives considered | **1. Constants in code**<br>Pros: Simplest.<br>Cons: Every change needs a code change and redeploy; fails QAS-7.<br>**2. General rules engine library**<br>Pros: Very flexible.<br>Cons: Overkill for three numbers; new concepts for the team to learn.<br>**3. quota_rules collection with version, percent, minHeadcount, rounding and effectiveFrom**<br>Pros: Admin changes a rule through the API; history kept; easy to test.<br>Cons: Admin endpoint must be well protected; a wrong rule affects every dashboard. |
| Decision | The Quota Module owns quota_rules. Each snapshot records the rule version it used. Admins add a new version through POST /v1/admin/quota-rules; the module picks the version in force for each month. |
| Rationale | Defer binding time to run time with the simplest structure that keeps history, and keep all rule logic in one cohesive module. |
| Consequences | Positive:<br>+ Meets QAS-7 with zero code changes.<br>+ Audit trail of who changed which rule.<br>+ Rounding assumption (round up) is data, easy to change if the instructor or law says otherwise.<br>Negative:<br>- A mistaken rule version changes every dashboard from its effective date until fixed.<br>- Admin role becomes high value; must be protected by Access Policy and audit. |
