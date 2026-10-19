import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from catalog_api_obs import TraceMiddleware, log, parse_traceparent  # noqa: E402
from catalog_api_obs.metrics import Metrics  # noqa: E402
from catalog_api_obs.product_reader import list_products  # noqa: E402

CALLER = "00-7c1e5b0a93d24f68b2a4e19d3f0c8a57-a3f91c20d4b8e657-01"
REQUIRED = ["timestamp", "level", "service", "version", "environment", "trace_id", "span_id",
            "correlation_id", "event", "message", "duration_ms"]


class FakeCollection:
    def __init__(self):
        self.calls = []

    def find(self, flt, sort=None, skip=0, limit=0, comment=None):
        self.calls.append({"filter": flt, "comment": comment})
        return []


def call(app, path="/api/v1/products", traceparent=None):
    """Runs one request through the app and returns its response headers and the log lines it wrote."""
    environ = {"REQUEST_METHOD": "GET", "PATH_INFO": path}
    if traceparent:
        environ["HTTP_TRACEPARENT"] = traceparent
    seen = {}
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        body = b"".join(app(environ, lambda status, headers, exc=None: seen.update(dict(headers))))
    return seen, [json.loads(line) for line in out.getvalue().splitlines()], body


class InstrumentationTest(unittest.TestCase):
    def setUp(self):
        self.collection = FakeCollection()
        self.metrics = Metrics()

        def app(environ, start_response):
            if environ["PATH_INFO"] == "/api/v1/products":
                list_products(self.collection, 1, 12)
            start_response("200 OK", [("Content-Type", "application/json")])
            return [b"{}"]

        self.app = TraceMiddleware(app, self.metrics)

    def test_the_trace_id_received_is_the_trace_id_sent_downstream(self):
        headers, _, _ = call(self.app, traceparent=CALLER)
        downstream = parse_traceparent(self.collection.calls[0]["comment"].split("=", 1)[1])
        served = parse_traceparent(headers["traceparent"])
        self.assertEqual(downstream.trace_id, "7c1e5b0a93d24f68b2a4e19d3f0c8a57")
        self.assertEqual(served.trace_id, downstream.trace_id)
        self.assertNotEqual(downstream.span_id, served.span_id)

    def test_the_response_returns_a_new_span_of_the_callers_trace(self):
        headers, _, _ = call(self.app, traceparent=CALLER)
        served = parse_traceparent(headers["traceparent"])
        self.assertEqual(served.trace_id, "7c1e5b0a93d24f68b2a4e19d3f0c8a57")
        self.assertNotEqual(served.span_id, "a3f91c20d4b8e657")

    def test_a_missing_or_malformed_header_starts_a_new_trace(self):
        for header in (None, "garbage"):
            headers, _, _ = call(self.app, traceparent=header)
            self.assertIsNotNone(parse_traceparent(headers["traceparent"]))

    def test_every_log_line_follows_the_contract_and_carries_the_trace(self):
        _, lines, _ = call(self.app, traceparent=CALLER)
        self.assertEqual([line["event"] for line in lines], ["products.listed", "http.request.completed"])
        for line in lines:
            self.assertTrue(all(field in line for field in REQUIRED))
            self.assertEqual(line["trace_id"], "7c1e5b0a93d24f68b2a4e19d3f0c8a57")

    def test_personal_data_is_never_written_and_the_idempotency_key_is_cut(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            log("INFO", "products.listed", "x", contactPhone="3001234567", idempotency_key="k7Q2mX9aZZZZ")
        line = json.loads(out.getvalue())
        self.assertNotIn("contactPhone", line)
        self.assertEqual(line["idempotency_key"], "k7Q2mX9a")

    def test_metrics_expose_a_counter_by_outcome_and_a_latency_histogram(self):
        call(self.app, traceparent=CALLER)
        _, _, body = call(self.app, path="/metrics")
        text = body.decode()
        self.assertIn('catalog_requests_total{route="/api/v1/products",outcome="ok"} 1', text)
        self.assertIn('catalog_request_duration_seconds_bucket{route="/api/v1/products",le="+Inf"} 1', text)


if __name__ == "__main__":
    unittest.main()
