<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       07-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 07

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta
- SPRINT_GOAL: Documentation-first week: publish the OpenAPI contract of each service (week 08 course topic: API contract spec), close the Sales and Catalog contract gaps, fix repo hygiene (author attribution, dev -> develop, ADR-007 palette), and start the RS256 JWT migration required by the course norm.
<!-- CONFIG-END -->

> Sprint window: Sep 21 - Sep 27, 2026

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-SALES-001 | Close the Sales error-response contract (guest checkout, real error shapes) | done | https://github.com/code-corhuila/amaranta-shop-docs/commit/1853cd5 |
| HU-CAT-001 | Catalog service OpenAPI contract | done | https://github.com/code-corhuila/amaranta-shop-docs/commit/5054827 |
| HU-CLIN-001 | Clinical and scheduling database schemas (migrations) | done | https://github.com/BrandowC/amaranta/commit/5249937 |
| HU-IAM-002 | Login - sign JWT with RS256 instead of HS256 (ADR-009) | doing | https://github.com/BrandowC/amaranta/commit/524a088 |
| HU-SCHED-001 | Scheduling OpenAPI contract (documented with real endpoints) | done | https://github.com/code-corhuila/amaranta-shop-docs/commit/5054827 |

## 2. My individual contribution

### Docs (`amaranta-shop-docs`) - 5 PRs merged to main
- Documented `07-api` with the real contracts of Auth, Catalog, Sales, Clinical, Scheduling and the gateway, plus API guidelines and authentication notes (commit 5054827); translated the OpenAPI files to English (ee88276; PR https://github.com/code-corhuila/amaranta-shop-docs/pull/9).
- Closed the Sales error-response contract with a decisions document (1853cd5; PR https://github.com/code-corhuila/amaranta-shop-docs/pull/10).
- Added ADR-007 (Fiery Ocean brand palette, 7daf944; PR https://github.com/code-corhuila/amaranta-shop-docs/pull/6), corrected author attribution across ADRs (74ffccd, 2e64049; PR https://github.com/code-corhuila/amaranta-shop-docs/pull/7) and renamed `dev` to `develop` in the Git conventions (ad42a41; PR https://github.com/code-corhuila/amaranta-shop-docs/pull/8).
- Wrote ADR-008 (JWT signing and token lifecycle) and ADR-009 (RS256 per course norm) and updated `authentication.md` and the auth OpenAPI (c2699a5, Sep 27).

### Code (`amaranta` repo) - PRs into develop
- Added the clinical and scheduling schemas (5249937; PR https://github.com/BrandowC/amaranta/pull/3) and updated the project documentation with the domain flow diagram and the extraction plan for clinical/scheduling (6b615be; PR https://github.com/BrandowC/amaranta/pull/7).
- Opened and merged CODEOWNERS PRs for `develop`, `qa` promotion and the qa promotion (PRs https://github.com/BrandowC/amaranta/pull/4, https://github.com/BrandowC/amaranta/pull/5).
- Implemented RS256 signing in Identity: RSA key pair, algorithm pinned to RS256 on sign and verify, `scripts/dev-keys.sh`, keys ignored by git (524a088, Sep 27). Review/merge happens next week.

## 3. Blockers and risks
- ADR-009 exists because the MVP signed JWTs with HS256, which the course norm forbids; this was found late and cost a re-work of Identity.
- The Catalog contract needed a second pass (gap analysis) because the first version described endpoints the monolith did not expose.
- The RS256 PR is waiting for review by the code owner, so HU-IAM-002 is not done yet.

## 4. Plan for next week
- Get the RS256 PRs (docs and code) reviewed and merged.
- Prepare the MVP 2 extraction decisions: engine per domain, identity design with revocation, stack of the extracted services.
- Write a spec for the Sales checkout before touching the code.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- API contracts commit: https://github.com/code-corhuila/amaranta-shop-docs/commit/5054827
- Sales contract gaps PR: https://github.com/code-corhuila/amaranta-shop-docs/pull/10
- ADR-009 commit (RS256): https://github.com/code-corhuila/amaranta-shop-docs/commit/c2699a5
- RS256 code commit: https://github.com/BrandowC/amaranta/commit/524a088
- Schemas PR: https://github.com/BrandowC/amaranta/pull/3
- Docs PRs merged: https://github.com/code-corhuila/amaranta-shop-docs/pull/6, https://github.com/code-corhuila/amaranta-shop-docs/pull/7, https://github.com/code-corhuila/amaranta-shop-docs/pull/8, https://github.com/code-corhuila/amaranta-shop-docs/pull/9, https://github.com/code-corhuila/amaranta-shop-docs/pull/10
- Code PRs merged: https://github.com/BrandowC/amaranta/pull/3, https://github.com/BrandowC/amaranta/pull/4, https://github.com/BrandowC/amaranta/pull/5, https://github.com/BrandowC/amaranta/pull/7
- Code repo: https://github.com/BrandowC/amaranta
- Docs repo: https://github.com/code-corhuila/amaranta-shop-docs
- Profile repo (CONFIG): https://github.com/BrandowC/BrandowC
