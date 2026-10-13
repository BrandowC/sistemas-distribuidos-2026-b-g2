<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       09-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 09

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta
- SPRINT_GOAL: Prepare the MVP 2 extraction and its platform: record ADR-010..013 and the Sales checkout spec, harden the monolith (atomic stock reservation, idempotent release, checkout compensation, scheduling slots, public pet history, web screens) and bring up the infrastructure repositories (PostgreSQL, MongoDB, observability, security base).
<!-- CONFIG-END -->

> Sprint window: Oct 5 - Oct 11, 2026 (current week, report as of Oct 9)

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-CAT-002 | Atomic stock reservation, idempotent release and product deletion (admin catalog) | done | https://github.com/BrandowC/amaranta/pull/14 |
| HU-SALES-001 | Checkout compensates reserved stock when the order fails | done | https://github.com/BrandowC/amaranta/pull/11 |
| HU-SCHED-001 | Validate business hours and expose available slots | done | https://github.com/BrandowC/amaranta/pull/10 |
| HU-CLIN-001 | Public pet medical history, pets directory and symptoms | done | https://github.com/BrandowC/amaranta/pull/12 |
| HU-WEB-001 | Reception, clinic and public pet screens with slot picker | done | https://github.com/BrandowC/amaranta/pull/15 |
| N/A (infra) | amaranta-shop-infra-postgres: single PostgreSQL instance, observability stack and PR/board tracking | done | https://github.com/code-corhuila/amaranta-shop-infra-postgres/pull/2 , /pull/3 , /pull/1 |
| N/A (infra) | amaranta-shop-infra-mongo: single MongoDB instance with one user per domain | done | https://github.com/code-corhuila/amaranta-shop-infra-mongo/pull/2 , /pull/1 |
| N/A (infra) | amaranta-shop-security: service base and design record (ADR-011) | done | https://github.com/code-corhuila/amaranta-shop-security/pull/2 , /pull/1 |

## 2. My individual contribution

### Docs (`amaranta-shop-docs`) - 4 branches pushed
- ADR-010 (database engine per domain: Sales on PostgreSQL, Catalog on MongoDB) and ADR-011 (identity design with token revocation) - commit https://github.com/code-corhuila/amaranta-shop-docs/commit/e909129.
- ADR-012 (stack of extracted services) and ADR-013 (monolith first, strangler fig) - commit https://github.com/code-corhuila/amaranta-shop-docs/commit/7279efe.
- `specs/checkout.md`: single-capability Sales checkout spec with stories, 15 business rules traced to tests, contract changes of the extraction, cutover and an executable definition of done - commit https://github.com/code-corhuila/amaranta-shop-docs/commit/bccf2ed.
- Recorded the checkout stock compensation in the Sales API decisions (6f6990a) and linked the code repo and the spec from the README, fixing stale repo names (ded0bbc).

### Code (`amaranta` repo) - one branch per HU, pushed on Oct 8 and merged into develop on Oct 9
- Catalog: reserve now uses a conditional UPDATE (stock >= qty) so two concurrent reservations cannot take the last unit; release is an idempotent compensating increment; added product deletion, image upload and a concurrency spec (32862eb, fd757e1; branch `hu-cat-002-dev`).
- Sales: checkout releases the reservation when the aggregate rejects the order or persisting fails; added shop-hours and walk-in customer value objects (bdd83bd; branch `hu-sales-001-dev`).
- Scheduling: availability respects business hours and conflicts through the repository port; new get-available-slots use case (94559a3; branch `hu-sched-dev`).
- Clinical: public pet history with an optional JWT guard, pets directory and symptoms on medical records, migration V010 (d26b05f; branch `hu-clin-dev`).
- Web: reception, clinic and public pet screens with QR code and the appointment slot picker (cffbbf4; branch `hu-web-dev`).
- Pull requests: https://github.com/BrandowC/amaranta/pull/14 (HU-CAT-002), https://github.com/BrandowC/amaranta/pull/11 (HU-SALES-001), https://github.com/BrandowC/amaranta/pull/10 (HU-SCHED-001), https://github.com/BrandowC/amaranta/pull/12 (HU-CLIN-001) and https://github.com/BrandowC/amaranta/pull/15 (HU-WEB-001) were merged into `develop` on Oct 9 after code-owner review.
- Repo hygiene: ignored JWT keys, tsbuildinfo and local tooling files; merged into `develop` through PR https://github.com/BrandowC/amaranta/pull/13 (47d721b) and promoted to `qa` with `git cherry-pick -x` (de414d0, branch `chore-gitignore-qa`, merged into `qa` through PR #16 on Oct 9).

