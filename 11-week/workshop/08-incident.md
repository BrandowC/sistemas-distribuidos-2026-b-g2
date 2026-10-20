# 08 - Incident drill and blameless postmortem

A simulated incident on the journey of `01-journey.md`, played with the contracts of CP1 to CP8.
Nothing here happened in production.

**The incident.** The dependency of hop 3, MongoDB read by `catalog-api`, answers in 3 seconds for
25 % of the requests during 40 minutes, from 10:00 to 10:40 UTC on 2026-10-20. The read timeout of
`catalog-api` is 3 s, so a slow read ends as an error: `catalog-api` answers `503` and the gateway
forwards it. The list and the detail of a product read the same MongoDB, so both are hit. Traffic is
the one of `05-slo.md`: 600 list reads a day (0.42 a minute) and 300 detail reads a day.

## The trace of one slow request

`trace_id = 4b8e2f7a1c9d4630a5e7b2d8f1c06a39`, a list read at 10:31:42 UTC.

- `GET /api/v1/products` on `api-gateway` (S1, root): **3,016 ms**
  - `GET /api/v1/products` on `catalog-api` (S2, child of S1): **3,007 ms**
    - MongoDB `find` on the collection `product` (S3, child of S2): **3,004 ms**, ends in timeout

The 3 s are in S3, and S1 and S2 are the same wait seen from above. Without the trace, the gateway
only shows a slow `503`.

Four log lines of that trace, in the format of `02-log-contract.md`:

```json
{"timestamp":"2026-10-20T10:31:42.118Z","level":"INFO","service":"api-gateway","version":"1.0.0","environment":"qa","trace_id":"4b8e2f7a1c9d4630a5e7b2d8f1c06a39","span_id":"6c0d93e1a47b2f58","correlation_id":"e45a1c07b93d4f2a8c6e0d5b7a91f3c2","event":"gateway.request.received","message":"GET /api/v1/products","duration_ms":0}
{"timestamp":"2026-10-20T10:31:42.124Z","level":"INFO","service":"catalog-api","version":"2.0.0","environment":"qa","trace_id":"4b8e2f7a1c9d4630a5e7b2d8f1c06a39","span_id":"d17e4a9b0c2f3865","correlation_id":"e45a1c07b93d4f2a8c6e0d5b7a91f3c2","event":"product.read.started","message":"reading the product list","duration_ms":1,"attempt":1}
{"timestamp":"2026-10-20T10:31:45.130Z","level":"ERROR","service":"catalog-api","version":"2.0.0","environment":"qa","trace_id":"4b8e2f7a1c9d4630a5e7b2d8f1c06a39","span_id":"2f95b8c6e1a07d34","correlation_id":"e45a1c07b93d4f2a8c6e0d5b7a91f3c2","event":"mongo.read.timeout","message":"MongoDB did not answer the product list read","duration_ms":3004,"attempt":1}
{"timestamp":"2026-10-20T10:31:45.134Z","level":"ERROR","service":"api-gateway","version":"1.0.0","environment":"qa","trace_id":"4b8e2f7a1c9d4630a5e7b2d8f1c06a39","span_id":"6c0d93e1a47b2f58","correlation_id":"e45a1c07b93d4f2a8c6e0d5b7a91f3c2","event":"gateway.response.sent","message":"503 sent to the browser","duration_ms":3016,"rule_code":"SERVICE_UNAVAILABLE","http_status":503}
```

In this drill the list is not retried: a second wait of 3 s would be longer than the visitor can wait.

## Values the SLIs reach

Expected values with uniform traffic: 25 % of the reads of those 40 minutes fail.

| SLO of `05-slo.md` | Target | During the 40 min | 1 h window at 10:40 | 30-day window after |
|---|---|---|---|---|
| 1. List availability | 99.5 % | 75 % | 1 - 4.17 / 25 = **83.3 %** | 1 - 4.17 / 18,000 = **99.977 %** |
| 2. List latency (0.25 s) | 95 % | 75 % | 83.3 % | 99.977 % |
| 3. Detail latency (1.0 s) | 99 % | 75 % | 1 - 2.08 / 12.5 = 83.3 % | 1 - 2.08 / 9,000 = 99.977 % |

During the incident the three SLIs are far under their targets. Over the month they barely move,
because the incident is short against 18,000 reads.

## Which alert fires first, and when

`CatalogListFastBurn` fires at **minute 18** (10:18). The 5-minute ratio is 25 %, above 7.2 % from
the first minutes. The 1-hour ratio is the slow one: it passes 7.2 % when 0.104 failed reads a
minute fill 7.2 % of the 25 reads of the hour, at 0.072 x 60 / 0.25 = 17.3 minutes. The rule
evaluates every minute, so it fires at 10:18, with 25 valid reads (the minimum is 10). At that
moment about 1.8 failed reads are spent, the 2 % of the budget that `06-alert-policy.md` announces.
With so few reads, the second failed read arrives on average at minute 19.2, so in a real run the
alert fires between minutes 18 and 20.

