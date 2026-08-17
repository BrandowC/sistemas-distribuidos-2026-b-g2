# Preliminary Design Review (PDR) — Week 01

> **How to use this document.** The structure below is the deliverable; the content is a **worked
> example** built on the "Place Order" scenario from Session 1, so every section shows what a
> defensible answer looks like. Once the team picks its real problem, replace the domain content
> and keep the structure. Sections marked **[TEAM]** cannot be answered individually and are
> pending team formation.

| | |
| --- | --- |
| **Course** | Distributed Systems (cod. 82739) — 2026-B, Group 2 |
| **Week / Unit** | Week 01 · Unit 1 — Foundations · Corte 1 |
| **Author** | Brandow Stivent Claros Polania (`BrandowC`) |
| **Team** | **[TEAM]** — pending |
| **Status** | Preliminary — for review |
| **Scope** | MVP 1 design intent |

---

## 1. Problem statement and scope

**[TEAM]** — the real problem is chosen collectively (HU-001-005). The example below is the
reference domain used throughout this document.

**Example domain.** An online store must let a customer place an order that atomically-in-intent
reserves inventory and charges a payment method, across three independently deployable services.
The system must remain correct when the network between those services partitions.

| | |
| --- | --- |
| **In scope (MVP 1)** | Place order; reserve stock; charge payment; confirm/cancel order; order status query |
| **Out of scope (MVP 1)** | Shipping, returns, refunds, promotions, multi-currency, recommendations |
| **Primary actor** | Customer placing an order |
| **Success condition** | No double charge, no oversell, and an honest order state visible to the customer at all times — including during a partition |

### Why this problem is genuinely distributed

It is not a monolith with extra servers. It crosses process boundaries, so it loses the three
guarantees a monolith provides for free — shared state, a single clock, and all-or-nothing
failure — and it must therefore be designed against the eight fallacies of distributed computing
rather than around them.

---

## 2. System model and assumptions

Fixing these assumptions is what makes the rest of the design reviewable.

| Dimension | Choice | Justification |
| --- | --- | --- |
| **Timing model** | Asynchronous (no bound on message or processing delay) | The realistic model for services communicating over a network; assuming bounded delay would make the design unsound in production |
| **Failure model** | Crash-recovery + omission | Nodes die and return; messages are lost. This is the standard operating reality for business systems |
| **Byzantine tolerance** | **Not** in scope | Arbitrary/malicious node behaviour is expensive to tolerate and is not justified by our threat model. All services are operated by us inside a trusted boundary |
| **Communication** | Synchronous (HTTP/gRPC) for the command path; asynchronous events for propagation | Request/response where the caller genuinely needs an answer; events where decoupling absorbs load |
| **Time source** | Logical (Lamport / causal), never wall-clock | Clock skew and NTP jumps make wall-clock timestamps unsafe for ordering events across nodes |

### Explicit non-assumptions (the fallacies, inverted)

The network is **not** reliable; latency is **not** zero; bandwidth is **not** infinite; the
network is **not** secure; topology **does** change; there is **not** one administrator; transport
cost is **not** zero; the network is **not** homogeneous. Each of these is an assumption the design
must survive being wrong about.

---

## 3. Bounded contexts and service decomposition

Strategic DDD: each bounded context owns its own model, its own ubiquitous language and its own
data. A bounded context is the natural service boundary.

| Bounded context | Responsibility | Owns (data) | Ubiquitous language |
| --- | --- | --- | --- |
| **Orders** | Order lifecycle; orchestrates the Saga | Orders, order lines, saga state | Order, Line, Confirm, Cancel |
| **Inventory** | Stock levels and reservations | Stock per SKU, reservations | SKU, Reserve, Release, On-hand |
| **Payments** | Charging and refunding | Charges, idempotency keys | Charge, Authorize, Refund |

**Context map.** `Orders` is the orchestrator; it is a *customer* of both `Inventory` and
`Payments`, which are *suppliers* exposing a published contract. No context reaches into another
context's database — ever. A service is never embedded inside another.

### Aggregates (tactical DDD)

| Aggregate root | Invariant it protects |
| --- | --- |
| `Order` | An order cannot be confirmed with zero lines; status transitions are legal only in one direction |
| `StockItem` | Reserved quantity never exceeds on-hand quantity (this is what prevents overselling) |
| `Charge` | The same idempotency key never produces two charges |

