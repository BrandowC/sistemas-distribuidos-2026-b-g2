<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       05-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 05

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta
- SPRINT_GOAL: Package and publish the individual evidence of weeks 1-4 in the fork and get the Cut 1 backlog (clinic and scheduling stories) ready for the next sprint. Low-activity week: no commits to the code or docs repos.
<!-- CONFIG-END -->

> Sprint window: Sep 7 - Sep 13, 2026

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-CLIN-001 | Register a pet - analysis and planning for Cut 1 | todo | No commit yet; implemented in week 06 |
| HU-SCHED-001 | Book an appointment within business hours - analysis and planning for Cut 1 | todo | No commit yet; implemented in week 06 |

## 2. My individual contribution

### Course deliverables
- Published the session reports for weeks 1-4 (six PDFs plus the week 03 and week 04 example diagrams) to the fork, and removed the superseded PDR drafts of weeks 1-2 (commit 6ef29d6, Sep 10).
- Prepared Cut 1 (clinic side of Amaranta): reviewed the Clinical and Scheduling user stories in `04-requirements/user-stories.md`, the domain rules and the data model to scope which stories belong to Cut 1 and which bounded contexts to add to the monolith. The implementation followed in week 06.

### Honest status
- There are no commits in `amaranta` or `amaranta-shop-docs` dated in this window. The sprint goal was only partially met: the delivery pipeline of the fork moved forward, product work did not.

## 3. Blockers and risks
- No product work was committed this week, which weakens the group sprint (board and backlog evidence) for week 05.
- No daily/board evidence of the Cut 1 planning was recorded, so it cannot be demonstrated beyond the user-stories document.

## 4. Plan for next week
- Implement Clinical and Scheduling with staff RBAC (Cut 1) and merge it through a PR into `develop`.
- Add repository governance: CODEOWNERS and the Git conventions the course requires.
- Record planning, daily and review notes in the board each sprint so the ceremonies leave evidence.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Fork delivery commit (session reports weeks 1-4): https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2/commit/6ef29d6
- Code repo: https://github.com/BrandowC/amaranta
- Docs repo: https://github.com/code-corhuila/amaranta-shop-docs
- Fork: https://github.com/BrandowC/sistemas-distribuidos-2026-b-g2
- Profile repo (CONFIG): https://github.com/BrandowC/BrandowC
