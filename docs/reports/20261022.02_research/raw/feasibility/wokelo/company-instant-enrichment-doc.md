> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Company Instant Enrichment

> Retrieve structured firmographic, funding, financial, M&A, headcount, and web traffic data for any company from Wokelo's native database of 20M+ cached companies — synchronously for a single company, or asynchronously in batch for multiple companies at once.

## 1. Overview

The Company Instant Enrichment API delivers structured data for any company from Wokelo's native database of 20M+ pre-cached companies. Results are returned within seconds for a single company, or asynchronously for batch enrichment of multiple companies simultaneously.

**Two endpoints, two usage patterns:**

| | Single Enrichment | Batch Enrichment |
| - | - | - |
| **Endpoint** | `POST /api/enterprise/company/enrich/single/` | `POST /api/enterprise/company/enrich/` |
| **Input** | `company` (single string) | `companies` (array of strings) |
| **Response pattern** | **Synchronous** — data returned immediately in the HTTP response | **Asynchronous** — returns `request_id`; poll until complete |
| **Speed** | Results within \~10 seconds | Depends on company count and sections |
| **Use case** | Real-time lookups, CRM enrichment on demand | Bulk watchlist enrichment, pipeline ingestion |

Both endpoints support the same nine structured data sections, and the batch endpoint additionally accepts all nine [Company Deep Intelligence](/company-deep-intelligence-doc) section types in the same request.

**The nine structured data sections:**

| Section | What you get |
| - | - |
| `firmographics` | Name, HQ, industry, founding year, operating status, description, ticker |
| `gtm_and_business_model` | Business model, customer segments, revenue streams, pricing strategy |
| `headcount` | Employee count, LinkedIn headcount, headcount growth trends |
| `funding` | All funding rounds with amounts, investors, round types, and linked news; total raised, funding stage, key investors |
| `public_company_financials` | Revenue, margins, market cap, valuation multiples — public companies only |
| `acquisitions` | Full M\&A history: targets, dates, amounts, descriptions |
| `investments` | Portfolio investments made by the company: investee names, round types, dates |
| `website_traffic` | Monthly visits, traffic sources, geographic distribution |
| `uk_private_company_financials` | Income statement and balance sheet data for UK-registered private companies |
| `uk_private_company_ownership` | Lists the shareholders of a UK private company, including shareholdings, share type/class, ownership percentage, shareholder identity, and historical share issuance details. |
| `social_media` | Linkedin and X(former Twitter) URLs and follower counts |

**Common use cases:**

* **CRM enrichment on demand** — call the single endpoint in a webhook or Zapier flow to instantly populate Salesforce, HubSpot, or DealCloud records when a new company is added
* **Deal screening data pull** — request `firmographics` + `funding` + `acquisitions` for a shortlist of targets before a deal team meeting
* **Watchlist bulk enrichment** — batch enrich hundreds of portfolio or prospect companies overnight with `headcount` + `public_company_financials` + `website_traffic` for a regular market pulse report
* **Funding intelligence** — pull `funding` for a set of companies to map investor syndicates, identify lead investors, and track round progression
* **UK private company financials** — use `uk_private_company_financials` to pull Companies House financials for UK-based private targets where Crunchbase data is thin

> [!NOTE]
>
> The Single Enrichment endpoint is **synchronous** — data is returned directly in the HTTP response. The Batch Enrichment endpoint is **asynchronous** — it returns a `request_id` and requires polling. The two endpoints and response patterns are not interchangeable.

***

## 2. Quick Start

**Single enrichment — synchronous, result in the response**

```bash cURL theme={"system"}
curl --location 'https://api.wokelo.ai/api/enterprise/company/enrich/single/' \
  --header 'Authorization: Bearer <YOUR_API_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
    "company": "tesla-motors",
    "sections": ["firmographics"]
  }'
```

