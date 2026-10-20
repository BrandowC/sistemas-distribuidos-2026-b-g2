# 06 - Alert policy

The rules are in `06-alerts.yml` and protect SLO 1 of `05-slo.md`: availability of the product list
of `catalog-api`, 99.5 % over 30 days, which is a budget of 90 failed reads or 216 minutes a month
(18,000 reads, 43,200 minutes).

## What each alert means

The burn rate is how many times faster than allowed the budget is being spent. At a burn rate of 1
the budget lasts exactly the 30 days (720 hours). The threshold of each alert is its burn rate times
the budget of 0.005.

| | Fast burn | Slow burn |
|---|---|---|
| Alert | `CatalogListFastBurn` | `CatalogListSlowBurn` |
| Burn rate | 14.4 | 6 |
| Long window / confirmation | 1 hour / 5 minutes | 6 hours / 30 minutes |
| Reads that must fail | more than 14.4 x 0.5 % = **7.2 %** | more than 6 x 0.5 % = **3 %** |
| Budget spent before it fires | 14.4 x 1 / 720 = **2 %** | 6 x 6 / 720 = **5 %** |
| In requests | 2 % of 90 = 1.8, about **2 failed reads** | 5 % of 90 = 4.5, about **5 failed reads** |
| In minutes of full outage | 2 % of 216 = **4.3 min** | 5 % of 216 = **10.8 min** |
| If it kept burning at that rate | the budget is gone in 720 / 14.4 = **50 hours** | the budget is gone in 720 / 6 = **120 hours (5 days)** |
| Severity | `critical`: someone looks at it now | `warning`: someone looks at it today |

Both alerts need two windows at once. The long one shows that the problem is real and not a single
bad minute, and the short one shows that it is still happening, so the alert stops by itself soon
after the service recovers.

A total outage is a burn rate of 100 % / 0.5 % = 200. The fast alert fires after about 4.3 minutes,
the time it takes 7.2 % of the hour to fail, and the slow one after about 10.8 minutes.

## A minimum of traffic

Our traffic is small: about 25 list reads an hour. Two failed reads in one hour are already 8 %, above
the 7.2 % of the fast alert. That is noise, not an incident. So both alerts also ask for a minimum of
valid reads in their long window: 10 in one hour for the fast alert and 50 in six hours for the slow
one. The price is that a night outage with almost no visitors can go unnoticed for longer. We accept
it: nobody is hurt when nobody is reading.

## Known blind spot

When `catalog-api` is down it exports no metrics at all, so a ratio computed from its own metrics is
empty and no alert fires. The measure that sees that case is the gateway, which answers
`503 SERVICE_UNAVAILABLE` and counts it in `gateway_requests_total` (target design of
`04-metrics.md`). The same rules, with that metric, close the gap. Until then, a person has to
notice a total outage by hand.

## Alerts on causes that we will not create

| Alert we do not create | Why not |
|---|---|
| MongoDB CPU above 80 % | It is a cause, not a symptom. Reading 12 products by an index can run at a high CPU with fast answers, and a real failure can happen at 10 % CPU. It would wake us for nothing and miss real failures. The burn rate fires when visitors are hurt, whatever the cause. |
| `catalog-api` container restarted | A restart of a few seconds loses almost no read at our traffic, so paging for each one trains the team to ignore pages. When restarts do hurt visitors, the burn rate alert already fires, and the restart is then one more clue in the runbook. |
