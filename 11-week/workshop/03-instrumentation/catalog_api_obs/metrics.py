"""A minimal Prometheus registry: one counter and one histogram, in the text exposition format."""
from collections import defaultdict

# Seconds. A visitor browsing the catalog expects an answer in well under a second.
BUCKETS = (0.05, 0.1, 0.25, 0.5, 1.0, 2.5)
_ROUTES = ("/internal/products/reserve-stock", "/internal/products/release-stock", "/api/v1/products", "/metrics")


def route_of(path: str) -> str:
    """A bounded label: the route template, never the raw URL (a product id in a label would be unbounded)."""
    if path.startswith("/api/v1/products/"):
        return "/api/v1/products/{id}"
    return path if path in _ROUTES else "other"


def outcome_of(status: int) -> str:
    return "ok" if status < 400 else "client_error" if status < 500 else "server_error"


class Metrics:
    def __init__(self):
        self.requests = defaultdict(int)
        self.buckets = defaultdict(lambda: [0] * len(BUCKETS))
        self.count = defaultdict(int)
        self.total = defaultdict(float)

    def observe(self, route: str, outcome: str, seconds: float) -> None:
        self.requests[(route, outcome)] += 1
        self.count[route] += 1
        self.total[route] += seconds
        for position, upper in enumerate(BUCKETS):
            if seconds <= upper:
                self.buckets[route][position] += 1

    def render(self) -> str:
        lines = ["# TYPE catalog_requests_total counter"]
        for (route, outcome), n in sorted(self.requests.items()):
            lines.append(f'catalog_requests_total{{route="{route}",outcome="{outcome}"}} {n}')
        lines.append("# TYPE catalog_request_duration_seconds histogram")
        for route in sorted(self.count):
            name = "catalog_request_duration_seconds"
            for upper, n in zip(BUCKETS, self.buckets[route]):
                lines.append(f'{name}_bucket{{route="{route}",le="{upper}"}} {n}')
            lines.append(f'{name}_bucket{{route="{route}",le="+Inf"}} {self.count[route]}')
            lines.append(f'{name}_sum{{route="{route}"}} {self.total[route]:.6f}')
            lines.append(f'{name}_count{{route="{route}"}} {self.count[route]}')
        return "\n".join(lines) + "\n"
