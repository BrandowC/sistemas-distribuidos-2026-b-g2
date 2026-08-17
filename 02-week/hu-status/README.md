<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       02-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 02

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM:
- SPRINT_GOAL: Compare distributed architecture styles (client-server, P2P, layered/N-tier, SOA, microservices, event-driven) and their coupling/scaling/failure trade-offs (Session 1); map the domain into bounded contexts, walk the extraction decision path, and record the choice as ADR-001 (Session 2).
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-002-001 | Session 1 - Compare architecture styles and their coupling/scaling/failure trade-offs | done |  |
| HU-002-002 | Session 1 - Identify the distributed-monolith anti-pattern and its warning signs | done |  |
| HU-002-003 | Session 2 - Draw the context map for the MVP 1 domain | doing |  |
| HU-002-004 | Session 2 - Walk the extraction decision path and choose the MVP 1 architecture | doing |  |
| HU-002-005 | Session 2 - Write ADR-001 and slice the decision into sprint backlog stories | todo |  |

## 2. My individual contribution

### Session 1 - Distributed architectures: client-server, P2P, SOA, microservices
- Framed architecture as two questions answered together: how the system is split into parts (boundaries) and how those parts communicate (contracts). Fixed the rule that good boundaries follow business capability (a DDD bounded context), not technical layers, so a part can change and deploy on its own.
- Compared the six styles on fit and risk: client-server (simple, single bottleneck/SPOF), peer-to-peer (resilient, harder to coordinate and secure), layered/N-tier (classic business apps, risks becoming a distributed monolith if split badly), SOA (enterprise integration via an ESB, heavy middleware and a central bus), microservices (independent scale and deploy by capability, operational complexity), event-driven (decoupling and spikes, eventual consistency and harder debugging).
- Studied the microservices decomposition example: API Gateway in front of Orders/Payments/Inventory, each owning its own database, talking only through contracts (REST/gRPC/events) - no shared database. This is specifically what buys independent deploy and independent scale.
- Internalized the distributed-monolith anti-pattern as the classic failure: services are split but share a database and must deploy together, so the network cost is paid without shedding any of the coupling. If services cannot deploy independently, they are not microservices.
- Worked the "should we split the catalog" scenario: Catalog is a real bounded context with its own data and a real independent scaling need (Black Friday spikes), so it is extracted with its own read-optimized, cached store; Orders and Payments stay together because they are tightly coupled by a transaction, coordinated later with a Saga instead of an early split. Split for a measured reason, never for fashion.
- Catalogued the common mistakes to avoid: splitting by technical layer instead of capability, sharing one database across services, adding a message bus "because enterprise" when a direct call suffices, and skipping the ADR so nobody remembers why the architecture is the way it is.
- Completed the Session 1 self-check (6/6).

### Session 2 - Planning: architecture, bounded contexts and the ADR
- Adopted the planning loop for this course: refine the backlog -> decide (architecture, boundaries, contracts) -> record the decision (ADR) -> slice it into user stories with testable acceptance criteria for the sprint. A decision without an ADR is a rumor; a story without acceptance criteria is a wish.
- Drew the context map for the example domain before naming any service: Orders (cart, checkout) places into Payments (charge, refund) and reserves via Inventory (stock, reserve), which ships through Shipping (deliver, track). Boundaries follow language and data ownership, never database tables or UI screens.
- Walked the explicit extraction decision path instead of starting at "microservices": do parts need to scale/deploy independently? If no, stay as a modular monolith. If yes, are the boundaries real bounded contexts? If no, refactor the modules first; only if both are true, extract a service.
- Wrote ADR-001 (Context / Decision / Alternatives considered / Consequences) recording: modular monolith as the baseline, with Catalog-equivalent extracted as its own service because it is the only context with a real, measured independent scaling need. Rejected full microservices on day one (operational cost too high for current size/need) and a pure monolith (would waste resources scaling everything to handle one context's spikes).
- Confirmed the ADR immutability rule: an ADR is accepted and immutable; a later change is a new ADR that supersedes it, not an edit to adr-001.
- Reasoned through the "let's do 12 microservices on day one" scenario: refuted it with evidence - premature decomposition multiplies operational cost (deployment, tracing, versioned contracts, data consistency) with no scaling need yet - and proposed a modular monolith now plus an ADR listing the measured trigger required for each future extraction. Evidence-based disagreement is exactly the professional stance this course grades.
- Sliced the decision into a sprint-ready story: "As the team, we want the Catalog-equivalent module isolated behind a port so that it can later be extracted", with acceptance criteria - no other module imports its internals, all access goes through the port, tests pass.
- Completed the Session 2 self-check (6/6).

## 3. Blockers and risks
- TEAM is still not defined, so the context map and ADR-001 above are built on the course's illustrative domain (Orders/Payments/Inventory/Shipping), not the team's real product; both must be redone once the team and problem are set (carried over from Week 01, HU-001-005).
- Without a formed team there is no one to co-sign ADR-001 as a team decision; an individually authored ADR is a draft, not the artifact the course expects.
- The long-lived environment branches `develop` and `qa` still do not exist in the fork, so this week's HUs also have no real PR evidence URLs yet (same blocker as Week 01, not yet resolved).
- Risk of drawing the context map from database tables or UI screens out of habit instead of business language - the session explicitly calls this out as a common mistake, so the map needs a team review pass once real domain experts (teammates) are available.

## 4. Plan for next week
- Form the team and pick the real MVP 1 problem (still pending from Week 01); redraw the context map and rewrite ADR-001 against the real domain, replacing the illustrative one in this week's PDR.
- Get ADR-001 accepted as a team decision in the `docs` repo, not just an individual draft.
- Create the `develop` and `qa` branches and produce real PR evidence for at least one HU this cycle.
- Slice ADR-001's consequences into the first MVP 1 backlog stories with testable acceptance criteria, estimated and MoSCoW-prioritized.
- Identify, for the real domain, which bounded context (if any) has a measured independent-scaling trigger analogous to Catalog - only that one is a Week 3+ extraction candidate.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [ ] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Fork: https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2
- Group repo (upstream): https://github.com/code-corhuila/sistemas-distribuidos-2026-b-g2
- Session 1 - Distributed architectures: client-server, P2P, SOA, microservices (Week 2)
- Session 2 - Planning: choosing your architecture, bounded contexts and the ADR (Week 2)
- Week 02 example diagram, animated (both sessions): ./week-02-example.svg (static preview: ./week-02-example.png)
- Preliminary Design Review (PDR) - architecture decision path + ADR-001 draft: ./PDR.md
- ADR-001 (team-accepted version): pending - see section 3
- HU branch PRs: pending - `develop`/`qa` branches not created yet
