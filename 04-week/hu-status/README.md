<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       04-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 04

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta
- SPRINT_GOAL: Deliver the first running slice of Amaranta: a hexagonal modular monolith (Identity, Catalog, Sales) over PostgreSQL with customer registration, login, product browsing and checkout, plus the UX/UI foundations (design system, navigation map, wireframes).
<!-- CONFIG-END -->

> Sprint window: Aug 31 - Sep 6, 2026

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-IAM-001 | Customer self-registration (POST /auth/register) | done | https://github.com/BrandowC/amaranta/commit/20cf133 |
| HU-IAM-002 | Login - issues the JWT required by checkout (support endpoint) | done | https://github.com/BrandowC/amaranta/commit/20cf133 |
| HU-CAT-001 | Browse product catalog (GET /products) | done | https://github.com/BrandowC/amaranta/commit/20cf133 |
| HU-SALES-001 | Add to cart and checkout (POST /orders, GET /orders) | done | https://github.com/BrandowC/amaranta/commit/20cf133 |

## 2. My individual contribution

### Code - walking skeleton of the product (`amaranta` repo)
- Built and committed the initial MVP as a modular monolith with NestJS + TypeORM + PostgreSQL 16: three bounded contexts (`identity`, `catalog`, `sales`), each with its own PostgreSQL schema and a domain / application / infrastructure layout (commit 20cf133, 116 files; most of the volume is the generated lockfile).
- Applied the hexagonal dependency rule: domain has no framework imports, use cases implement inbound ports, and `sales` reaches `catalog` only through an outbound port plus an adapter (stock reservation), so the context can be extracted later.
- Wrote pure domain unit tests (`*.spec.ts`, Product and Order entities, plus the checkout use case) that do not boot Nest or touch a database.
- Documented the structure, the HU table and the extraction path in the repo README and `docs/path-to-microservices.md`.

### Docs (`amaranta-shop-docs`)
- Authored the UX/UI foundations: design system, navigation map and wireframes (commit 9db8e3b, `12-ux-ui/`).

### Course deliverables
- Wrote the Sprint 4 session reports (Session 1: layered service + walking skeleton, Aug 31; Session 2: contract-first planning, MoSCoW and Definition of Done, Sep 3) - see `./Semana-04-Amaranta-Sesion1.pdf` and `./Semana-04-Amaranta-Sesion2.pdf`.

## 3. Blockers and risks
- The MVP is a monolith, while the Session 1 report planned a standalone `ordenes-service`; the extraction path is documented but not executed yet.
- The first MVP landed directly on `main`/`develop`/`qa` as one commit, so there are no per-environment HU branches or PRs as evidence for these four HUs.

## 4. Plan for next week
- Add the Clinic bounded contexts (Clinical Records and Scheduling) so the MVP covers both the shop and the veterinary clinic.
- Add role-based authorization (staff vs customer) because every endpoint is currently open to any authenticated user.
- Start working with per-environment HU branches and PRs (hu-xxx-dev -> develop).

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Initial MVP commit (code repo): https://github.com/BrandowC/amaranta/commit/20cf133
- UX/UI foundations (docs repo): https://github.com/code-corhuila/amaranta-shop-docs/commit/9db8e3b
- Session reports: ./Semana-04-Amaranta-Sesion1.pdf, ./Semana-04-Amaranta-Sesion2.pdf
- Code repo: https://github.com/BrandowC/amaranta
- Docs repo: https://github.com/code-corhuila/amaranta-shop-docs
- Fork: https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2
- Profile repo (CONFIG): https://github.com/BrandowC/BrandowC
