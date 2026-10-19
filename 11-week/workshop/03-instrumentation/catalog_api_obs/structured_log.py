"""One JSON object per line, with the fields of 02-log-contract.md."""
import json
import os
import sys
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timezone

from .trace_context import TraceContext

SERVICE = "catalog-api"
VERSION = os.environ.get("APP_VERSION", "2.0.0")
ENVIRONMENT = os.environ.get("APP_ENV", "dev")
# Never written, whatever the caller passes (the "Never log" table of 02-log-contract.md).
NEVER_LOG = {"contactName", "contactPhone", "deliveryAddress", "authorization", "password"}


@dataclass(frozen=True)
class RequestState:
    trace: TraceContext
    correlation_id: str


# The request being served: set by the middleware, read by every log line written while it lasts.
current: ContextVar[RequestState | None] = ContextVar("request_state", default=None)


def log(level: str, event: str, message: str, duration_ms: float = 0, **fields) -> dict:
    state = current.get()
    line = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "level": level,
        "service": SERVICE,
        "version": VERSION,
        "environment": ENVIRONMENT,
        "trace_id": state.trace.trace_id if state else "0" * 32,
        "span_id": state.trace.span_id if state else "0" * 16,
        "correlation_id": state.correlation_id if state else "none",
        "event": event,
        "message": message,
        "duration_ms": round(duration_ms),
    }
    for name, value in fields.items():
        if name not in NEVER_LOG:
            line[name] = value[:8] if name == "idempotency_key" else value
    sys.stdout.write(json.dumps(line, separators=(",", ":")) + "\n")
    return line
