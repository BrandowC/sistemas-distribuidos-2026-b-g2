<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       10-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 10

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta
- SPRINT_GOAL: Start the MVP 2 extraction on the new service repositories: merge the week 09 decisions into main, build and merge the Sales and Catalog database repositories, implement the Sales API against its spec, and open the MVP 2 release flow (qa, release branch, main) in the monolith repository.
<!-- CONFIG-END -->

> Sprint window: Oct 12 - Oct 18, 2026 (in progress, report as of Oct 13)

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| N/A (docs) | Sales checkout spec, ADR-012/013 and housekeeping merged into main of the documentation repository | done | https://github.com/code-corhuila/amaranta-shop-docs/pull/14 , /pull/16 , /pull/17 |
| HU-SALES-001 | Sales database: Flyway runner, sales schema, checkout tables, idempotency key, roles and grants, rebuild check on every PR | done | https://github.com/code-corhuila/amaranta-shop-sales-db/pull/1 , /pull/2 , /pull/3 (merged into develop) |
| HU-CAT-001 | Catalog database (MongoDB): Liquibase runner, product collection with validator and indexes, seed of the ten products, roles and grants | done | https://github.com/code-corhuila/amaranta-shop-catalog-db/pull/1 , /pull/2 , /pull/3 (merged into develop) |
| HU-SALES-001 | Sales API (Java 21): domain, application ports, HTTP layer with RS256 and error envelope, PostgreSQL and Catalog adapters, container image | doing | 29 commits d23ffe2 ... 4a3d20c on 21 local one-task branches of https://github.com/code-corhuila/amaranta-shop-sales-api (not pushed yet) |
| N/A (release) | MVP 2 release flow in the monolith repository: qa sync, release.md and changelog, release.2.0.0 branch | doing | https://github.com/BrandowC/amaranta/pull/19 , /pull/20 , /pull/21 , /pull/22 merged; /pull/23 (release.2.0.0 into main) open |
| N/A (repo base) | Minimum content of a code repository (norm 5.1) in the ten new service repositories | doing | 10 commits on branch chore/repo-base (pushed); PRs into develop pending |

## 2. My individual contribution

