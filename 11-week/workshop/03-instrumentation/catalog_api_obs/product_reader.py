"""The outgoing call of catalog-api in the journey: reading the product list from MongoDB (span S4)."""
import time

from .structured_log import current, log
from .trace_context import child_of


def list_products(collection, page: int, limit: int) -> list:
    """The active products of one page, sorted by name.

    MongoDB has no headers, so the trace context travels in the `comment` of the command, where it shows
    in the server log and the profiler next to the operation it belongs to.
    """
    downstream = child_of(current.get().trace)
    started = time.perf_counter()
    products = list(collection.find(
        {"isActive": True},
        sort=[("name", 1)],
        skip=(page - 1) * limit,
        limit=limit,
        comment=f"traceparent={downstream.header()}",
    ))
    log("INFO", "products.listed", f"{len(products)} products read", (time.perf_counter() - started) * 1000)
    return products
