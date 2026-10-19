# How to run the instrumentation of catalog-api

A minimal module for `catalog-api`, the Python service that owns the products and their stock. It
reads or creates the W3C trace context, writes the JSON logs of `02-log-contract.md`, exposes two
metrics and passes the context to the one outgoing call of the journey: the product list read from
MongoDB (the database span of `01-journey.md`).

## Install

Nothing to install. It uses only the Python standard library (Python 3.10 or newer).

## Run the tests

From the root of the repository:

```bash
cd 11-week/workshop/03-instrumentation
python -m unittest discover -s tests -v
```

Output on my machine (Python 3.13, Windows):

```text
test_a_missing_or_malformed_header_starts_a_new_trace ... ok
test_every_log_line_follows_the_contract_and_carries_the_trace ... ok
test_metrics_expose_a_counter_by_outcome_and_a_latency_histogram ... ok
test_personal_data_is_never_written_and_the_idempotency_key_is_cut ... ok
test_the_response_returns_a_new_span_of_the_callers_trace ... ok
test_the_trace_id_received_is_the_trace_id_sent_downstream ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.003s

OK
```

The test that matters most is `test_the_trace_id_received_is_the_trace_id_sent_downstream`: a request
arrives with `traceparent` carrying the trace `7c1e5b0a...`, and the command sent to MongoDB carries
the same `trace_id` in its `comment`, with a new span id.

## Where each piece is

| File | What it does |
|---|---|
| `catalog_api_obs/trace_context.py` | parses, creates and derives `traceparent` |
| `catalog_api_obs/structured_log.py` | writes one JSON line with the fields of the log contract |
| `catalog_api_obs/middleware.py` | WSGI middleware: reads or creates the trace and returns it in the response |
| `catalog_api_obs/metrics.py` | request counter by route and outcome, latency histogram, `/metrics` text |
| `catalog_api_obs/product_reader.py` | reads the product list from MongoDB, carrying the trace context in the command |
