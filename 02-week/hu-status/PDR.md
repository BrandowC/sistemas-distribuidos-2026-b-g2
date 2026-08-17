# Preliminary Design Review (PDR) — Week 02

> **How to use this document.** The structure below is the deliverable; the content is a **worked
> example** built on the course's illustrative e-commerce domain (Orders / Payments / Inventory /
> Shipping, with Catalog as the scaling trigger from Session 1's own example), so every section
> shows what a defensible answer looks like. Once the team picks its real problem, redraw the
> context map and rewrite ADR-001 against the real domain — keep the structure and the decision
> path. Sections marked **[TEAM]** cannot be answered individually and are pending team formation.

| | |
| --- | --- |
| **Course** | Distributed Systems (cod. 82739) — 2026-B, Group 2 |
| **Week / Unit** | Week 02 · Session 1 (architecture styles) + Session 2 (planning) |
| **Author** | Brandow Stivent Claros Polania (`BrandowC`) |
| **Team** | **[TEAM]** — pending |
| **Status** | Preliminary — draft ADR, not yet team-accepted |
| **Builds on** | [Week 01 PDR](../../01-week/hu-status/PDR.md) — system model, consistency per operation, hexagonal core |

---

## 1. What this week adds

Week 01 fixed *how a request behaves* under failure — consistency per operation, the Saga, the
hexagonal core. Week 02 answers a different question: **how is the system cut into deployable
parts, and who talks to whom.** The two are independent decisions. A well-chosen architecture with
sloppy consistency still corrupts data; correct consistency semantics wrapped in the wrong service
boundaries still ships a distributed monolith.

---

## 2. Architecture styles — compared, not listed

A style is a bet about where coupling and failure live. The table states the bet, not just the name.

| Style | Where coupling lives | Fits when | Primary failure mode |
| --- | --- | --- | --- |
| Client-server | All clients depend on one server | Simple apps, one authority | Single bottleneck / SPOF |
| Peer-to-peer | Coordination itself | File sharing, blockchains, resilience-first | Coordination and security cost |
| Layered / N-tier | Between presentation, logic, data | Classic business apps | Becomes a distributed monolith if split badly |
| SOA | The ESB / message bus | Enterprise integration across orgs | Heavy central middleware |
| Microservices | The network, between capabilities | Independent scale and deploy per team | Operational complexity everywhere |
| Event-driven | Time — producers and consumers decouple | Spikes, audit, decoupling | Eventual consistency, harder debugging |

### The trap this table exists to prevent

**Distributed monolith.** Split into services that still share a database and must deploy
together: the network cost is paid, none of the coupling is shed. If services cannot deploy
independently, they are not microservices — regardless of how many repositories exist.

See [`week-02-example.svg`](./week-02-example.svg) for the context map and decision path below,
drawn out.

---

## 3. Context map — before naming a single service

Bounded contexts are drawn from **business language and data ownership**, never from database
tables or UI screens. Naming a service comes *after* this map, not before.

| Context | Owns | Language |
| --- | --- | --- |
| Orders | Cart, checkout | Order, Line, Confirm |
| Payments | Charge, refund | Charge, Authorize, Refund |
| Inventory | Stock, reserve | SKU, Reserve, Release |
| Shipping | Deliver, track | Shipment, Carrier, Tracking |
| Catalog | Product listing, search | Product, Listing, Price |

**Relations:** Orders *places into* Payments; Orders *reserves via* Inventory; Orders *ships
through* Shipping; Catalog is read by Orders but owned independently.

---

## 4. The decision path — walked, not assumed

The question is never "microservices or not." It is two sequential questions, and skipping either
one is how teams end up over-decomposed on day one.

1. **Does this context need to scale or deploy independently — for a real, measured reason?**
   If no → it stays inside the modular monolith.
2. **If yes: is the boundary real?** Does it already behave like its own bounded context, with its
   own language and data, or would extracting it just relocate shared-database coupling across a
   network? If the boundary is not real → refactor the module first. Only when **both** are true
   does a service get extracted.

### Applying it to this domain

| Context | Independent scaling need? | Boundary real? | Verdict |
| --- | --- | --- | --- |
| Catalog | **Yes** — Black Friday–class read spikes, rest of the shop stays flat | Yes — owns product data, read-optimized | **Extract** |
| Orders | No measured need yet | Tightly coupled to Payments by a transaction | Stay in the monolith |
| Payments | No measured need yet | Coupled to Orders | Stay in the monolith |
| Inventory | No measured need yet | Real context, but no scaling trigger | Stay in the monolith |
| Shipping | No measured need yet | Real context, but no scaling trigger | Stay in the monolith |

Orders and Payments are not merged for convenience — they are kept together because splitting them
today would force a distributed transaction with no scaling justification. That coupling gets
resolved later with the Saga from the Week 01 PDR, once (or if) a real reason to split emerges.

---

## 5. ADR-001 (draft — pending team acceptance)