### Documentation (`amaranta-shop-docs`)
- Merged into `main` the pull requests of the Sales checkout spec (#14), ADR-012/013 (#16) and the housekeeping branch (#17) on Oct 12. The commits were written in week 09 (bccf2ed, 7279efe, ded0bbc, 6f6990a); merging them puts the decisions (Java for Sales, Python for Catalog, nginx gateway, monolith first) on `main`, where the service repositories can cite them.
- Replaced the placeholder authors of ADR-001 (commit 86da83f, branch `docs/fix-adr-001-authors`).

### Sales database (`amaranta-shop-sales-db`) - 3 PRs merged into develop
- `feat/sales-schema` (PR #1): Flyway runner reading DDL, DML, DCL and TCL as one version sequence (a537c8f), the `sales` schema with `orders` and `order_items` as the monolith created them (82b7448), a rebuild check that runs on every pull request (3e99fda) and the README (a24c0f2).
- `feat/sales-idempotency-key` (PR #2): `sales.idempotency_key` with an 8-128 character primary key and a foreign key to the order (RN-15), and the "my orders, newest first" index built CONCURRENTLY in its own migration (490b3a3), with a test and documentation (a4cb46c, f0b53b3).
- `feat/sales-roles-and-grants` (PR #3): `sales_reader` and `sales_writer` NOLOGIN roles, table-by-table grants (c544749), a test that logs in as the service user and checks every permission that must and must not exist (2c36d4c) and documentation (d52a60d).

### Catalog database (`amaranta-shop-catalog-db`) - 3 PRs merged into develop
- `chore/catalog-rebuild-check` (PR #1): Liquibase runner and the layout of the three families (bc1030c), the product collection with its validator and indexes (feb6b8f), a rebuild of the collections from empty on every pull request (74fa0bb) and documentation (2a6b2b5).
- `feat/catalog-seed-products` (PR #2): seed of the ten products under the ids the monolith issued (5de4c92), with a test that proves the seed leaves ten products and never resets a live stock (4e5c175) and documentation of the cutover caveat (24fdab9).
- `feat/catalog-roles` (PR #3): catalog roles and the grant to `catalog_app` (cc880c9), a test that logs in as the service user (a39f2c8) and documentation (3c2eed1).

### Sales API (`amaranta-shop-sales-api`) - 29 commits on 21 local one-task branches, not pushed yet
- Build and deploy: three Maven modules (core without Spring, adapters, app), composition root, container image, compose file and CI build (d23ffe2, aff79f5, ffb335a).
- Domain and application, test-first with a table that maps each rule of `specs/checkout.md` to the test that proves it: Money in whole pesos, shop hours of Bogota, the Order aggregate, placing an order reserving stock only after the rules that cannot fail, giving the stock back when the order cannot be saved, marking an order as paid and listing my orders (74805cf ... 65c79bc).
- HTTP layer: RS256 verification in the service with a closed list of algorithms, authentication on every `/api/` route with one declared guest exception, one error envelope with a correlation id, online order with or without an account, counter order for the receptionist only, mark as paid and list my orders (962d4a3 ... c2ce782).
- Persistence and integration: in-memory repository behind the same contract as the database, PostgreSQL repository connecting as `sales_app`, reserve and release through the internal endpoints of Catalog, wiring in the composition root and an end-to-end container test including the failure with Catalog down (e73a403, ab4d494, 3bf1664, 49440c3, 5d34163).

### Monolith repository (`amaranta`) - MVP 2 release flow
- Opened and merged the qa sync (PR #19) and the release documents `release.md` and changelog for v2.0.0 (commit 09eb5ba, PR #20) into `qa`, then promoted `qa` and the CODEOWNERS alignment (4a825bc) into the `release.2.0.0` branch (PRs #21 and #22). The release pull request into `main` (PR #23) is open and waits for teacher approval.

### Ten service repositories - repository base
- Added the commit `chore(repo): add the minimum content of a code repository` to api-gateway, front, worker, workflow, catalog-db, catalog-api, catalog-portal, sales-db, sales-api and sales-portal (gitignore, environment example, PR template citing the user story, board-tracking workflow, CI that guards what does not depend on the language, README with role, dependencies and stack).

### Decisions taken
- One version sequence per database repository, with the migration control table kept in the domain's own schema so that two database repositories never share it (Annex J, J.6); the compose file only runs the migrations because the instance lives in the infra repository.
- The tables and the seed keep the names and ids the monolith issued, so every migration is safe over the monolith's database and the Catalog seed never resets a live stock.
- The idempotency key is enforced by the database (primary key, length check, foreign key) so that the service writes the order and its key in one transaction and answers a retry with the order that already exists.
- Least privilege by construction: service users can only do what the spec allows (lines and keys insert-only, nothing deleted, migration history out of reach), and a test proves it by logging in as the service user.
- The Sales service verifies the RS256 token itself with a closed list of algorithms and keeps a single declared public exception (guest checkout), as ADR-009 and ADR-012 decided.
- Work is split into one branch per task, so every pull request stays small and cites a single concern.

## 3. Blockers and risks
- The 29 commits of the Sales API are only on 21 local branches. They have to be pushed and merged in order before their links resolve and before the HU can be `done`.
- The release pull request into `main` (PR #23) needs teacher approval; the tag is created only after the merge (norm 11.5).
- The ten `chore/repo-base` branches are pushed but their pull requests into `develop` are not merged yet.
- The week is not over, so every status in this report is as of Oct 13.

## 4. Plan for next week
- Push the Sales API branches and open the pull requests in order, each citing its user story.
- Configure the nginx gateway route for Sales with its single public exception for guest checkout.
- Start the Catalog API in Python and the portals, following ADR-010 and ADR-012.
- Merge the ten repository-base pull requests and publish the version tag after teacher approval.
- Update this report at the end of the week with the real pull requests and results.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Docs PRs merged on Oct 12: https://github.com/code-corhuila/amaranta-shop-docs/pull/14 , /pull/16 , /pull/17
- Sales database PRs: https://github.com/code-corhuila/amaranta-shop-sales-db/pull/1 , /pull/2 , /pull/3
- Catalog database PRs: https://github.com/code-corhuila/amaranta-shop-catalog-db/pull/1 , /pull/2 , /pull/3
- Monolith release flow PRs: https://github.com/BrandowC/amaranta/pull/19 , /pull/20 , /pull/21 , /pull/22 , /pull/23 (open)
- Sales API repository: https://github.com/code-corhuila/amaranta-shop-sales-api
- Full list of commits and PRs: ./commits-week-10.md (in this folder)
- Docs repo: https://github.com/code-corhuila/amaranta-shop-docs
- Profile repo (CONFIG): https://github.com/BrandowC/BrandowC