The aggregate is the **only** place these invariants change. Repositories load and save whole
aggregates; nothing reaches inside to mutate them. Domain events are immutable and past tense:
`OrderConfirmed`, `StockReserved`, `PaymentCharged`.

---

## 4. Consistency and delivery semantics per operation

**This is the core of the review.** Consistency is chosen per operation, never per system — and
choosing it late forces redesign, because a decision like "strong consistency on inventory
decrement" changes the architecture, not just the code.

| Operation | Consistency | Delivery | Justification |
| --- | --- | --- | --- |
| **Reserve stock** | Strong / linearizable | At-least-once + idempotency | Overselling is a real-money error. Under a partition this operation chooses **C over A** (reject rather than oversell) |
| **Charge payment** | Strong / linearizable | At-least-once + **idempotency key** | Double-charging a customer is the worst failure this system can produce |
| **Confirm order** | Strong within the `Order` aggregate | At-least-once | The aggregate is the consistency boundary; no cross-service transaction |
| **Order status read** | Read-your-writes (causal) | — | The customer must always see their own order, immediately after acting on it |
| **Product catalog read** | Causal | — | Slightly stale catalog data is acceptable; coordination cost is not justified |
| **"Units sold" counter** | Eventual | At-least-once | A counter that converges is fine. This operation chooses **A over C** |

### PACELC position

**If** a partition occurs → the order path chooses **C** (fail honestly rather than oversell or
double-charge). **Else**, in normal operation → we accept slightly higher **L**atency on the money
path to preserve **C**onsistency, and trade the opposite way on catalog and counters.

### Exactly-once is a myth

Exactly-once *delivery* over a network does not exist. What this design builds is exactly-once
**processing** = at-least-once delivery **+** an idempotency key **+** deduplication. Every
consumer is designed to survive redelivery:

```java
// at-least-once delivery ⇒ the same event may arrive twice
if (processed.putIfAbsent(event.id(), TRUE) == null) {
    applyEffect(event);          // runs once per unique event id
}                                // duplicates are ignored, not double-applied
```

---

## 5. Architecture

### 5.1 Hexagonal (ports and adapters)

The core — domain plus application/use-cases — does not know how it is driven (HTTP, CLI, queue)
or what it drives (DB, cache, external API). All I/O crosses a **port** implemented by an
**adapter**.

```
DRIVING adapters  ──►   CORE (no I/O, no framework)   ──►  DRIVEN adapters
REST controller         application / use-cases            PostgresOrderRepository
Kafka consumer          domain (aggregates, VOs)           PaymentsHttpClient
CLI                                                        OutboxPublisher
```

**Dependency rule:** adapters → application → domain. Never inward-out.

**Smell test (fails review):** a file under `domain/` importing an ORM or driver
(`pgxpool`, `EntityManager`, `PrismaClient`), or a controller running SQL.

```java
interface OrderRepository { Optional<Order> byId(OrderId id); void save(Order o); }  // OUT port

final class ConfirmOrder {                              // use-case
  private final OrderRepository repo;                   // depends on the PORT, not on JPA
  ConfirmOrder(OrderRepository repo){ this.repo = repo; }
  void handle(OrderId id){
    var o = repo.byId(id).orElseThrow();
    o.confirm();                                        // invariants enforced INSIDE the aggregate
    repo.save(o);
  }
}
```

### 5.2 The Saga (no distributed transaction)

The checkout spans three services, so it **cannot** be one ACID transaction. It is a Saga with
compensations:

```
reserve stock  ──►  charge card  ──►  confirm order
      ▲                  │ fail
      └──────────────────┘  compensate: release stock
```

The charge step carries an **idempotency key**, so a retry after the partition heals does not
double-charge.

### 5.3 Resilience patterns

| Pattern | Problem it solves here |
| --- | --- |
| **Circuit Breaker + Timeout** | Stop hammering a partitioned Payments; fail fast instead of exhausting the thread pool |
| **Retry + backoff + jitter** | Survive a transient partition without causing a retry storm |
| **Bulkhead** | Isolate pools so one slow dependency cannot sink the whole service |
| **Saga** | Consistency across services without a distributed transaction |
| **Outbox** | Commit DB state and publish the event atomically — no lost events |
| **CQRS** | Separate the write model (commands) from the read model (queries) |

---

## 6. The failure path (designed first, not last)

