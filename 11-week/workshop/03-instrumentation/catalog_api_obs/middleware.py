"""WSGI middleware: read or create the trace context, give it to the logger, return it in the response."""
import time

from .structured_log import RequestState, current, log
from .trace_context import child_of, new_trace, parse_traceparent


class TraceMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        incoming = parse_traceparent(environ.get("HTTP_TRACEPARENT"))
        # With a caller, this service is a new span of the caller's trace; without one, it starts the trace.
        trace = child_of(incoming) if incoming else new_trace()
        state = RequestState(trace, environ.get("HTTP_X_CORRELATION_ID") or trace.trace_id)
        token = current.set(state)
        started = time.perf_counter()
        status = {"code": 500}

        def respond(status_line, headers, exc_info=None):
            status["code"] = int(status_line.split()[0])
            extra = [("traceparent", trace.header()), ("X-Correlation-Id", state.correlation_id)]
            return start_response(status_line, list(headers) + extra, exc_info)

        try:
            return self.app(environ, respond)
        finally:
            log("INFO", "http.request.completed", f"{environ['REQUEST_METHOD']} {environ['PATH_INFO']}",
                (time.perf_counter() - started) * 1000, http_status=status["code"])
            current.reset(token)
