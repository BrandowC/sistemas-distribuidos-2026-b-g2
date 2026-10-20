# 05 - SLIs, SLOs and error budget

Journey: a visitor browses the catalog (`01-journey.md`), served by `catalog-api` on top of the
`product` collection of MongoDB (ADR-010 of the team `-docs`). The user story is `HU-CAT-001`. The
routes come from `07-api/contracts/openapi/catalog-service.yaml`: the public list `/products` and
the detail of one product. The metrics are the ones of `04-metrics.md`: `catalog_requests_total` and
`catalog_request_duration_seconds`.

These metrics exist today in the module of `03-instrumentation`. The real `catalog-api` has to
expose them before the SLOs can be measured in production.

## Traffic

The shop is a local veterinary clinic with a physical store, a website and a self-service kiosk.
We estimate 150 visitors a day who read about 4 pages of the list each: **600 list reads a day**,
which is 18,000 a month (30 days). About one visitor in two opens a product, so **300 detail reads
a day**, 9,000 a month.

On average that is 600 / 1,440 = 0.42 list reads a minute. The traffic is small, so one failure
matters more than in a busy service, and the budget is better read in minutes than in requests.

## The three SLOs

All use a rolling window of 30 days. Valid events are the requests that the service could answer:
`client_error` (4xx) is left out, because the visitor, not the service, caused it.

### SLO 1 - Availability of the product list

- **SLI:** list reads that did not fail / valid list reads.
- **PromQL:**
  `sum(rate(catalog_requests_total{route="/api/v1/products",outcome="ok"}[30d])) / sum(rate(catalog_requests_total{route="/api/v1/products",outcome=~"ok|server_error"}[30d]))`
- **Target:** 99.5 % over 30 days.

### SLO 2 - Latency of the product list

- **SLI:** list reads answered in 0.25 s or less / all list reads.
- **PromQL:**
  `sum(rate(catalog_request_duration_seconds_bucket{route="/api/v1/products",le="0.25"}[30d])) / sum(rate(catalog_request_duration_seconds_count{route="/api/v1/products"}[30d]))`
- **Target:** 95 % over 30 days. The 0.25 s is the target of CP4 for an indexed read of 12 products.

### SLO 3 - Latency of the detail of a product

- **SLI:** detail reads answered in 1.0 s or less / all detail reads.
- **PromQL:**
  `sum(rate(catalog_request_duration_seconds_bucket{route="/api/v1/products/{id}",le="1.0"}[30d])) / sum(rate(catalog_request_duration_seconds_count{route="/api/v1/products/{id}"}[30d]))`
- **Target:** 99 % over 30 days.
- **Why this one fits the shop:** opening a product is the moment the visitor decides to buy. It is
  a read by primary key, much cheaper than the list, so 99 % is realistic, and 1.0 s is where CP4
  says a visitor notices the wait.

## Error budget

| SLO | Valid events a month | Target | Budget in requests | Budget in minutes |
|---|---|---|---|---|
| 1. List availability | 18,000 | 99.5 % | 0.5 % of 18,000 = **90 failed reads** | 0.5 % of 43,200 = **216 min** of full outage |
| 2. List latency | 18,000 | 95 % | 5 % of 18,000 = **900 slow reads** | 5 % of 43,200 = **2,160 min** of every read being slow |
| 3. Detail latency | 9,000 | 99 % | 1 % of 9,000 = **90 slow reads** | 1 % of 43,200 = **432 min** of every read being slow |

The month has 30 x 24 x 60 = 43,200 minutes. Check of SLO 1: at 0.42 reads a minute, 216 minutes
of outage lose about 90 reads, the same figure as the budget in requests.

Reality check: a 30 minute failure of MongoDB loses about 12 list reads, 14 % of the budget of
SLO 1. Two such failures in a month use more than a quarter of it, so the target is demanding but
reachable for a team without on-call duty.

## Error budget policy

Budget of SLO 1 (90 failed list reads, 216 minutes). The percentage is the share already spent in
the rolling window.

| Spent | In requests / minutes | What the team does |
|---|---|---|
| 50 % | 45 reads / 108 min | The cause goes to the next planning as a user story. We read the logs of the failed traces by `trace_id` and name the most frequent cause. Work goes on as usual. |
| 75 % | 68 reads / 162 min | Risky changes to `catalog-api` and `catalog-db` stop: migrations, new indexes and new validators. Only fixes and reliability work are merged. The owner of the alert reviews the budget every day. |
| 100 % | 90 reads / 216 min | No new features on the catalog journey until the window recovers: the team only stabilizes. A blameless postmortem is written in two working days, and the Tech Lead tells the teacher in the next sprint review. |
