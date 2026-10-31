"""A minimal catalog-api to run the negative test without Docker (W13, CP8).

It starts the REAL HTTP adapter and the REAL use cases of catalog-api (branch develop) and swaps only the product repository
for the in-memory double that its own tests use (`tests/application/fakes.py`). Run it from the root of a copy of
amaranta-shop-catalog-api: `PYTHONPATH="src;." python serve_minimal_catalog.py` (on Linux or macOS use `:` instead of `;`).
It listens on 127.0.0.1:8082, the address the test reads from CATALOG_URL.
"""

import uvicorn

from catalog.adapter.inbound.http.app import create_app
from catalog.adapter.inbound.http.internal import internal_router
from catalog.application.usecase.release_stock import ReleaseStockService
from catalog.application.usecase.reserve_stock import ReserveStockService
from tests.application.fakes import DOG_FOOD, FakeClock, FakeProducts, product

products = FakeProducts(product(DOG_FOOD, "Dog food 3 kg", 45_000, stock=10))
router = internal_router(ReserveStockService(products, FakeClock()), ReleaseStockService(products, FakeClock()))

uvicorn.run(create_app(routers=[router]), host="127.0.0.1", port=8082, log_level="warning")