```
# ADR-001: Initial architecture

Status: Proposed (individual draft — needs team acceptance)
Date:   2026-08-24

Context
  Five candidate bounded contexts (Orders, Payments, Inventory, Shipping,
  Catalog). Only Catalog has a real, measured independent-scaling need
  (traffic spikes decoupled from the rest of checkout).

Decision
  Start as a modular monolith. Extract Catalog as its own service,
  read-optimized with its own cache and datastore. Everything else stays
  in the monolith, module-separated behind ports.

Alternatives considered
  (a) Full microservices on day one
      Rejected: operational cost (deployment, tracing, versioned
      contracts, data consistency) is unjustified with no scaling need
      behind most contexts yet.
  (b) Pure monolith, no extraction
      Rejected: would force the whole system to scale to absorb
      Catalog's spikes, wasting resources on contexts that are flat.

Consequences
  + Catalog scales and deploys independently of checkout.
  + Team ships one deployable for everything else — lower ops cost now.
  - One cross-boundary call (Orders -> Catalog) to keep price/availability
    consistent at checkout time.
  - Revisit this ADR (a new ADR-00N, this one is immutable) if Orders and
    Payments ever need independent scaling — do not edit this file to
    change the decision.
```

**Why draft, not accepted.** An ADR records a *team* decision. Written individually, before the
team exists, this is a rehearsal of the reasoning — not the artifact the course grades. It becomes
real when the team reviews it against the actual product and co-signs it in the `docs` repo.

---

## 6. The scenario this design already refuses

A teammate proposes: *"Let's do 12 microservices from day one, that's how big companies do it."*

<div class="reject">The refutation, with evidence — not opinion</div>

- Premature decomposition multiplies operational cost — deployment, distributed tracing, versioned
  contracts, data spread across stores — **before** any context has demonstrated a real scaling or
  deploy-independence need.
- The correct response is not "no," it is a **modular monolith now** plus this ADR, which already
  states the measured trigger required for each future extraction (a demonstrated, independent
  scaling or deploy need — not a guess).
- Refuting a proposal with evidence, and proposing the disciplined alternative in writing, is
  exactly the professional stance this course grades — silently complying, or silently ignoring it,
  both fail that bar.

---

## 7. Sprint backlog slice

The ADR is not the deliverable by itself — it has to produce work the sprint can commit to.

| Story | Acceptance criteria |
| --- | --- |
| As the team, we want the Catalog module isolated behind a port so it can later be extracted | No other module imports Catalog internals; all access goes through the port; tests pass |
| As the team, we want Orders' calls to Catalog to go through a contract, not a direct import | Contract test exists between Orders and Catalog; breaking the contract fails CI |
| As the team, we want ADR-001 reviewed and accepted in the `docs` repo | ADR-001 has a team sign-off; status changes from Proposed to Accepted |

---

## 8. Risks

| # | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| R1 | Context map and ADR-001 are built on the illustrative domain, not the real product | **Blocking** | Redo both once the team and problem are set |
| R2 | ADR-001 is an individual draft, not a team decision | High | Requires team review and sign-off before it counts as accepted |
| R3 | Context map drawn from database tables or UI screens out of habit | Medium | Explicit review pass against business language, not schema |
| R4 | "Extract because it's fashionable" pressure once the team forms | Medium | The decision path (§4) is the standing rule; any extraction must show a measured trigger |
| R5 | Catalog extraction adds one cross-boundary call at checkout | Low | Acceptable per ADR-001; revisit only if it becomes a consistency problem in practice |
| R6 | **[TEAM]** not formed; carried over from Week 01 | **Blocking** | Same mitigation as Week 01 PDR — resolve in Week 02/03 |

---

## 9. Open questions for review

1. **[TEAM]** Does the real product even have a context with Catalog's profile — a real, independent, measured scaling need — or does everything stay in the monolith at MVP 1?
2. Should the context map be redrawn with the team before or after the problem statement is finalized?
3. Who owns `docs/adr/` — is ADR-001 committed by whoever writes it, or does it require a PR reviewed by the whole team before merge?
4. If no context shows a scaling trigger yet, is a pure modular monolith the correct ADR-001 for MVP 1 — should the decision explicitly say "no extraction, revisit at MVP 2"?

---

## 10. Definition of Done — this week's HUs

- [ ] Context map redrawn against the real domain (once the team exists)
- [ ] Decision path (§4) applied per real context, not just the illustrative one
- [ ] ADR-001 reviewed and accepted by the team, status updated from Proposed to Accepted
- [ ] Backlog stories from §7 adapted to the real product, with testable acceptance criteria
- [ ] No context extracted without a documented, measured scaling/deploy trigger

---

## 11. References

- Week 02 · Session 1 — *Distributed architectures: client-server, P2P, SOA, microservices*
- Week 02 · Session 2 — *Planning: choosing your architecture, bounded contexts and the ADR*
- Week 02 example diagram — [`week-02-example.svg`](./week-02-example.svg)
- Weekly status — [`README.md`](./README.md)
- [Week 01 PDR](../../01-week/hu-status/PDR.md) — system model and consistency this architecture must honor
- Course material (OVAs) — https://code-corhuila.github.io/ova-web/2026-B/distribuidos/

---

*Distributed Systems · Week 02 · Preliminary Design Review · Systems Engineering · Faculty of
Engineering · CORHUILA 2026-B*