`CatalogListSlowBurn` does **not** fire: its 6-hour ratio reaches 4.17 / 150 = 2.8 % at minute 40,
under 3 %. It would need minute 43. No alert exists for the latency SLOs; here the timeouts count as
errors, so the availability alert is enough, but a slow answer under 3 s would page nobody.

## The runbook step that stops the bleeding

**Mitigation 1 of `07-runbook.md`: `docker compose restart catalog-api`.** It builds a new pool of
connections to MongoDB and drops the one that hangs. Mitigations 2 and 3 do not apply: the failures
do not grow with traffic and no migration of `catalog-db` came before.

## Postmortem

Blameless: it describes what the system and our process allowed, not who made a mistake.

### Summary

For 40 minutes, 1 of every 4 reads of the catalog failed with `503`. The alert fired at minute 18, a
restart at minute 40 ended it. About 6 visitors saw the error.

### Timeline (UTC, 2026-10-20)

| Time | Minute | Event |
|---|---|---|
| 10:00 | 0 | One connection of the pool of `catalog-api` hangs after a network failover of MongoDB. 25 % of the reads wait 3 s and fail. |
| 10:18 | 18 | `CatalogListFastBurn` fires, severity `critical`. 2 % of the budget is spent. |
| 10:20 | 20 | The developer on duty acknowledges the page and opens the runbook. |
| 10:26 | 26 | Confirmation done: ratio 25 %, p95 of the list 3 s, the first `ERROR` of the trace is `mongo.read.timeout`. |
| 10:26 | 26-38 | The developer checks the MongoDB server because the runbook row says "MongoDB, or the connection". It is healthy: the same query in `mongosh` takes 38 ms. |
| 10:33 | 33 | 15 minutes without improvement: the runbook sends the incident to the Tech Lead. |
| 10:39 | 39 | The Tech Lead decides: restart first, investigate later. |
| 10:40 | 40 | `docker compose restart catalog-api`. Every read answers in about 40 ms again. |
| 10:45 | 45 | The 5-minute ratio is back to 0 and the alert resolves. The recovery checks of the runbook pass. |

Detection took 18 minutes and the mitigation 22 more.

### Impact

| | Reads in 40 min | Failed | Share of budget |
|---|---|---|---|
| List (SLO 1) | 0.417 x 40 = 16.7 | 4.17 | 4.17 / 90 = **4.6 %** of the availability budget, equal to 40 x 25 % = **10 of 216 minutes** |
| List (SLO 2) | 16.7 | 4.17 slow | 4.17 / 900 = 0.46 % of the latency budget |
| Detail (SLO 3) | 0.208 x 40 = 8.3 | 2.08 slow | 2.08 / 90 = 2.3 % of the detail budget |

The budget policy of SLO 1 starts at 50 %, so the policy asks nothing. We write the postmortem anyway.

### Root cause

One of the 4 connections of the pool of `catalog-api` (a size assumed for the drill; it is a driver
setting that `03-instrumentation` does not fix) kept waiting for a MongoDB node that was gone. A read
that took that connection waited for the whole timeout, 1 read in 4 = 25 %. The pool did not drop the
connection after its first timeout.

### Contributing factors

- The pool of connections cannot be seen: `catalog_mongo_connections_in_use` is only proposed in
  `04-metrics.md`, and no metric separates the MongoDB wait from the rest of the request.
- The runbook row for `mongo.read.timeout` names two places, and 12 minutes went into the one that
  was healthy. The restart is the cheapest mitigation and could have come first.
- The alert needs the 1-hour window to fill, so at 25 % it cannot fire before minute 17.
- The gateway exports no metrics yet, so only `catalog-api` could see the failure.

### Action items

1. **As the developer on duty, I want to see the connections of the pool and the MongoDB wait, so
   that I can tell in the first 5 minutes that the problem is inside `catalog-api`.**
   - Given the service runs, when I call `GET /metrics`, then `catalog_mongo_connections_in_use` is
     listed with no labels.
   - Given a test double of the collection whose `find` blocks 3 s, when 4 list reads run at once,
     then the gauge is 4 during the wait and 0 after it.
2. **As the developer on duty, I want the runbook to say "restart first" when the first `ERROR` is
   `mongo.read.timeout`, so that I apply mitigation 1 before I investigate.**
   - Given the table of `07-runbook.md`, when the first `ERROR` is `mongo.read.timeout`, then its
     row sends to mitigation 1 with the order "restart, then check the server".
   - Given the next drill of this fault, when the alert fires, then the restart happens in 10
     minutes or less, measured on the timeline.
3. **As a visitor, I want `catalog-api` to drop a connection after it times out, so that one broken
   connection does not slow 1 read in 4.**
   - Given a test double with one connection that never answers, when 100 list reads run, then at
     most 1 waits for the timeout and the other 99 answer in under 0.25 s.
   - Given that test, when it runs in the unit tests of `03-instrumentation`, then it passes
     without a real MongoDB.