A customer taps Buy. Orders reserves stock successfully, then the network between Orders and
Payments partitions mid-request.

**The naive path — and why it is a classic production outage.** One big synchronous transaction
across three services holding a DB lock while waiting for Payments: threads freeze, the connection
pool is exhausted, and the failure cascades until the whole shop is down. This design explicitly
rejects it.

**The designed path:**

1. **Do not block** holding a DB lock waiting for Payments.
2. The circuit breaker opens after repeated timeouts; the call fails fast.
3. The Saga runs its compensation: **release the reserved stock**.
4. The charge retry carries the idempotency key, so healing the partition cannot double-charge.
5. **Tell the customer the truth:** `"Order received — confirming payment…"` — a pending state.
   An infinite spinner or a fake `"Success!"` is a lie the system cannot yet guarantee.

> Distributed correctness is about designing the failure paths first. The happy path is the easy
> part.

---

## 7. Testing strategy

Test at the cheapest level that gives confidence.

| Level | What it covers | Tooling |
| --- | --- | --- |
| **Unit** | Aggregate invariants and use-case logic, with no I/O | JUnit / Go testing |
| **Integration** | Adapters against a real database | Testcontainers |
| **Contract** | Producer/consumer compatibility between services | Pact (`*_contract`) |
| **E2E** | The Saga end to end, including the compensation path | Explicit e2e suite |

```java
@Test void confirm_rejects_empty_order() {
  var order = new Order(new OrderId("1"), List.of());   // Arrange
  assertThrows(DomainException.class, order::confirm);   // Act + Assert (the contract)
}
```

**Non-negotiable:** the failure path is tested, not just the happy path — a compensation that has
never run is a compensation that does not work. Declared coverage may never exceed measured
coverage; over-claiming is a review failure, and `tests/` mirrors the source layout.

---

## 8. Risks

| # | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| R1 | Double charge on retry after a partition heals | **Critical** — real money | Idempotency key on every charge; deduplication at the consumer |
| R2 | Overselling under concurrent reservations | High | Strong consistency on the reserve operation; invariant enforced inside the `StockItem` aggregate |
| R3 | Compensation never tested, silently broken | High | Failure-path tests are mandatory, not optional |
| R4 | Cascading failure from a slow dependency | High | Circuit breaker, timeout and bulkhead on every outbound call |
| R5 | Lost events (DB committed, event never published) | Medium | Outbox pattern |
| R6 | Hexagonal boundaries erode over time | Medium | Make it a build-failing check, not a code-review comment — a standard that does not fail the build is only a comment |
| R7 | **[TEAM]** not formed; problem not yet chosen | **Blocking** | Resolve in Week 02 (HU-001-005) |
| R8 | Profile repo CONFIG mismatch → work reads as "nothing delivered" | **Blocking** | Verify `BrandowC/BrandowC` CONFIG matches character for character |

---

## 9. Open questions for review

1. **[TEAM]** What real problem will the system solve, and does it genuinely require distribution?
2. Is `Payments` an internal bounded context, or an anti-corruption layer over an external gateway?
3. Should order status be served from a CQRS read model in MVP 1, or is that premature?
4. Where does the idempotency key originate — client-generated or server-generated per attempt?
5. Java or Go for the backend, and does the team commit to one for the whole product?

---

## 10. Definition of Done for MVP 1

- [ ] Implemented **and tested** (unit + integration + contract; e2e for the Saga)
- [ ] Acceptance criteria met and testable
- [ ] Consistency and delivery semantics documented per operation
- [ ] Failure path exercised — the compensation actually runs in a test
- [ ] Security addressed for critical risks; no secrets in code (config via environment variables)
- [ ] Hexagonal boundaries respected — domain has no I/O
- [ ] Documentation updated
- [ ] **Validated at runtime**: it actually runs, the DB is up, the service starts, no blank screen

---

## 11. References

- Week 01 · Session 1 — *Distributed systems: models, time, consistency and trade-offs*
- Week 01 · Session 2 — *Professional engineering foundations for distributed systems*
- Week 01 example diagram — [`week-01-example.png`](./week-01-example.png)
- Weekly status — [`README.md`](./README.md)
- Course material (OVAs) — https://code-corhuila.github.io/ova-web/2026-B/distribuidos/

---

*Distributed Systems · Week 01 · Preliminary Design Review · Systems Engineering · Faculty of
Engineering · CORHUILA 2026-B*
