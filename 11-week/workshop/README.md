# W11 Workshop - Observability for Amaranta Shop

Individual workshop, delivery 1, Sistemas Distribuidos 2026-B, group 2.

<!-- CONFIG-START -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta-shop (Group 2)
- DOCS_REPO: https://github.com/code-corhuila/amaranta-shop-docs
- REFLECTION_DOC: https://docs.google.com/document/d/1TtYVJ_sy1sLXimUXC-Vlaz84JzAWj4WBWvk08Id1wSA/edit?usp=sharing
- JOURNEY:
<!-- CONFIG-END -->

## My part

I work on the Catalog side of the checkout of our project. In the team `-docs` repository the
checkout is `POST /api/v1/orders` on `sales-api`, behind the `api-gateway`. To take the stock,
`sales-api` calls the internal route `reserve-stock` of `catalog-api`, the Python service that owns
the products and their stock. That service is the one I instrument in this workshop.

## Files of this folder

| File | Checkpoint |
|---|---|
| `README.md` | CP0 |
| `01-journey.md` | CP1 |
| `02-log-contract.md` | CP2 |
| `03-instrumentation/` | CP3 |
| `04-metrics.md` | CP4 |

The reflection document is written in Google Docs and linked in the CONFIG block above.