```python Python theme={"system"}
import requests

response = requests.post(
    "https://api.wokelo.ai/api/enterprise/company/enrich/single/",
    headers={
        "Authorization": "Bearer <YOUR_API_TOKEN>",
        "Content-Type": "application/json"
    },
    json={
        "company": "tesla-motors",
        "sections": ["firmographics"]
    }
)
data = response.json()
print(data["data"]["firmographics"]["name"])   # "Tesla Motors"
```

**Batch enrichment — async, poll for completion**

```python theme={"system"}
import requests, time

API_KEY = "<YOUR_API_TOKEN>"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Step 1: Submit
submit = requests.post(
    "https://api.wokelo.ai/api/enterprise/company/enrich/",
    headers=HEADERS,
    json={
        "companies": ["tesla-motors", "stripe"],
        "sections":  ["firmographics", "funding"]
    }
)
request_id = submit.json()["request_id"]
print(f"Submitted. request_id: {request_id}")

# Step 2: Poll
while True:
    r = requests.get(
        "https://api.wokelo.ai/api/enterprise/request/status/",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"request_id": request_id}
    )
    data = r.json()
    status = data.get("status")
    print(f"Status: {status}")
    if status == "COMPLETED":
        result = data["result"]
        break
    if status == "FAILED":
        raise Exception("Request failed")
    time.sleep(10)

# Step 3: Use the result
for company_key, company_data in result.items():
    print(f"{company_key}: {company_data.get('firmographics', {}).get('name')}")
```

***

## 3. Authentication

All requests must include a **Bearer token** in the `Authorization` HTTP header.

```text theme={"system"}
Authorization: Bearer <YOUR_API_TOKEN>
```

API tokens are issued from your Wokelo account. Navigate to **Account Details → API Credentials** in the Wokelo dashboard to get your client id and client secret. Contact [support@wokelo.ai](mailto:support@wokelo.ai) if you do not yet have API access.

> [!WARNING]
>
> Never expose your token in client-side code, browser requests, or public repositories. A missing or invalid token returns `401 Unauthorized`. A valid token without sufficient plan permissions returns `403 Forbidden`.

***

## 4. Request Reference

### Single Enrichment

**Endpoint**

```text theme={"system"}
POST https://api.wokelo.ai/api/enterprise/company/enrich/single/
```

