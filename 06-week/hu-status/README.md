<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       06-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 06

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta
- SPRINT_GOAL: Complete the Cut 1 backlog by adding the Clinical Records and Scheduling bounded contexts with staff role-based access, and put repository governance (CODEOWNERS, Git conventions, brand palette) in place.
<!-- CONFIG-END -->

> Sprint window: Sep 14 - Sep 20, 2026

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-CLIN-001 | Register a pet | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |
| HU-CLIN-002 | Veterinarian adds a medical record | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |
| HU-SCHED-001 | Book an appointment within business hours | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |
| HU-SCHED-002 | Prevent double-booking | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |
| HU-SCHED-003 | Cancel my appointment | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |
| HU-SCHED-004 | Receptionist manages appointments for a customer | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |
| HU-IAM-003 | Receptionist registers a walk-in customer (role-based access added) | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |
| HU-CAT-002 | Admin manages the catalog (create, update, stock, activate/deactivate) | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |
| HU-SALES-003 | Receptionist creates an in-store order and marks it as paid | done | https://github.com/BrandowC/amaranta/commit/fb799f6 |

## 2. My individual contribution

### Code (`amaranta` repo)
- Added the two remaining bounded contexts, Clinical Records and Scheduling, with domain invariants for business hours and double-booking (commit fb799f6, 96 files; PR https://github.com/BrandowC/amaranta/pull/2 into `develop`).
- Introduced role-based authorization (RolesGuard + @Roles). Before this change every staff-only endpoint was reachable by any authenticated user.
- Fixed a bug where `OrderRepository.save()` re-inserted order items on every update (e.g. mark as paid), which caused a NOT NULL violation; updates now touch only the order columns.
- Opened and merged the CODEOWNERS PR so `main` requires approval (PR https://github.com/BrandowC/amaranta/pull/1, commit 2a9dcd2).
- Documented the circular dependency between Clinical and Scheduling (resolved with forwardRef) and how it would be broken at extraction time.

### Docs (`amaranta-shop-docs`)
- Extended the Git conventions (cherry-pick promotion, no direct commits to permanent branches) and redefined the colour palettes in the design system (commit f38b69a; PR https://github.com/code-corhuila/amaranta-shop-docs/pull/5).
- Adopted the course branching policy and CODEOWNERS added by the instructor (75785f5, 3ac0250) and reformatted the repo README tables (b90b384).

### Flow
- Used feature branches with PRs into `develop` and a promotion PR to `qa` and `main` for the governance change, instead of committing directly to permanent branches.

## 3. Blockers and risks
- The Cut 1 PR was large (96 files) and combined two contexts plus RBAC, which makes review harder; it should have been split per HU.
- Branch names used `feat/...` instead of the per-environment `hu-xxx-dev` convention, and no automated test report is attached to the PR.
- Clinical and Scheduling depend on each other, which couples them until they are extracted.

## 4. Plan for next week
- Contract-first documentation: publish the OpenAPI contract of every service in `07-api`.
- Fix author attribution and the `dev` -> `develop` rename in the governance docs.
- Add the clinical and scheduling database schemas and keep PRs small and per HU.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Cut 1 backlog (clinical, scheduling, RBAC), commit: https://github.com/BrandowC/amaranta/commit/fb799f6
- Cut 1 PR into develop: https://github.com/BrandowC/amaranta/pull/2
- CODEOWNERS PR: https://github.com/BrandowC/amaranta/pull/1
- Git conventions + palette PR (docs): https://github.com/code-corhuila/amaranta-shop-docs/pull/5
- Docs commit: https://github.com/code-corhuila/amaranta-shop-docs/commit/f38b69a
- Code repo: https://github.com/BrandowC/amaranta
- Docs repo: https://github.com/code-corhuila/amaranta-shop-docs
- Profile repo (CONFIG): https://github.com/BrandowC/BrandowC