### Infrastructure and security repositories (`code-corhuila` organisation) - 9 commits, 8 PRs merged into develop
- `amaranta-shop-infra-postgres`: PR template and board tracking so every PR cites its user story (5b2cef9, PR #1); one PostgreSQL 16 instance with an idempotent bootstrap, one login user per domain, one environment file per environment and the Annex J privilege self-check, tested in CI by running the bootstrap twice (34abe55, b553892, PR #2); OpenTelemetry collector, Prometheus and Grafana (a1671f0, PR #3).
- `amaranta-shop-infra-mongo`: the same PR template and board tracking (c071837, PR #1); one MongoDB 7.0 instance with one database and one user per domain restricted to its own database, with CI proving the user cannot write outside it (c29529f, dd0ec0c, PR #2).
- `amaranta-shop-security`: PR template (461a6fe, PR #1) and the minimum content of a code repository plus the README that records the token design of ADR-011: lifetimes, rotating refresh token and revocation (9bb9598, PR #2). The implementation is explicitly pending its own spec.
- CI fix: replaced fixed throwaway passwords with random per-run values and renamed a bootstrap variable, so the secret-scanning audit of the norm has no false positives (b553892, dd0ec0c).

## 3. Blockers and risks
- The five HU branches are in `develop`, but they are not promoted to `qa` and `main` yet; promotion has to be done by `git cherry-pick -x` through `qa/...` and `release/...` branches, with the `qa` branch name conflict still open with the teacher.
- The docs PRs of the checkout spec (#14), ADR-012/013 (#16) and housekeeping (#17) were merged into `main` on Oct 12, after the week closed; the ADR-010/011 branch is still pending review.
- The infrastructure and security repositories were merged into `develop` only; `main` of those repositories is still the empty scaffold until the release PR.
- The Catalog engine decision (MongoDB, ADR-010) is a course requirement but is not implemented yet; the Catalog read service of the monolith still uses PostgreSQL.
- Commit `84439b6` of week 07 has a malformed message (a shell here-doc was committed as the subject); history cannot be rewritten under the norm, so it is justified here.

## 4. Plan for next week
- Promote the five HUs merged into `develop` to `qa` and then to `main` through `qa/...` and `release/...` branches with `git cherry-pick -x`.
- Get the ADR-010/011 branch of the docs repo reviewed and merged.
- Start the extracted Sales service following `specs/checkout.md`, using the PostgreSQL instance of `amaranta-shop-infra-postgres`.
- Cut the first release (`release/1.0.0`) with the five elements required by norm 11.3 and publish the version tag after teacher approval.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- ADR-010/011: https://github.com/code-corhuila/amaranta-shop-docs/commit/e909129
- ADR-012/013: https://github.com/code-corhuila/amaranta-shop-docs/commit/7279efe
- Checkout spec: https://github.com/code-corhuila/amaranta-shop-docs/commit/bccf2ed
- Sales API decisions update: https://github.com/code-corhuila/amaranta-shop-docs/commit/6f6990a
- Housekeeping: https://github.com/code-corhuila/amaranta-shop-docs/commit/ded0bbc
- Catalog reservation: https://github.com/BrandowC/amaranta/commit/32862eb and https://github.com/BrandowC/amaranta/commit/fd757e1
- Checkout compensation: https://github.com/BrandowC/amaranta/commit/bdd83bd
- Scheduling slots: https://github.com/BrandowC/amaranta/commit/94559a3
- Clinical public history: https://github.com/BrandowC/amaranta/commit/d26b05f
- Web screens: https://github.com/BrandowC/amaranta/commit/cffbbf4
- HU PRs merged into develop: https://github.com/BrandowC/amaranta/pull/14 , https://github.com/BrandowC/amaranta/pull/11 , https://github.com/BrandowC/amaranta/pull/10 , https://github.com/BrandowC/amaranta/pull/12 , https://github.com/BrandowC/amaranta/pull/15
- Gitignore PRs: https://github.com/BrandowC/amaranta/pull/13 (develop) , https://github.com/BrandowC/amaranta/pull/16 (qa)
- Docs PRs merged on Oct 12: https://github.com/code-corhuila/amaranta-shop-docs/pull/14 , https://github.com/code-corhuila/amaranta-shop-docs/pull/16 , https://github.com/code-corhuila/amaranta-shop-docs/pull/17
- Infra PostgreSQL PRs: https://github.com/code-corhuila/amaranta-shop-infra-postgres/pull/1 , /pull/2 , /pull/3
- Infra MongoDB PRs: https://github.com/code-corhuila/amaranta-shop-infra-mongo/pull/1 , /pull/2
- Security PRs: https://github.com/code-corhuila/amaranta-shop-security/pull/1 , /pull/2
- Full list of commits and PRs per week: ./commits-week-09.md (in this folder)
- Code repo: https://github.com/BrandowC/amaranta
- Docs repo: https://github.com/code-corhuila/amaranta-shop-docs
- Profile repo (CONFIG): https://github.com/BrandowC/BrandowC
