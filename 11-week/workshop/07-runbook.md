# 07 - Runbook: CatalogListFastBurn

Alert `CatalogListFastBurn` of `06-alerts.yml`, severity `critical`, team `catalog`. It protects
SLO 1 of `05-slo.md`: availability of the product list of `catalog-api`, 99.5 % over 30 days
(`HU-CAT-001`, the visitor who opens the shop). When it fires, 2 % of the monthly budget is already
spent, and at that rate the rest lasts 50 hours.

## Symptoms

- The alert fires: more than 7.2 % of the list reads failed over the last hour and over the last
  5 minutes, with at least 10 valid reads.
- The visitor sees the catalog area with its failure notice and the retry button, or an empty page.
  The gateway answers `503 SERVICE_UNAVAILABLE` with the error envelope and a `traceId`.
- In the logs of `catalog-api` there are `ERROR` lines, for example `mongo.read.timeout`
  (`02-log-contract.md`).

## 1. Confirm

Run the commands from the directory of the Compose project of the environment.

1. The ratio is really above the threshold: `catalog:list_error_ratio:rate5m` must be above
   `0.072`. Which route fails:
   `sum by (route) (rate(catalog_requests_total{outcome="server_error"}[5m]))`
2. Whether the answers are also slow:
   `histogram_quantile(0.95, sum by (le) (rate(catalog_request_duration_seconds_bucket{route="/api/v1/products"}[5m])))`
3. Take the `trace_id` of one failed request and follow it through the services:
   ```bash
   docker compose logs --no-log-prefix api-gateway catalog-api | grep '"level":"ERROR"' | tail -5
   docker compose logs --no-log-prefix api-gateway catalog-api | grep '<trace_id>'
   ```
4. Read the first `ERROR` of that trace:

| What the logs show | Where the problem is | Go to |
|---|---|---|
| `mongo.read.timeout` in `catalog-api` | MongoDB, or the connection of `catalog-api` to it | mitigation 1 |
| only `503` in the gateway, nothing in `catalog-api` | `catalog-api` is down | mitigation 1 |
| failures that grow with the traffic | overload | mitigation 2 |
| the failures began right after a migration of `catalog-db` | the last changeset | mitigation 3 |

## 2. Mitigations, from the least to the most risky

Only what our architecture really supports.

1. **Restart `catalog-api`.** Risk low: a few seconds without service and no data touched.
   `docker compose restart catalog-api`. It clears a stuck process or a broken pool of connections
   to MongoDB.
2. **Tighten the rate limit of the gateway** on the products route. Risk medium: some visitors get
   `429 TOO_MANY_REQUESTS`. The `api-gateway` already limits the requests of each client with
   `limit_req`; lower the limit for that route in the configuration of `amaranta-shop-api-gateway`
   and reload nginx. Use it only when the failures grow with the traffic.
3. **Roll back the last changeset of `catalog-db`.** Risk high: it changes the database. Every
   changeset of the `product` collection declares its inverse, so the Liquibase runner of
   `amaranta-shop-catalog-db` can undo the last one. Use it only when the failures began right
   after a migration (a new index or validator) and mitigations 1 and 2 did not help.

What we do not have today, and so is not in the list: a feature flag, scaling out (one instance of
`catalog-api` per environment), a circuit breaker, and a rollback of the image of `catalog-api`
(it has had a single release; from the second one, going back to the previous image becomes the
first rollback step).

## 3. Escalation

| When | Role | What it does |
|---|---|---|
| First 15 minutes | the developer who receives the alert | confirms and applies mitigation 1 |
| No improvement after 15 minutes | Tech Lead | owns the incident and decides mitigations 2 and 3 |
| 50 % of the budget spent, or 60 minutes without recovery | Product Owner | tells the shop that the catalog is unavailable and decides the message to visitors |
| 100 % of the budget spent | the teacher | is informed at the next sprint review, as the policy of `05-slo.md` says |

## 4. Verify the recovery

1. `catalog:list_error_ratio:rate5m` is back under `0.005`, the fraction of failures that the SLO
   allows, and stays there for 5 minutes. The alert resolves by itself.
2. The list answers through the gateway:
   `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/api/v1/products` prints `200`.
3. The 95th percentile of the list is back under 0.25 s (query of step 1.2).
4. No new `ERROR` line appears in the logs of `catalog-api` for 5 minutes.
5. Write down what the incident spent: failed reads and minutes of the budget of 90 reads and 216
   minutes. At 100 % a blameless postmortem is due in two working days.
