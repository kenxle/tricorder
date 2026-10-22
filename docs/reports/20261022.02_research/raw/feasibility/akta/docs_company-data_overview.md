> ## Documentation Index
> Fetch the complete documentation index at: https://docs.akta.pro/llms.txt
> Use this file to discover all available pages before exploring further.

# Company Data API Overview

> Structured company data across 16 sections

The akta.pro Company Data API returns structured data for any company from akta.pro's native database. Pass a company website domain or UUID and specify which sections you need. Only the requested sections are returned, keeping responses lean and processing fast.

This is a **synchronous GET API**. Pass parameters in the URL and receive enriched company data immediately in the HTTP response. No polling required.

**The available sections:**

| Section | What you get | Fields |
| - | - | - |
| `firmographic` | Firmographics and identity | `name`, `legal_name`, `website`, `company_type`, `founded_year`, `operating_status`, `headcount`, `logo_url` |
| `business_model` | How the company makes money | `gtm_motion`, `revenue_model`, `marketing_channels`, `distribution_channels`, `pricing_details` |
| `company_assessment` | Strengths, risks and summary | `strengths`, `weaknesses`, `opportunities`, `risks`, `summary` |
| `trust_signal` | Compliance, awards and credibility | `compliance`, `regulatory_updates`, `awards` |
| `company_hierarchy` | Parent and subsidiaries | `subsidiaries` |
| `digital_presence` | Web, social and app footprint | `website_traffic`, `social_profiles`, `app_listings`, `seo_rank`, `domain_authority` |
| `financial_estimate` | Estimated financial performance | `est_revenue`, `est_growth_rate`, `est_valuation`, `funding_total`, `profitability` |
| `location` | HQ, offices and markets served | `hq`, `market_served`, `offices` |
| `management_profile` | Founders and executives | `ceo`, `executives`, `founders`, `board_members`, `tenure` |
| `product_offering` | Products, brands and differentiators | `brand`, `differentiator`, `functional_benefit`, `problem_solved`, `quantifiable_outcome`, `product_overview` |
| `strategic_signal` | Partnerships and recent moves | `scale_indicator`, `partnership`, `recent_move`, `leadership_change` |
| `customer_profile` | Segments and customers | `segment`, `customer` |
| `industry` | Industry classification | `primary_industry`, `sub_industry`, `naics_code`, `sic_code`, `sector` |
| `technology` | Tech stack and AI capabilities | `is_technology_focussed`, `api_detail`, `integration`, `ai_capability`, `ai_maturity`, `app_detail`, `feature`, `core_technology` |
| `funding_detail` | Rounds, amounts and dates *(subscription and enterprise tier only)* | `total_raised`, `last_round`, `round_type`, `amount`, `date`, `investors` |
| `mna_and_investment` | Acquisitions and investments *(subscription and enterprise tier only)* | `acquisitions`, `investments`, `acquirers`, `deal_value`, `deal_date` |

> [!NOTE]
>
> `funding_detail` and `mna_and_investment` are only available on subscription and enterprise plans. Requesting them on other plans returns 403 error.

**Common use cases:**

* **CRM enrichment on demand** : call the API from a webhook or automation to instantly populate Salesforce, HubSpot, or DealCloud records when a new company is added, using `firmographic` + `location` + `management_profile` as the base record
* **Deal screening data pull** : request `firmographic` + `financial_estimate` + `funding_detail` + `mna_and_investment` for a shortlist of targets to build a fast pre-IC data pack
* **Funding intelligence** : pull `funding_details` and `financial_estimate` for a set of companies to map raise history, identify stage, and track total capital deployed
* **Traffic and growth signals** : combine `digital_presence` and `financial_estimate` to proxy revenue trajectory and growth momentum for private companies
* **Competitive and market mapping** : use `industry`, `product_offering`, and `strategic_signal` together to compare positioning, differentiators, and recent moves across a peer set
* **Tech stack and AI maturity screening** : request `technology` on its own to assess a company's AI capabilities and core stack without pulling unrelated sections

> [!NOTE]
>
> This API is synchronous. Enriched data is returned directly in the HTTP response. No job submission or polling required.

***


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.