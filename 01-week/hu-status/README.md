<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.

     Your weekly grade is read AUTOMATICALLY from this file:
       01-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 01

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->

- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM:
- SPRINT_GOAL: Set up the individual delivery pipeline (profile repo CONFIG + fork) and establish the Week 01 foundations: distributed system models, logical time, the consistency spectrum and delivery semantics (Session 1); DDD, hexagonal architecture, resilience patterns and the per-environment Git flow (Session 2).
<!-- CONFIG-END -->

## 1. User stories worked this week

| HU ID      | Title                                                                                                       | Status (todo/doing/done) | Evidence (PR or commit URL) |
| ---------- | ----------------------------------------------------------------------------------------------------------- | ------------------------ | --------------------------- |
| HU-001-001 | Session 1 - Study distributed system and failure models, logical time and causality                         | done                     |                             |
| HU-001-002 | Session 1 - Position core operations on the consistency spectrum (CAP/PACELC) and choose delivery semantics | doing                    |                             |
| HU-001-003 | Session 2 - Set up profile repo CONFIG block and fork with 01-week/hu-status/README.md                      | doing                    |                             |
| HU-001-004 | Session 2 - Apply DDD and hexagonal boundaries to the MVP 1 domain draft                                    | todo                     |                             |
| HU-001-005 | Session 2 - Create the team `docs` repo, write ADR-001 (architecture style) and draft the MVP 1 backlog     | todo                     |                             |

## 2. My individual contribution

### Session 1 - Distributed systems: models, time, consistency and trade-offs

- Studied what changes when crossing a process boundary: loss of shared memory/state, of a single clock, and of all-or-nothing failure. Reviewed the 8 fallacies of distributed computing and adopted the inverse of each as a design assumption.
- Reviewed system models (synchronous vs asynchronous) and the failure-model ladder crash-stop -> crash-recovery -> omission -> Byzantine. Positioned our target system at crash-recovery + omission over an asynchronous network; Byzantine tolerance is not justified by our threat model.
- Worked through logical time: Lamport's happens-before (->) as the source of ordering instead of wall-clock time. Noted the limit that L(a) < L(b) does not prove a -> b, which requires vector clocks.
- Mapped the consistency spectrum (linearizable -> sequential -> causal -> eventual) and applied CAP/PACELC per operation rather than per system: money-like operations strong, profile/catalog causal (read-your-writes), metrics and counters eventual.
- Reviewed replication and partitioning with quorums, verifying the R + W > N rule (N=3, W=2, R=2 -> 4 > 3) so a read overlaps the latest write.
- Reviewed consensus: FLP impossibility and why practical systems use timeouts/randomization; Raft as the teachable leader + replicated-log protocol committing on majority ACK.
- Compared synchronous (REST/gRPC) vs asynchronous (Kafka/RabbitMQ) communication and the delivery guarantees at-most-once / at-least-once / exactly-once, concluding that exactly-once _delivery_ is a myth and the practical goal is exactly-once _processing_ via idempotency key + deduplication.
- Reasoned through the "Place order during a partition" scenario: no single ACID transaction across Orders/Inventory/Payments, no blocking on a DB lock waiting for Payments, a Saga with compensation (release stock) on charge failure, an idempotency key on the charge so a retry after the partition heals does not double-charge, and an honest pending state shown to the user.
- Completed the Session 1 self-check (7/7).

### Session 2 - Professional engineering foundations for distributed systems

- Adopted the executable-standards mindset: a standard that does not fail the build is only a comment; "MVP" reduces scope, never standards.
- Applied strategic DDD (bounded contexts such as Orders, Payments and Inventory as natural service boundaries, with context mapping) and tactical DDD (entities, value objects, aggregates as the single mutation/consistency boundary, and past-tense domain events).
- Applied hexagonal architecture with real ports and adapters, enforcing the dependency rule adapters -> application -> domain, and using the smell test that a domain file importing an ORM/driver is a violation.
- Reviewed SOLID where it bites in services (SRP, DIP via injected adapters, OCP/ISP with small specific ports) and Clean Code rules: honest names, small functions, no dead TODO/FIXME, wrapped errors instead of swallowed ones.
- Studied the resilience patterns to apply from MVP 1: Circuit Breaker, Retry with backoff and jitter, Timeout/Bulkhead, Saga, Outbox and CQRS.
- Defined the testing strategy: test at the cheapest level that gives confidence, unit + integration + e2e per feature, contract tests for producer/consumer compatibility, testcontainers for real-DB integration, and honest reporting where declared coverage never exceeds measured.
- Internalized the ways of working: weekly sprints over a prioritized backlog of user stories with testable acceptance criteria, DoR before starting, and a DoD that includes runtime validation.
- Set up the per-environment HU branch model (from develop cut hu-xxx-dev and PR to develop; repeat for qa and main) and confirmed no PR ever skips an environment. Configured the `upstream` remote to the group repo to receive instructor material without conflicts.
- Completed the Session 2 self-check (8/8).

## 3. Blockers and risks

- TEAM is not yet defined, so HU-001-005 (team `docs` repo, ADR-001 and MVP 1 backlog) cannot start until the team is formed and the real problem to solve is picked.
- The profile repo `BrandowC/BrandowC` with the CONFIG block must exist and match this file exactly; without a correct match the automation reads the delivery as "nothing delivered". Highest-priority risk of the week.
- The long-lived environment branches `develop` and `qa` do not exist yet in the fork; only `main` is present, so the per-environment HU flow cannot be exercised end to end and no PR evidence URLs exist yet.
- Risk of under-specifying consistency and delivery semantics per operation before MVP 1: choosing them late tends to force redesign, since a decision like strong consistency on inventory decrement changes the architecture, not just the code.

## 4. Plan for next week

- Create/verify the profile repo `BrandowC/BrandowC` with the CONFIG block and confirm FULL_NAME and GITHUB_USER match this file character for character.
- Create the `develop` and `qa` environment branches and run one HU through the full per-environment flow (hu-xxx-dev -> develop, then qa, then main) to produce real PR evidence URLs.
- Form the team, pick the real problem the distributed system will solve, and open the `docs` repo as source of truth.
- Write ADR-001 (chosen architecture style) and draft the MVP 1 backlog with testable acceptance criteria.
- For each core operation of MVP 1, document its required consistency level and delivery semantics, ready to defend in the MVP 1 design.
- Fill in the Evidence links section and the empty Evidence column of section 1 with the resulting commit/PR URLs.

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
- Course material (OVAs): https://code-corhuila.github.io/ova-web/2026-B/distribuidos/
- Session 1 - Distributed systems: models, time, consistency and trade-offs (Week 1, Unit 1 - Foundations, Corte 1)
- Session 2 - Professional engineering foundations for distributed systems (Week 1)
- Week 01 example diagram, animated (both sessions): ./week-01-example.svg (static preview: ./week-01-example.png)
- Preliminary Design Review (PDR) - MVP 1 design intent: ./PDR.md
- Profile repo CONFIG (`BrandowC/BrandowC`): pending - see section 3
- HU branch PRs: pending - `develop`/`qa` branches not created yet
- PDR: https://claude.ai/code/artifact/b9b2fcb6-5416-4ed3-90be-87918b7ef296
