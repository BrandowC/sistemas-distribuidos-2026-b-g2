"""Negative authorization test for the first security story of my W13 backlog (STRIDE: Spoofing).

Boundary: sales-api to catalog-api. The internal stock routes of catalog-api, POST /internal/products/reserve-stock and
POST /internal/products/release-stock, must refuse a caller that does not show the shared secret.

Acceptance criterion covered: "a request to /internal/products/reserve-stock without the shared-secret header answers 401".
Today catalog-api has no such check (decision OD-3 of the checkout spec trusts the Docker network), so this test FAILS
against the current service: the failure is the evidence of the gap, and it turns green when the story is done.

It talks to a running catalog-api over HTTP (CATALOG_URL), with the standard library only.
"""

import json
import os
import urllib.error
import urllib.request

import pytest

BASE_URL = os.environ.get("CATALOG_URL", "http://localhost:8082").rstrip("/")

# A product id that does not exist: if a request gets through, it changes no stock.
UNKNOWN_PRODUCT = "00000000-0000-4000-8000-000000000000"
ITEMS = {"items": [{"productId": UNKNOWN_PRODUCT, "quantity": 1}]}


def post(path: str, body: dict) -> int:
    """POST a JSON body, with no credential at all, and give back the HTTP status."""
    request = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


@pytest.mark.parametrize("route", ["/internal/products/reserve-stock", "/internal/products/release-stock"])
def test_internal_stock_route_refuses_a_caller_without_the_shared_secret(route: str) -> None:
    assert post(route, ITEMS) == 401
