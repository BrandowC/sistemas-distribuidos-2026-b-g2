<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       13-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 13

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta-shop (Group 2)
- SPRINT_GOAL: Threat model the internal stock endpoints between sales-api and catalog-api and turn it into security stories.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| W13-CP0 | Claim the trust boundary and start the workshop | done | https://github.com/code-corhuila/amaranta-shop-docs/issues/34 , https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/7678d6b44725905f89c8aadd5f8576aa26620461 |
| W13-CP1 | Attack surface map and trust boundaries of Amaranta Shop | done | https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/118faf54b71f1726d9a50c7d4124f82a0bf6b028 |
| W13-CP2 | STRIDE analysis of the sales-api to catalog-api internal stock endpoints | doing | https://github.com/code-corhuila/amaranta-shop-docs/pull/36 |
| W13-CP3 | Three security stories in the team backlog | done | https://github.com/code-corhuila/amaranta-shop-docs/issues/37 , https://github.com/code-corhuila/amaranta-shop-docs/issues/38 , https://github.com/code-corhuila/amaranta-shop-docs/issues/39 , https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/cc0c8e989e60e99edb2d0fd99ac5a89c0d6c95a3 |
| W13-CP4 | Security gates and a negative authorization test | done | https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/c5c90a747856c2b36662443470d8db82fef2e592 |

## 2. My individual contribution
- I claimed the boundary between `sales-api` and `catalog-api` (issue #34): the internal routes `POST /internal/products/reserve-stock` and `release-stock`.
- I drew the data flow, the trust boundaries, the assets and the entry points (`01-attack-surface.md`).
- I wrote the STRIDE analysis in the team docs, with six threats, their risk and a ranking (pull request #36, left open for review).
- I opened three `[security]` stories with acceptance criteria: callers of the internal routes (#37), an idempotent release tied to a reservation (#38) and a bound on the size of an internal request (#39).
- I wrote the security gates (`security.yml`) and one negative authorization test for the internal routes of `catalog-api`.

## 3. Blockers and risks
- The record of the library visit and the citation of the library book are still pending; they will be added to the STRIDE analysis and to one story.
- The negative test fails today against `catalog-api` on purpose: the control it checks, a shared secret on the internal routes, does not exist yet.

## 4. Plan for next week
- Answer the review comment on pull request #36, finish the residual risk and the references.
- Run the negative test against the real `catalog-api` and record the console output.
- Add the library record and the book citation.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Workshop folder: https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/tree/main/13-week/workshop
- STRIDE pull request: https://github.com/code-corhuila/amaranta-shop-docs/pull/36
- Claim issue: https://github.com/code-corhuila/amaranta-shop-docs/issues/34
- Security stories: https://github.com/code-corhuila/amaranta-shop-docs/issues/37 , https://github.com/code-corhuila/amaranta-shop-docs/issues/38 , https://github.com/code-corhuila/amaranta-shop-docs/issues/39
