<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       11-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 11

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta
- SPRINT_GOAL: Make the Catalog journey observable end to end: trace map, structured log contract, instrumentation code with an automated test and a metric catalog (week 11 workshop, delivery 1).
<!-- CONFIG-END -->

> Sprint window: Oct 19 - Oct 25, 2026 (in progress, report as of Oct 19)

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-CAT-001 | Browse product catalog: critical journey and trace map for the visitor who opens the shop (api-gateway, catalog-api, MongoDB) | doing | https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/26f23d7 |
| HU-CAT-001 | Structured log contract of the Catalog journey: fields, domain fields, never-log list and seven lines of one trace | doing | https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/94b46b1 |
| HU-CAT-001 | Instrumentation of catalog-api in Python: trace-context middleware, structured logger, context propagated to MongoDB, two metrics and six automated tests | done | https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/0b6fbc8 |
| HU-CAT-001 | Golden signals and metric catalog of catalog-api and api-gateway, with cardinality and histogram buckets | done | https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/683a74d |

## 2. My individual contribution

### Week 11 workshop, delivery 1 (`11-week/workshop/`)
- CP0: folder and README with the CONFIG block and the part of the project I work on, the Catalog side (45d149f).
- CP1: critical journey and trace map, with the hop table, a Mermaid sequence diagram and the span tree (26f23d7, 9db87ab).
- CP2: structured log contract with the eleven required fields, the domain fields, the never-log list, the log levels and seven JSON lines of one trace (94b46b1).
- CP3: `catalog_api_obs`, a Python module for `catalog-api` with no dependencies. First push: trace-context middleware and structured logger (546beff). Second push: metrics and the trace context sent to MongoDB in the `comment` of the command (922d535), and six tests, one of which proves that the `trace_id` received is the `trace_id` sent downstream, plus `HOW-TO-RUN.md` with the real console output (0b6fbc8).
- CP4: golden signals, cardinality of every label and latency buckets justified by what a visitor expects (683a74d).

### Decisions taken
- The journey is the one of the Catalog service only: `catalog-api` depends on no other domain service, and the checkout of `sales-api` is the one that is interrupted when `catalog-api` is down.
- The trace context travels to MongoDB in the `comment` of the command, because MongoDB has no headers.
- Labels of the metrics are bounded: the route template instead of the URL, and three outcomes.

## 3. Blockers and risks
- The first versions of CP0, CP1 and CP2 described the checkout of Sales. They are being rewritten to the Catalog journey, each in its own push, after the delivery closed.
- The asynchronous hop of the journey (`StockDepleted` to `notification-service`) is the target design of the team docs: the outbox and RabbitMQ are not built yet.

## 4. Plan for next week
- Rewrite CP0, CP1 and CP2 so that the whole workshop describes the Catalog journey.
- Delivery 2: SLOs and error budget, burn-rate alerts, runbook and the incident drill, all for the Catalog journey.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Workshop folder: https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop
- Instrumentation and its test: https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop/03-instrumentation
