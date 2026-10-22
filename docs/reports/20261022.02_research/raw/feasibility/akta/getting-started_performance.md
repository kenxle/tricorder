> ## Documentation Index
> Fetch the complete documentation index at: https://docs.akta.pro/llms.txt
> Use this file to discover all available pages before exploring further.

# akta.pro API Latency

> Reference latency for every akta.pro API endpoint, in p50, p90, and p99 percentiles.

End-to-end latency for every akta.pro API endpoint, in **p50, p90, and p99** percentiles (milliseconds).

> [!NOTE]
>
> Baseline reference numbers from internal performance testing. Live latency varies with filter scope, result-set size, plan tier, and current traffic.

## Latency by endpoint

| Endpoint | p50 | p90 | p99 |
| :- | -: | -: | -: |
| Company Search `/api/v1/company/search/` | 4.9 | 148 | 774 |
| News Signals `/api/v1/news/` | 164 | 1,389 | 17,326 |
| Company Data `/api/v1/company/enrichment/` | 108 | 324 | 1,128 |
| Social Posts `/api/v1/company/posts/` | 89 | 9,761 | 55,589 |
| Headcount Trends `/api/v1/company/headcount-trends/` | 248 | 17,586 | 55,175 |
| Website Traffic `/api/v1/company/website-traffic/` | 76 | 9,180 | 19,300 |
| Employee Reviews `/api/v1/company/employee-reviews/` | 204 | 5,121 | 9,353 |
| Product Reviews `/api/v1/company/product-reviews/` | 154 | 1,926 | 3,252 |
| Job Posts `/api/v1/company/jobs/` | 113 | 25,215 | 70,005 |
| Industry Search `/api/v1/industry/search/` | 154 | 3,330 | 4,171 |
| List Generation `/api/v1/list/generate/companies/` | 327 | 1,547 | 31,562 |
| Filter Options `/api/v1/filters/options/` | 73 | 90 | 102 |
| List Filters `/api/v1/filters/list/` | 13 | 55 | 60 |
| Filter Builder `/api/v1/list/filter-builder/` | 15,550 | 23,771 | 28,443 |

## What drives latency

**[Alternative signals](/docs/alternative-data/job-posts/overview)** — Job Posts, Social Posts, Headcount Trends, Website Traffic, Employee Reviews, Product Reviews — are live-fetched from partner sources. Set client timeouts at 2×–3× p99.

**[News Signals](/docs/news-signals/overview)** and **[List Generation](/docs/list-generation/overview)** accept a free-text `query`. p99 grows with the scan size — scope to a company, industry code, or entity whenever you can. For List Generation, latency also grows with the number of companies returned and the enrichment depth requested, so generate the list first and enrich the rows you actually need in a second call.

***

For limits on request volume, see [Rate limits](/getting-started/rate-limits). For error responses when a request fails, see [Error codes](/getting-started/error-codes).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.