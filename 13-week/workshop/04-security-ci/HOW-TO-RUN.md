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

## Output of the run

To be filled in CP8 with the real console output.

## In the team pipeline

`security.yml` has three gates: a secret scan of the whole history (gitleaks), an audit of the Python dependencies
(`pip-audit`) and this negative test. The test needs a running `catalog-api`, so the job reads its address from the
repository variable `CATALOG_URL` and fails if it is not set. If the team adopts it, the test moves to `tests/security/` of
`amaranta-shop-catalog-api`.
