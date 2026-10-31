# How to run the negative authorization test

## What it covers

- **Story:** `[security] Authenticate the callers of the internal Catalog stock endpoints` (STRIDE S).
- **Criterion:** a request to `POST /internal/products/reserve-stock` or `POST /internal/products/release-stock` of
  `catalog-api` without the shared-secret header answers `401`.
- **Test:** `tests/test_internal_stock_requires_secret.py`, one negative test run for the two routes. It sends no credential
  and uses a product id that does not exist, so a request that gets through changes no stock.

Today `catalog-api` does not check any secret on these routes (decision OD-3 of the checkout spec: the Docker network is
the only protection), so the test **fails** against the current service. That failure is the evidence of the gap. It turns
green when the story is done.

## Run it on my machine

1. Start the real chain, with the repositories side by side (this is the script of `amaranta-shop-catalog-portal`):

   ```bash
   bash scripts/e2e-real-stack.sh up
   ```

2. Run the test inside the same Docker network, because `catalog-api` is not published to the host:

   ```bash
   MSYS_NO_PATHCONV=1 docker run --rm --network amaranta-real-stack -e CATALOG_URL=http://catalog-api:8082 \
     -v "$PWD/13-week/workshop/04-security-ci/tests:/tests:ro" python:3.12-slim \
     sh -c "pip install -q pytest && pytest /tests -q"
   ```

3. Remove everything the script created:

   ```bash
   bash scripts/e2e-real-stack.sh down
   ```

## Run it without Docker (the way I ran it for CP8)

The Docker engine of my machine was not available, so I ran the test against a minimal module of the real service:
`serve_minimal_catalog.py` starts the real HTTP adapter and use cases of `catalog-api` (branch `develop`, commit `87a98f3`)
with the product repository in memory.

1. In a copy of `amaranta-shop-catalog-api` at `develop`, start the service: `python serve_minimal_catalog.py` with
   `PYTHONPATH="src;."`.
2. From the root of my fork, in another terminal: `CATALOG_URL=http://127.0.0.1:8082 python -m pytest 13-week/workshop/04-security-ci/tests -q`.

## Output of the run

Run on 2026-10-30 against `catalog-api` `develop` (87a98f3), with no credential in the requests:

```text
FF                                                                       [100%]
================================== FAILURES ===================================
_ test_internal_stock_route_refuses_a_caller_without_the_shared_secret[/internal/products/reserve-stock] _
>       assert post(route, ITEMS) == 401
E       AssertionError: assert 422 == 401
E        +  where 422 = post('/internal/products/reserve-stock', {'items': [{'productId': '00000000-0000-4000-8000-000000000000', 'quantity': 1}]})
_ test_internal_stock_route_refuses_a_caller_without_the_shared_secret[/internal/products/release-stock] _
>       assert post(route, ITEMS) == 401
E       AssertionError: assert 204 == 401
E        +  where 204 = post('/internal/products/release-stock', {'items': [{'productId': '00000000-0000-4000-8000-000000000000', 'quantity': 1}]})
=========================== short test summary info ===========================
FAILED ...test_internal_stock_requires_secret.py::test_internal_stock_route_refuses_a_caller_without_the_shared_secret[/internal/products/reserve-stock]
FAILED ...test_internal_stock_requires_secret.py::test_internal_stock_route_refuses_a_caller_without_the_shared_secret[/internal/products/release-stock]
2 failed in 0.33s
```

How I read it: both tests fail, and that is the expected result today. Neither route answered `401`. `reserve-stock` processed the
request and answered `422` for the unknown product, and `release-stock` accepted it with `204`. A caller with no secret reached
the use cases of both routes, which is the gap of story #37. The unknown product id means no stock changed. The two tests
turn green when `catalog-api` refuses a request without the shared-secret header.

## Validation of `security.yml`

`actionlint` is not installed on my machine, so I did not run it. I checked the file with PyYAML: it parses as valid YAML, the
trigger is `pull_request` on `develop`, `qa` and `main`, and the three jobs (`secret-scan`, `dependency-audit`,
`authorization-tests`) each have `runs-on` and steps that use exactly one of `uses` or `run`. This checks the syntax and the
structure, not the GitHub Actions rules; actionlint or a first run in the team repository would check those.

## In the team pipeline

`security.yml` has three gates: a secret scan of the whole history (gitleaks), an audit of the Python dependencies
(`pip-audit`) and this negative test. The test needs a running `catalog-api`, so the job reads its address from the
repository variable `CATALOG_URL` and fails if it is not set. If the team adopts it, the test moves to `tests/security/` of
`amaranta-shop-catalog-api`.
