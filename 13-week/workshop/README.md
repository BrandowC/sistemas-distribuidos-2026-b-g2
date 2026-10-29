# W13 Workshop - Threat modeling for Amaranta Shop

Individual workshop, delivery 1, Sistemas Distribuidos 2026-B, group 2.

<!-- CONFIG-START -->
- FULL_NAME: Brandow Stivent Claros Polania
- GITHUB_USER: BrandowC
- TEAM: amaranta-shop (Group 2)
- DOCS_REPO: https://github.com/code-corhuila/amaranta-shop-docs
- BOUNDARY: sales-api to catalog-api, the internal stock endpoints (POST /internal/products/reserve-stock and release-stock)
- CLAIM_ISSUE: https://github.com/code-corhuila/amaranta-shop-docs/issues/34
- REFLECTION_DOC: https://docs.google.com/document/d/1138oyhIXT3e3PBRl7bsQbHQAXY4Q0-hrJmX9M3qR5iA/edit?tab=t.0
- LIBRARY_BOOK:
- LIBRARY_RECORD_TIME:
- STORIES:
<!-- CONFIG-END -->

## My boundary

I analyze the trust boundary between `sales-api` and `catalog-api` on the platform network. To take the stock of an
order, `sales-api` calls `POST /internal/products/reserve-stock`, and `release-stock` to give it back when the order cannot
be saved. The gateway never publishes these routes and they ask for no credential: decision OD-3 of the checkout spec
trusts the Docker network. The security policy of the team `-docs` asks for Zero Trust inside the internal network, so this
boundary is where the two documents disagree.

## Files of this folder

| File | Checkpoint |
|---|---|
| `README.md` | CP0 |
| `01-attack-surface.md` | CP1 |
| `04-security-ci/` (`security.yml`, the negative test, `HOW-TO-RUN.md`) | CP4 |

The STRIDE analysis is in the team `-docs` repository, in the pull request of the branch `security/stride-BrandowC` (CP2).
