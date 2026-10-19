# 02 - Structured log contract

Every service of the guest checkout (`api-gateway`, `sales-api`, `catalog-api`,
`notification-service`) writes one JSON object per line to standard output, with the same fields.
That makes "everything that happened to trace X" a single filter.

## Fields

| Field | Type | Required | Example | Why it exists |
|---|---|---|---|---|
| `timestamp` | string, ISO-8601 UTC | yes | `2026-10-19T14:58:03.412Z` | orders the lines of different services |
| `level` | string | yes | `WARN` | lets us filter by severity |
| `service` | string | yes | `sales-api` | tells which service wrote the line |
| `version` | string | yes | `2.0.0` | links a failure to the release that caused it |
| `environment` | string | yes | `qa` | separates `dev`, `qa` and `main` data |
| `trace_id` | string, 32 hex | yes | `7c1e5b0a93d24f68b2a4e19d3f0c8a57` | joins the lines of one request across services |
| `span_id` | string, 16 hex | yes | `a3f91c20d4b8e657` | places the line in the span tree of CP1 |
| `correlation_id` | string | yes | `b81d0e47c2a94f3c8d5e6a7f10293b4c` | the `X-Correlation-Id` the gateway already creates |
| `event` | string | yes | `order.rejected` | stable name to search and count, unlike free text |
| `message` | string | yes | `quantity outside 1-50` | explanation for the person reading |
| `duration_ms` | number | yes | `18` | latency of the operation, feeds the metrics of CP4 |

Domain fields of our checkout:

| Field | Type | Required | Example | Why it exists |
|---|---|---|---|---|
| `order_id` | string, UUID | optional | `df0ee10a-bf79-4038-a6c2-b73bb4577f4f` | follows one order from `orders` and `order_items`; absent until it is created |
| `idempotency_key` | string, first 8 characters | optional | `k7Q2mX9a` | shows that a retry of `POST /api/v1/orders` is the same intention |
| `line_count` | number | optional | `2` | size of the order, to spot failures that only happen with many lines |
| `rule_code` | string | optional | `RN-04` | the business rule of `specs/checkout.md` that decided the outcome |
| `http_status` | number | optional | `422` | what the caller received |

## Never log

| Data | Where it appears in our domain | Treatment |
|---|---|---|
| Contact name and phone | `contactName`, `contactPhone` of the order | never written; the `order_id` is enough to find them |
| Delivery address | `deliveryAddress` of the order | never written |
| Token | the `Authorization` header (JWT) of a customer | never written; only the role, as `user_role`, if needed |
| Password | the sign-in of the Security service | never written, not even masked |
| Full idempotency key | `Idempotency-Key` header | only the first 8 characters |
| Payment detail | `paymentMethod` is only a category (cash, card, transfer); no card number is collected | the category may be logged; anything beyond it never |

## Levels

| Level | We use it when | Example in our checkout |
|---|---|---|
| `ERROR` | an operation failed and a person or a retry has to act | `sales-api` cannot give a reservation back: `release-stock` times out |
| `WARN` | the system did the right thing, but something is wrong | a business rule rejects an order with `422` |
| `INFO` | a normal step of the journey | `catalog-api` reserved the stock |
| `DEBUG` | detail for finding a bug, off in `main` | the lines of the body sent to `reserve-stock` |

## Seven lines of one request

One checkout where the stock was reserved, the order was rejected by a business rule and the
compensation timed out. All lines share the same `trace_id`.

```json
{"timestamp":"2026-10-19T14:58:03.101Z","level":"INFO","service":"api-gateway","version":"1.0.0","environment":"qa","trace_id":"7c1e5b0a93d24f68b2a4e19d3f0c8a57","span_id":"0f8a2c61b9d4e3a7","correlation_id":"b81d0e47c2a94f3c8d5e6a7f10293b4c","event":"gateway.request.received","message":"POST /api/v1/orders","duration_ms":0}
{"timestamp":"2026-10-19T14:58:03.118Z","level":"INFO","service":"sales-api","version":"2.0.0","environment":"qa","trace_id":"7c1e5b0a93d24f68b2a4e19d3f0c8a57","span_id":"a3f91c20d4b8e657","correlation_id":"b81d0e47c2a94f3c8d5e6a7f10293b4c","event":"checkout.started","message":"visitor checkout, two lines","duration_ms":3,"idempotency_key":"k7Q2mX9a","line_count":2}
{"timestamp":"2026-10-19T14:58:03.141Z","level":"INFO","service":"catalog-api","version":"2.0.0","environment":"qa","trace_id":"7c1e5b0a93d24f68b2a4e19d3f0c8a57","span_id":"5d7e1b94a2c03f68","correlation_id":"b81d0e47c2a94f3c8d5e6a7f10293b4c","event":"stock.reserved","message":"two products reserved","duration_ms":18,"line_count":2}
{"timestamp":"2026-10-19T14:58:03.163Z","level":"WARN","service":"sales-api","version":"2.0.0","environment":"qa","trace_id":"7c1e5b0a93d24f68b2a4e19d3f0c8a57","span_id":"e2b46d0a7f19c853","correlation_id":"b81d0e47c2a94f3c8d5e6a7f10293b4c","event":"order.rejected","message":"quantity outside 1-50 reached the order_items check","duration_ms":9,"idempotency_key":"k7Q2mX9a","rule_code":"RN-04","http_status":422}
{"timestamp":"2026-10-19T14:58:03.170Z","level":"INFO","service":"sales-api","version":"2.0.0","environment":"qa","trace_id":"7c1e5b0a93d24f68b2a4e19d3f0c8a57","span_id":"c4a09e7d2b61f358","correlation_id":"b81d0e47c2a94f3c8d5e6a7f10293b4c","event":"stock.release.requested","message":"giving the reservation back","duration_ms":1,"rule_code":"RN-09","line_count":2}
{"timestamp":"2026-10-19T14:58:06.175Z","level":"ERROR","service":"sales-api","version":"2.0.0","environment":"qa","trace_id":"7c1e5b0a93d24f68b2a4e19d3f0c8a57","span_id":"c4a09e7d2b61f358","correlation_id":"b81d0e47c2a94f3c8d5e6a7f10293b4c","event":"catalog.release.timeout","message":"catalog-api did not answer release-stock","duration_ms":3004,"rule_code":"RN-09"}
{"timestamp":"2026-10-19T14:58:06.181Z","level":"WARN","service":"api-gateway","version":"1.0.0","environment":"qa","trace_id":"7c1e5b0a93d24f68b2a4e19d3f0c8a57","span_id":"0f8a2c61b9d4e3a7","correlation_id":"b81d0e47c2a94f3c8d5e6a7f10293b4c","event":"gateway.response.sent","message":"422 sent to the browser","duration_ms":3080,"http_status":422}
```
