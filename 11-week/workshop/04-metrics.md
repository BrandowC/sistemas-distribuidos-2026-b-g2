# 04 - Golden signals and metric catalog

Journey: a visitor browses the catalog (`01-journey.md`). Two services take part: `api-gateway` and
`catalog-api`. The product data lives in the `product` collection of MongoDB (ADR-010 of the team
`-docs`: the Catalog domain uses MongoDB). The routes come from
`07-api/contracts/openapi/catalog-service.yaml`: the public `/products` and, for staff,
`/admin/products/{productId}/stock`.

## catalog-api

The first three rows are implemented in `03-instrumentation/catalog_api_obs/metrics.py`.

| Signal | Metric | Type | Labels | PromQL for the dashboard |
|---|---|---|---|---|
| Latency | `catalog_request_duration_seconds` | histogram | `route` | `histogram_quantile(0.95, sum by (le, route) (rate(catalog_request_duration_seconds_bucket[5m])))` |
| Traffic | `catalog_requests_total` | counter | `route`, `outcome` | `sum by (route) (rate(catalog_requests_total[5m]))` |
| Errors | `catalog_requests_total` | counter | `route`, `outcome` | `sum(rate(catalog_requests_total{outcome="server_error"}[5m])) / sum(rate(catalog_requests_total[5m]))` |
| Saturation | `catalog_mongo_connections_in_use` | gauge | none | `max_over_time(catalog_mongo_connections_in_use[5m])` |

`catalog_mongo_connections_in_use` is proposed and not in the code yet: the pool of connections to
MongoDB is the first resource `catalog-api` runs out of when the list is read many times at once.

## api-gateway

Target design: today the gateway writes access logs but exposes no metrics.

| Signal | Metric | Type | Labels | PromQL for the dashboard |
|---|---|---|---|---|
| Latency | `gateway_request_duration_seconds` | histogram | `route` | `histogram_quantile(0.95, sum by (le, route) (rate(gateway_request_duration_seconds_bucket[5m])))` |
| Traffic | `gateway_requests_total` | counter | `route`, `outcome` | `sum by (route) (rate(gateway_requests_total[5m]))` |
| Errors | `gateway_requests_total` | counter | `route`, `outcome` | `sum(rate(gateway_requests_total{route="/api/v1/products",outcome="server_error"}[5m]))` |
| Saturation | `gateway_active_connections` | gauge | none | `max_over_time(gateway_active_connections[5m])` |

The gateway answers `503 SERVICE_UNAVAILABLE` when `catalog-api` is down, so its error ratio on
`/api/v1/products` is the signal that a visitor sees first.

## Cardinality

| Label | Values | Count | Note |
|---|---|---|---|
| `route` | route template, never the URL: `/api/v1/products`, `/api/v1/products/{id}`, `/internal/products/reserve-stock`, `/internal/products/release-stock`, `/metrics`, `other` | 6 | the function `route_of` collapses everything else into `other` |
| `outcome` | `ok`, `client_error`, `server_error` | 3 | built from the status code by `outcome_of` |
| `le` | the buckets below and `+Inf` | 7 | |

Series per instance of `catalog-api`: the counter has 6 x 3 = 18, the histogram has 6 x (7 buckets
plus `_sum` and `_count`) = 54. About 72 in total, and it does not grow with traffic or with the
number of products.

Labels we forbid because they are unbounded:

| Forbidden label | Why | What replaces it |
|---|---|---|
| `product_id` | one value per product, and the catalog keeps growing | `category` (`FOOD`, `ACCESSORIES`, `HYGIENE`, `MEDICATION`, `TOYS`: 5 values) |
| raw URL or query string | `?page=2&limit=12` and the `q` search text create endless values | the route template |
| `user_id`, email or IP | one value per person, and personal data (see `02-log-contract.md`) | none: it goes in the logs, filtered by `trace_id` |
| `sku` | one value per product | `category` |

## Histogram buckets

`0.05, 0.1, 0.25, 0.5, 1.0, 2.5` seconds, chosen for what our visitor expects.

- A visitor who opens the shop expects the list at once: under `0.1` s it feels instant, and
  `0.25` s is our target for the 95th percentile, because the read is an indexed query of 12 products
  on `category` and `isActive`.
- `1.0` s is where the visitor notices the wait, so it is the line between a good and a slow answer.
- `2.5` s is the last bucket before the 3 s timeout that `sales-api` and the gateway apply when they
  wait for `catalog-api`: anything above it ends as an error, not as a slow answer.