| Parameter | Type | Required | Description |
| - | - | - | - |
| `company` | string | **Required** | Permalink or URL of the company to enrich. Permalinks (e.g. `"canva"`, `"tesla-motors"`) resolve faster. Full URLs (e.g. `"https://tesla.com"`) are also accepted. Use the [Company Search API](/supporting-apis-doc#company-search) to look up a permalink by name. |
| `sections` | string\[] | **Required** | Array of section identifiers to include. Defaults to all sections if omitted. Request only what you need — each additional section adds processing time. |

**Full request example:**

```bash cURL theme={"system"}
curl --location 'https://api.wokelo.ai/api/enterprise/company/enrich/single/' \
  --header 'Authorization: Bearer <YOUR_API_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
    "company": "canva",
    "sections": [
      "firmographics",
      "funding",
      "investments",
      "acquisitions"
    ]
  }'
```

```python Python theme={"system"}
import requests

response = requests.post(
    "https://api.wokelo.ai/api/enterprise/company/enrich/single/",
    headers={
        "Authorization": "Bearer <YOUR_API_TOKEN>",
        "Content-Type": "application/json"
    },
    json={
        "company": "canva",
        "sections": ["firmographics", "funding", "investments", "acquisitions"]
    }
)
print(response.json())
```

### Batch Enrichment

**Endpoint**

```text theme={"system"}
POST https://api.wokelo.ai/api/enterprise/company/enrich/
```

| Parameter | Type | Required | Description |
| - | - | - | - |
| `companies` | string\[] | **Required** | Array of company permalinks or URLs to enrich. Accepts 1–N entries. All companies are processed in parallel. |
| `sections` | string\[] | **Required** | Array of section identifiers to include. Same 9 structured sections as Single Enrichment, plus all 9 [Company Deep Intelligence](/company-deep-intelligence-doc) sections (`products_and_services`, `product_launches`, `strategic_initiatives`, `partnerships`, `business_model`, `key_customers`, `management_profiles`, `employee_sentiment`, `product_sentiment`). |

> [!NOTE]
>
> The Batch endpoint accepts both the structured data sections listed in Section 1 and the full set of Company Deep Intelligence sections. This means you can fetch firmographics, funding, and AI-synthesised product narratives in a single batch request. See the [Company Deep Intelligence API](/company-deep-intelligence-doc) for documentation on those additional sections.

**Full request example:**

```bash cURL theme={"system"}
curl --location 'https://api.wokelo.ai/api/enterprise/company/enrich/' \
  --header 'Authorization: Bearer <YOUR_API_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
    "companies": ["tesla-motors", "stripe"],
    "sections": ["firmographics", "products", "funding"]
  }'
```

```python Python theme={"system"}
import requests

response = requests.post(
    "https://api.wokelo.ai/api/enterprise/company/enrich/",
    headers={
        "Authorization": "Bearer <YOUR_API_TOKEN>",
        "Content-Type": "application/json"
    },
    json={
        "companies": ["tesla-motors", "stripe"],
        "sections": ["firmographics", "products", "funding"]
    }
)
print(response.json())
# {"request_id": "931643e9-b6c7-45d4-9ba9-bd3b534221e7", "status": "PENDING"}
```

***

## 5. Response

### Single Enrichment response

The single endpoint returns a `200 OK` synchronously with the enriched data in the `data` field:

```json theme={"system"}
{
  "status": "success",
  "data": {
    "firmographics": { ... },
    "funding": { ... },
    "acquisitions": [ ... ],
    "investments": [ ... ]
  }
}
```

| Field | Type | Description |
| - | - | - |
| `status` | string | `"success"` when data was returned successfully. |
| `data` | object | Dict keyed by section name. Only the sections you requested are present. |

### Batch Enrichment submission response

The batch endpoint returns a `202 Accepted` immediately:

```json theme={"system"}
{
  "request_id": "931643e9-b6c7-45d4-9ba9-bd3b534221e7",
  "status": "PENDING"
}
```

| Field | Type | Description |
| - | - | - |
| `request_id` | string (UUID) | Use with `GET /api/enterprise/request/status/` to poll for completion. Store immediately — there is no endpoint to recover a lost `request_id`. |
| `status` | string | Always `"PENDING"` on submission. |

### Batch Enrichment polling and result

Poll `GET /api/enterprise/request/status/?request_id={request_id}` until `status` is `"COMPLETED"`. The full result is embedded in the polling response:

| Status | Meaning |
| - | - |
| `"PENDING"` | Queued, waiting to start. |
| `"PROCESSING"` | In progress. |
| `"COMPLETED"` | Done. The `result` field contains all company data. |
| `"FAILED"` | Failed. Retry the submission. |

When completed, `result` is a **dict keyed by company identifier** — one entry per company in your `companies` array. Each company object has section data at the top level (not nested under `"data"`):

```json theme={"system"}
{
  "request_id": "...",
  "status": "COMPLETED",
  "result": {
    "tesla-motors": {
      "firmographics": { ... },
      "funding": { ... }
    },
    "stripe": {
      "firmographics": { ... },
      "funding": { ... }
    }
  }
}
```

### Section-level response schemas

**`firmographics`**

```json theme={"system"}
{
  "name": "Canva",
  "website": "http://www.canva.com",
  "location": "Sydney, Australia",
  "founded": 2013,
  "type": "private",
  "operating_status": "Operating",
  "ticker": null
}
```

| Field | Type | Description |
| - | - | - |
| `name` | string | Company display name. |
| `website` | string | Canonical website URL. |
| `location` | string | City and country of HQ. |
| `founded` | integer | Year founded. |
| `type` | string | `"public"`, `"private"`, or `"startup"`. |
| `operating_status` | string | `"Operating"`, `"Acquired"`, `"IPO"`, or similar. |
| `ticker` | string or null | Stock ticker (e.g. `"NASDAQ:FRSH"`). `null` for private companies. |

**`funding`**

Contains two keys: `overall` (aggregate summary) and `funding_rounds` (per-round array), plus `key_investors` array.

`overall` fields:

| Field | Type | Description |
| - | - | - |
| `funding_stage` | string | Most recent round type (e.g. `"Series F"`, `"Secondary Market"`). |
| `total_funding` | float | Total capital raised in raw USD (e.g. `2508450682.0` = \$2.51B). |
| `last_funding_date` | string | Date of most recent funding event (`YYYY-MM-DD`). |
| `num_funding_rounds` | string | Total number of rounds as a string (e.g. `"21"`). |
| `key_investors` | string\[] | Flat list of all investor names across all rounds. |

Each `funding_rounds` object:

| Field | Type | Description |
| - | - | - |
| `date` | string | Round close date (`YYYY-MM-DD`). |
| `round` | string | Round type (e.g. `"Series A"`, `"Seed"`, `"Venture"`, `"Debt"`, `"Private Equity"`). |
| `amount` | float | Amount raised in raw USD. `0.0` when the amount was not publicly disclosed — not `null`. |
| `total_investors` | integer or string | Number of investors. May be `"-"` when count is unknown. |
| `lead_investors` | string\[] | Names of lead investors. Empty array when not disclosed. |
| `investors` | string\[] | Names of non-lead investors. Empty array when not disclosed. |
| `pre_money_valuation` | float or null | Pre-money valuation if available. Usually `null`. |
| `news` | object | `{type: "news", data: [{publisher, news_url, news_title}]}` — press coverage of the round. |

`key_investors` array (top-level in funding):

| Field | Type | Description |
| - | - | - |
| `name` | string | Investor name. |
| `permalink` | string | Wokelo/Crunchbase permalink for the investor entity. |
| `type` | string | Investor type: `"angel"`, `"investment_partner"`, or empty string for institutional. |
| `first_entry_date` | string | Date of their first investment in this company (`YYYY-MM-DD`). |
| `rounds_participated` | string\[] | List of round types they participated in. |

**`acquisitions`**

Array of acquisition objects:

| Field | Type | Description |
| - | - | - |
| `acquisition_date` | string | Date of acquisition (`YYYY-MM-DD`). |
| `name` | string | Descriptive name (e.g. `"Doohly acquired by Canva"`). |
| `amount` | float or null | Raw USD deal amount. `null` when undisclosed. |
| `amount_usd` | float or null | Same as `amount` — present for compatibility. |
| `description` | string | One-line summary of the deal. |
| `acquiree_name` | string | Name of the company acquired. |
| `acquiree_permalink` | string | Permalink of the acquired company. |

**`investments`**

Array of investment objects made by the company:

| Field | Type | Description |
| - | - | - |
| `announcement_date` | string | Investment announcement date (`YYYY-MM-DD`). |
| `amount` | float or null | Investment amount in raw USD. `null` when undisclosed. |
| `amount_usd` | float or null | Same as `amount`. |
| `description` | string | One-line summary (e.g. `"Canva investment in Series B - Black Forest Labs"`). |
| `lead_investor` | boolean | Whether this company was the lead investor. |
| `funding_round_id` | string | Wokelo/Crunchbase ID for the funding round. |
| `investee_name` | string | Name of the company invested in. |
| `investee_permalink` | string | Permalink of the investee. |

> [!NOTE]
>
> In `funding_rounds`, an `amount` of `0.0` means the round amount was **not publicly disclosed** — it is not a zero-dollar round. Always distinguish between `0.0` (undisclosed) and a genuine small amount. In `acquisitions`, an undisclosed deal amount is represented as `null`, not `0.0`.

***

## 6. Examples

### PE deal screening — firmographics, funding, and M\&A for a target

```bash cURL theme={"system"}
curl --location 'https://api.wokelo.ai/api/enterprise/company/enrich/single/' \
  --header 'Authorization: Bearer <YOUR_API_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
    "company": "canva",
    "sections": ["firmographics", "funding", "investments", "acquisitions"]
  }'
```

```python Python theme={"system"}
import requests

API_KEY = "<YOUR_API_TOKEN>"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

response = requests.post(
    "https://api.wokelo.ai/api/enterprise/company/enrich/single/",
    headers=HEADERS,
    json={
        "company": "canva",
        "sections": ["firmographics", "funding", "investments", "acquisitions"]
    }
)

data = response.json()["data"]

# Firmographics
firm = data["firmographics"]
print(f"{firm['name']} | {firm['type']} | {firm['operating_status']} | {firm['location']}")

# Funding summary
overall = data["funding"]["overall"]
total_b = overall["total_funding"] / 1e9
print(f"Total funding: ${total_b:.1f}B | Stage: {overall['funding_stage']} | Rounds: {overall['num_funding_rounds']}")
print(f"Last round: {overall['last_funding_date']}")

# Most recent 3 rounds
print("\nRecent rounds:")
for round_ in data["funding"]["funding_rounds"][:3]:
    amt = round_["amount"]
    amt_str = f"${amt/1e6:.0f}M" if amt > 0 else "undisclosed"
    print(f"  {round_['date']}  {round_['round']}  {amt_str}  Lead: {', '.join(round_['lead_investors']) or 'N/A'}")

# Acquisitions
print(f"\nAcquisitions ({len(data['acquisitions'])}):")
for acq in data["acquisitions"][:5]:
    amt = acq.get("amount")
    amt_str = f"${amt/1e6:.0f}M" if isinstance(amt, (int, float)) and amt > 0 else "undisclosed"
    print(f"  {acq['acquisition_date']}  {acq['acquiree_name']}  ({amt_str})")
```

**Sample submission response (single):**

```json theme={"system"}
{
  "status": "success",
  "data": {
    "firmographics": {
      "name": "Canva",
      "website": "http://www.canva.com",
      "location": "Sydney, Australia",
      "founded": 2013,
      "type": "private",
      "operating_status": "Operating",
      "ticker": null
    },
    "funding": {
      "overall": {
        "funding_stage": "Secondary Market",
        "total_funding": 2508450682.0,
        "last_funding_date": "2025-08-20",
        "num_funding_rounds": "21",
        "key_investors": ["Blackbird Ventures", "Felicis", "T. Rowe Price", "..."]
      },
      "funding_rounds": [ { ... } ],
      "key_investors": [ { ... } ]
    },
    "acquisitions": [
      {
        "acquisition_date": "2026-04-08",
        "name": "Simtheory acquired by Canva",
        "amount": null,
        "amount_usd": null,
        "description": "Canva acquires Simtheory on 2026-04-08 for an undisclosed amount",
        "acquiree_name": "Simtheory",
        "acquiree_permalink": "simtheory"
      }
    ],
    "investments": [
      {
        "announcement_date": "2025-12-01",
        "amount": null,
        "amount_usd": null,
        "description": "Canva investment in Series B - Black Forest Labs",
        "lead_investor": false,
        "funding_round_id": "black-forest-labs-01de-series-b--b4a4a81b",
        "investee_name": "Black Forest Labs",
        "investee_permalink": "black-forest-labs-01de"
      }
    ]
  }
}
```

### Batch enrichment — multiple companies in one request

Enrich a watchlist of companies in parallel using the async batch endpoint.

```python theme={"system"}
import requests, time

API_KEY = "<YOUR_API_TOKEN>"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Submit
submit = requests.post(
    "https://api.wokelo.ai/api/enterprise/company/enrich/",
    headers=HEADERS,
    json={
        "companies": [
            "salesforce",
            "hubspot",
            "pipedrive",
            "zoho",
            "freshworks"
        ],
        "sections": ["firmographics", "funding", "headcount"]
    }
)
request_id = submit.json()["request_id"]
print(f"Submitted. request_id: {request_id}")

# Poll
while True:
    r = requests.get(
        "https://api.wokelo.ai/api/enterprise/request/status/",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"request_id": request_id}
    )
    data = r.json()
    status = data.get("status")
    print(f"Status: {status}")
    if status == "COMPLETED":
        result = data["result"]
        break
    if status == "FAILED":
        raise Exception("Request failed")
    time.sleep(10)

# Process results
print(f"\n{'Company':<20} {'Type':<10} {'Stage':<20} {'Total Funding'}")
print("-" * 70)
for company_key, company_data in result.items():
    firm = company_data.get("firmographics", {})
    funding = company_data.get("funding", {}).get("overall", {})
    total = funding.get("total_funding", 0)
    total_str = f"${total/1e9:.1f}B" if total >= 1e9 else (f"${total/1e6:.0f}M" if total > 0 else "—")
    print(
        f"{firm.get('name', company_key):<20} "
        f"{firm.get('type', '—'):<10} "
        f"{funding.get('funding_stage', '—'):<20} "
        f"{total_str}"
    )
```

### CRM enrichment — resolve permalink then enrich instantly

Resolve a company name to its permalink via Company Search, then enrich synchronously for a CRM record update.

```python theme={"system"}
import requests

API_KEY = "<YOUR_API_TOKEN>"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def enrich_by_name(company_name, sections):
    # Step 1: resolve permalink
    search = requests.get(
        "https://api.wokelo.ai/api/enterprise/company/search",
        headers=HEADERS,
        params={"query": company_name, "search_by": "name"}
    )
    results = search.json().get("data", [])
    if not results:
        raise ValueError(f"Company not found: {company_name}")
    permalink = results[0]["permalink"]

    # Step 2: enrich
    enrich = requests.post(
        "https://api.wokelo.ai/api/enterprise/company/enrich/single/",
        headers=HEADERS,
        json={"company": permalink, "sections": sections}
    )
    return enrich.json()["data"]

data = enrich_by_name("Stripe", ["firmographics", "funding"])
print(f"{data['firmographics']['name']}: {data['funding']['overall']['total_funding'] / 1e9:.1f}B raised")
```

### Investor syndicate mapping

Pull funding data for a set of companies and identify which investors appear most frequently across the portfolio.

```python theme={"system"}
import requests, time
from collections import Counter

API_KEY = "<YOUR_API_TOKEN>"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

COMPANIES = ["canva", "figma", "miro", "notion", "loom"]

# Batch enrich — funding only
submit = requests.post(
    "https://api.wokelo.ai/api/enterprise/company/enrich/",
    headers=HEADERS,
    json={"companies": COMPANIES, "sections": ["funding"]}
)
request_id = submit.json()["request_id"]

# Poll
while True:
    r = requests.get(
        "https://api.wokelo.ai/api/enterprise/request/status/",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"request_id": request_id}
    )
    data = r.json()
    if data["status"] == "COMPLETED":
        result = data["result"]
        break
    if data["status"] == "FAILED":
        raise Exception("Failed")
    time.sleep(10)

# Map investor → companies
investor_count = Counter()
investor_companies = {}

for company_key, company_data in result.items():
    firm_name = company_data.get("firmographics", {}).get("name", company_key)
    investors = company_data.get("funding", {}).get("overall", {}).get("key_investors", [])
    for inv in investors:
        investor_count[inv] += 1
        investor_companies.setdefault(inv, []).append(firm_name)

print("Top cross-portfolio investors:")
for inv, count in investor_count.most_common(10):
    cos = ", ".join(investor_companies[inv])
    print(f"  {inv} ({count} companies): {cos}")
```

### Batch with mixed structured and Deep Intelligence sections

Combine `firmographics` + `funding` (structured) with `products_and_services` (Deep Intelligence) in one batch call.

```python theme={"system"}
submit = requests.post(
    "https://api.wokelo.ai/api/enterprise/company/enrich/",
    headers=HEADERS,
    json={
        "companies": ["zendesk", "freshworks"],
        "sections": [
            "firmographics",
            "funding",
            "products_and_services",    # Deep Intelligence section
            "product_launches"          # Deep Intelligence section
        ]
    }
)
request_id = submit.json()["request_id"]
# Poll and retrieve as normal
```

### JavaScript / Node.js — single enrichment

```javascript theme={"system"}
const fetch = require("node-fetch");

async function enrichCompany(company, sections) {
  const response = await fetch(
    "https://api.wokelo.ai/api/enterprise/company/enrich/single/",
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.WOKELO_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ company, sections })
    }
  );

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  const json = await response.json();
  return json.data;
}

// Example: funding snapshot for Canva
enrichCompany("canva", ["firmographics", "funding"]).then(data => {
  const { name } = data.firmographics;
  const { total_funding, funding_stage } = data.funding.overall;
  const totalB = (total_funding / 1e9).toFixed(1);
  console.log(`${name}: $${totalB}B raised | Stage: ${funding_stage}`);
});
```

***

## 7. Error Handling

Both endpoints use standard HTTP status codes. The single endpoint returns all errors synchronously. The batch endpoint returns submission errors synchronously; processing errors appear as `"FAILED"` when polling.

| Status | Meaning | Cause & Resolution |
| - | - | - |
| `200 OK` | Single success | Data returned in response body. |
| `202 Accepted` | Batch accepted | `request_id` returned. Proceed to polling. |
| `400 Bad Request` | Invalid parameters | Missing `company` or `companies`, missing `sections`, invalid section name, or empty `companies` array. Check the `detail` field. |
| `401 Unauthorized` | Auth failed | The `Authorization` header is missing or contains an invalid token. Verify your key in **Settings → API Keys**. |
| `403 Forbidden` | Insufficient access | Your plan does not include access to this endpoint or section. Contact [support@wokelo.ai](mailto:support@wokelo.ai). |
| `404 Not Found` | Company not found | The permalink could not be resolved. Verify using the [Company Search API](/supporting-apis-doc#company-search), or try the website URL instead. |
| `429 Too Many Requests` | Rate limit exceeded | Implement exponential back-off. The response includes a `Retry-After` header. |
| `500 Internal Server Error` | Server error | Retry after a brief delay. If the issue persists, contact [support@wokelo.ai](mailto:support@wokelo.ai). |

**Retry with exponential back-off (batch submission):**

```python theme={"system"}
import time, requests

def submit_with_retry(body, api_key, max_retries=3):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    for attempt in range(max_retries):
        try:
            r = requests.post(
                "https://api.wokelo.ai/api/enterprise/company/enrich/",
                headers=headers, json=body, timeout=30
            )
            if r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r.json()["request_id"]
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    raise Exception(f"Submission failed after {max_retries} attempts")
```

***

## 8. Best Practices

**Use Single for real-time lookups; use Batch for bulk enrichment**

The two endpoints serve different workflows. Single Enrichment returns data within \~10 seconds synchronously — ideal for CRM webhook triggers, API-driven form enrichment, and on-demand lookups. Batch Enrichment processes many companies in parallel and is better suited to overnight bulk jobs, watchlist refreshes, and pipeline ingestion tasks where latency is less critical than throughput.

**Use permalinks over URLs for faster resolution**

Permalinks (e.g. `"canva"`, `"tesla-motors"`) resolve from Wokelo's cached index directly, typically within 1–2 seconds. Website URLs trigger a lookup step that adds latency, particularly for companies with non-standard or redirecting domains. Use the [Company Search API](/supporting-apis-doc#company-search) to resolve names to permalinks:

```python theme={"system"}
search = requests.get(
    "https://api.wokelo.ai/api/enterprise/company/search",
    headers=HEADERS,
    params={"query": "Canva", "search_by": "name"}
)
permalink = search.json()["data"][0]["permalink"]   # "canva"
```

**Request only the sections you need**

Both endpoints process each section independently. A single-section request (`firmographics` only) returns in under 5 seconds; a full 9-section request takes longer. For time-sensitive integrations (webhook-driven CRM updates, real-time enrichment), request only the sections you will use immediately.

**Distinguish `0.0` (undisclosed) from `null` (not available) in funding data**

In `funding_rounds`, an `amount` of `0.0` means the round amount was not publicly disclosed — it is not an actual zero-dollar round. In `acquisitions`, an undisclosed deal amount is `null`. Never sum or average `amount` values without filtering out `0.0` entries first:

```python theme={"system"}
# Sum only rounds with disclosed amounts
disclosed_rounds = [r for r in funding_rounds if r["amount"] > 0]
total_disclosed = sum(r["amount"] for r in disclosed_rounds)

# Acquisition amounts — null means undisclosed
for acq in acquisitions:
    amt = acq.get("amount")
    label = f"${amt/1e6:.0f}M" if isinstance(amt, (int, float)) and amt > 0 else "Undisclosed"
```

**`num_funding_rounds` is a string, not an integer**

The `funding.overall.num_funding_rounds` field returns a string (e.g. `"21"`) rather than an integer. Parse it before arithmetic:

```python theme={"system"}
num_rounds = int(data["funding"]["overall"]["num_funding_rounds"])
```

**Batch result keys match the identifiers you submitted**

The batch result is keyed by whatever identifier you passed in the `companies` array. Submit permalinks for predictable, clean keys. Mixing URLs and permalinks in the same request produces mixed key formats in the result:

```python theme={"system"}
# ❌ Mixed formats — inconsistent result keys
companies=["https://canva.com", "hubspot", "https://pipedrive.com"]

# ✅ All permalinks — consistent result keys
companies=["canva", "hubspot", "pipedrive"]
```

**The batch endpoint accepts Deep Intelligence sections alongside structured sections**

The batch endpoint's `sections` parameter accepts both the nine structured data sections documented here and all nine Company Deep Intelligence sections (`products_and_services`, `product_launches`, `strategic_initiatives`, etc.). Use this to fetch firmographics, funding, and AI narratives in a single request — reducing total round-trips. Be aware that Deep Intelligence sections take longer to generate than structured data sections.

**Understand the difference from Company Deep Intelligence**

Company Instant Enrichment returns **raw structured data** from Wokelo's cached database — firmographic fields, funding round records, M\&A history — in seconds. Company Deep Intelligence returns **AI-synthesised narratives** — product portfolio analysis, strategic initiative summaries, sentiment data — in minutes. For CRM enrichment and data pipelines, use Instant Enrichment. For pre-IC product intelligence and competitive sweeps, use Deep Intelligence. For both in one call, use the Batch endpoint with mixed sections.

***

## 9. Related APIs

> **[Company Deep Intelligence](/company-deep-intelligence-doc)**
>
> AI-synthesised intelligence on products, strategy, sentiment, and leadership — section-selective, async, uses the same request\_id pattern as Batch Enrichment.

> **[Company Research](/company-research-doc)**
>
> Full async intelligence report for a single company — Executive Summary, Key Insights, Product Insights, Transaction Highlights — with PDF/DOCX/PPT export.

> **[Company News Monitoring](/company-news-monitoring-doc)**
>
> Real-time, source-cited news articles for any company — synchronous, no polling, complements enrichment data with current event context.

> **[Peer Comparison](/peer-comparison-doc)**
>
> Side-by-side benchmarking of 2–5 companies with financial data, feature matrices, and business model analysis — async Workflow API.

> **[Target Screening](/target-screening-doc)**
>
> AI-ranked acquisition target identification — use before enrichment to build the shortlist, then enrich to populate deal screening data.

> **[Supporting APIs](/supporting-apis-doc)**
>
> Company Search and Request Status — both used alongside Company Instant Enrichment for permalink resolution and batch polling.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.