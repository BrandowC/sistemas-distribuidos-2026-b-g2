"""W3C trace context: the traceparent header that carries one trace_id through every service."""
import re
import secrets
from dataclasses import dataclass

_TRACEPARENT = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


@dataclass(frozen=True)
class TraceContext:
    trace_id: str
    span_id: str
    flags: str = "01"

    def header(self) -> str:
        return f"00-{self.trace_id}-{self.span_id}-{self.flags}"


def new_trace() -> TraceContext:
    """The root of a trace: what the gateway does when a request arrives without one."""
    return TraceContext(secrets.token_hex(16), secrets.token_hex(8))


def parse_traceparent(value: str | None) -> TraceContext | None:
    """The context a caller sent, or None when the header is missing, malformed or all zeros."""
    match = _TRACEPARENT.match((value or "").strip().lower())
    if not match or set(match.group(1)) == {"0"} or set(match.group(2)) == {"0"}:
        return None
    return TraceContext(*match.groups())


def child_of(parent: TraceContext) -> TraceContext:
    """A new span of the same trace: what a service sends downstream."""
    return TraceContext(parent.trace_id, secrets.token_hex(8), parent.flags)
