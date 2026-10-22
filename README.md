# Tamkeen

Inclusive employment and 5% quota compliance platform.

**Team:** Success Enablers
**Course:** CSE4203 Principles of Software Architecture, AASTMT (Fall 2026)
**Instructor:** Dr. Nada Mahmoud Hassan · **TA:** Eng. Mohamed Fareh

| Member | Student ID |
|---|---|
| Layal Ahmed Moussa | 231006574 |
| Mark Hany Elia | 231006804 |
| Sara Raef Abdelsalam | 231015069 |
| Youssef Sameh Elbendary | 231006239 |
| Zaid Mohamed Abdelrahman | 231006511 |

## What is Tamkeen?

Egypt's Law No. 10 of 2018 says any company with 20 or more employees has to give at least 5% of its jobs to persons with disabilities (PwDs). Many companies don't, or they hire people "on paper" and pay them to stay home. On the other side, most job sites don't work well with a screen reader, and a lot of forms ask for a diagnosis.

Tamkeen is a job platform for PwDs in Arabic and English. Job seekers list their skills and what they need to work well (a screen reader, step-free access, written instructions). We never ask for a diagnosis. Companies post jobs and say which accommodations they offer, and the platform matches the two. When a company hires a verified PwD, its quota dashboard updates: a company of 120 employees needs 6, so with 2 verified the dashboard shows a gap of 4.

The features are simple. What makes the architecture interesting is the trade-offs: security against usability (no CAPTCHAs or short time-outs for screen-reader users), privacy of disability data under Law 151/2020, and availability on free hosting that sleeps when idle.

## Milestones

| Milestone | What it covers | Status |
|---|---|---|
| M1 | Proposal and architectural requirements | Submitted 23 Oct 2026 |
| M2 | Software Architecture Document | Upcoming |
| M3 | Architectural prototype | Upcoming |
| M4 | Architecture evaluation and final presentation | Upcoming |

## Repository structure

```
.
├── README.md
├── successEnablers_tamkeen.pdf     # Milestone 1 document
└── diagrams/
    ├── context.mmd                 # Figure 1: C4 Level 1 system context
    └── utility-tree.mmd            # Figure 2: utility tree
```

## Diagrams

The diagram sources are Mermaid files. GitHub renders the copies below, and you can also open any `.mmd` file in [mermaid.live](https://mermaid.live) to view or edit it.

### Figure 1: System context (C4 Level 1)

Dark blue boxes are people, the blue box is our system, and grey boxes are external systems. Dashed arrows are optional (Could priority).

```mermaid
flowchart LR
  seeker["<b>Job seeker with disability</b><br/>[Person]<br/>visual, hearing, mobility, cognitive"]
  coach["<b>Job coach / family helper</b><br/>[Person, optional]"]
  hr["<b>Employer HR</b><br/>[Person]"]
  admin["<b>Admin / verifier</b><br/>[Person]"]
  sys["<b>Tamkeen</b><br/>[Software system]<br/>Inclusive employment and<br/>5% quota compliance platform"]
  idp["<b>Firebase Authentication</b><br/>[External system]<br/>identity provider"]
  mail["<b>Brevo email service</b><br/>[External system]"]
  app["<b>Tamkeen mobile app</b><br/>[External system]<br/>other accessibility pillars"]
  seeker -->|builds profile, searches, applies<br/>HTTPS| sys
  coach -.->|helps, with permission<br/>HTTPS| sys
  hr -->|posts jobs, reviews candidates,<br/>tracks quota - HTTPS| sys
  admin -->|verifies companies<br/>and PwD status - HTTPS| sys
  sys -->|verifies ID tokens<br/>HTTPS| idp
  sys -->|sends status emails<br/>SMTP| mail
  app -->|reads jobs and profiles<br/>REST/JSON over HTTPS| sys
  classDef person fill:#08427b,stroke:#052e56,color:#ffffff
  classDef system fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8a8a8a,stroke:#6b6b6b,color:#ffffff
  class seeker,coach,hr,admin person
  class sys system
  class idp,mail,app external
```

### Figure 2: Utility tree

Each scenario is rated (Importance, Difficulty) with H, M or L. Full six-part scenarios are in section 5 of the M1 PDF.

```mermaid
flowchart LR
  U(("<b>Utility</b><br/>Tamkeen"))
  U --> US[Usability]
  U --> SE[Security]
  U --> AV[Availability]
  U --> PE[Performance]
  U --> MO[Modifiability]
  U --> IO[Interoperability]
  US --> u1["QAS-1: Blind user applies with screen reader and keyboard; 0 serious axe errors, ≤ 15 min<br/><b>H, H</b>"]
  US --> u2["QAS-2: Easy-read user applies in ≤ 6 screens, ≤ 10 min<br/><b>H, M</b>"]
  SE --> s1["QAS-3: Employer views never return disability data; 100% of contract tests pass<br/><b>H, H</b>"]
  SE --> s2["QAS-4: Cross-company requests 100% denied and logged within 1 s<br/><b>H, M</b>"]
  AV --> a1["QAS-5: Server asleep: 0 applications lost, submit completes ≤ 90 s after wake<br/><b>M, H</b>"]
  PE --> p1["QAS-6: 95% of job searches < 1.5 s with 100 concurrent users<br/><b>M, M</b>"]
  MO --> m1["QAS-7: Quota rule change in ≤ 10 min, 0 code changes, 0 redeploys<br/><b>M, M</b>"]
  IO --> i1["QAS-8: Mobile app requests 100% correctly processed; invalid tokens 100% rejected and logged<br/><b>H, H</b>"]
  classDef root fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef qa fill:#dbe8f6,stroke:#1168bd,color:#0b2540
  classDef leaf fill:#ffffff,stroke:#8a8a8a,color:#1a1a1a
  class U root
  class US,SE,AV,PE,MO,IO qa
  class u1,u2,s1,s2,a1,p1,m1,i1 leaf
```

## Tech stack (planned)

MERN (MongoDB, Express, React, Node.js), Firebase Authentication for sign-in shared with the wider Tamkeen platform, and Brevo for email. Everything runs on free tiers.
