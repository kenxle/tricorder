> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Choosing the right API

## Overview

Wokelo's API suite is organized into four capability groups. Use this page to find the right API for your use case.

| # | API | Type | Description |
| :- | :- | :- | :- |
| 1 | Market Map | Async | Ranked company discovery within a market category |
| 2 | Target Screening | Async | Scored acquisition targets for a defined acquirer |
| 3 | Buyer Screening | Async | Scored buyers for a defined target company |
| 4 | Competitor List | Async | Find peers of a given company |
| 5 | M\&A Activity | Async | Find all the acquisition activities of a given company |
| 6 | Fundraising Activity | Async | Find all the fundrasing activities of a given company |
| 7 | Company Research | Async | In-depth company intelligence report |
| 8 | Industry Research | Async | End-to-end sector coverage report |
| 9 | Peer Comparison | Async | Side-by-side peer benchmarking report |
| 10 | Earnings Analysis | Async | Earnings highlights, guidance, and sentiment report |
| 11 | Custom Workflow | Async | Build and trigger custom research workflows via API |

> [!NOTE]
>
> APIs marked **Async** return a `request_id` immediately. You must poll `/request-status/` and then call `/request-result/` to retrieve the output. [Learn how async APIs work →](https://docs.wokelo.ai/how-async-apis-work)

***

## Discovery

### 1. Market Map

**Overview:** Search and rank companies across Wokelo's 20M+ entity graph using custom parameters such as sector, geography, funding stage, revenue range, headcount, and keywords.

**Endpoint:** `POST /api/enterprise/market-map/enrich/`

**What you get:** A ranked, enriched list of companies matching your criteria — each with firmographics, funding data, and relevance scoring.

**Use Cases:** Deal sourcing, coverage universe building, competitive mapping, BD prospecting, whitespace identification.

**Best for:** Situations where you have a thesis or category in mind and need a long list of matching companies to work from.

***

### 2. Target Screening

**Overview:** Generate a scored list of acquisition or investment targets for a defined acquirer. Applies Wokelo's entity graph and configurable scoring logic — filtering by sector, geography, headcount, revenue, funding stage, and more.

**Endpoint:** `POST /api/enterprise/target-screening/enrich/`

**What you get:** Ranked targets with rationale, firmographic data, fit scores, and filtering metadata.

**Use Cases:** Buy-side M\&A screening, platform add-on identification, sector roll-up targeting, investment thesis validation, partnership candidate identification.

**Best for:** Structured deal origination workflows where you need a scored, filterable list of candidates matched to a specific acquirer's criteria.

***

### 3. Buyer Screening

**Overview:** Identify potential strategic and financial buyers for a target company. Uses Wokelo's entity graph and scoring logic to surface the most relevant acquirers based on strategic fit, sector overlap, and deal profile.

**Endpoint:** `POST /api/enterprise/buyer-screening/enrich/`

**What you get:** Ranked buyer list with strategic rationale, buyer type classification (strategic vs. financial), and fit scoring.

**Use Cases:** Sell-side M\&A process preparation, exit planning, fundraising target identification, secondary sale preparation.

**Best for:** Sell-side advisors and founders looking to build a qualified buyer universe quickly — particularly useful early in a process.

***

### 4. Competitor List

**Overview:** Discover companies similar to a given company, filtered by geography, funding stage, headcount, financials, and more — powered by Wokelo's 20M+ entity graph. Returns results synchronously.

**Endpoint:** `POST /api/enterprise/company-peers/enrich/`

**What you get:** A list of peer companies with firmographic data, similarity scoring, and filter metadata.

**Use Cases:** Competitive benchmarking, peer set construction, deal sourcing, coverage universe building, comparable company analysis.

**Best for:** Quickly building a peer set or competitive landscape for a given company — without manually curating lists.

***

### 5. M\&A Activity

**Overview:** Generate a structured, in-depth acquisitions report for a specific company, providing intelligence on acquisition history, target company profiles, and the broader M\&A landscape. This is an asynchronous API — it returns a `report_id` that you use with the Report Status and Download Report endpoints to retrieve results.

**Endpoint:** `POST /api/assets/process_common/`

**What you get:** A comprehensive M\&A workflow report covering a company's acquisition activity, details on acquired targets, and contextual analysis of its M\&A strategy — filterable by geography, company type, funding stage, and headcount.

**Use Cases:** Tracking acquirer behavior, sourcing acquisition targets, understanding a company's inorganic growth strategy, competitive intelligence on M\&A patterns, deal origination research.

**Best for:** Situations where you need to understand how actively a company acquires, what kinds of targets it pursues, or want to map the M\&A landscape around a specific player.

***

### 6. Fundraising Activity

**Overview:** Generate a structured, in-depth fundraising report for a specific company, providing intelligence on funding rounds, investor landscape, and funding stage progression. This is an asynchronous API — it returns a `report_id` that you use with the Report Status and Download Report endpoints to retrieve results.

**Endpoint:** `POST /api/assets/process_common/`

**What you get:** A comprehensive fundraising workflow report covering a company's funding history, key investors, round details, and analysis of its capital-raising trajectory — filterable by geography, company type, funding stage, and headcount.

**Use Cases:** Investor research, tracking funding activity in a sector, identifying recently funded companies as potential targets or partners, monitoring portfolio company fundraising, sourcing for outreach.

**Best for:** Situations where you need a complete picture of a company's financing history, want to understand its investor base, or are tracking fundraising signals across a market.

***

## Workflow Reports

Workflow APIs generate full-length research reports. All are asynchronous — they return a `report_id` that you use to poll for status and retrieve results.

### 7. Company Research

**Overview:** Generate a comprehensive company intelligence report covering 19 sections including firmographics, products and services, strategic moves, management profiles, financials, funding history, competitive landscape, and alternative signals.

**Endpoint:** `POST /api/workflow_manager/start/` with `"workflow": "company_primer"`

**What you get:** A structured JSON report with the following sections:

`Quick Snapshot` · `Executive Summary` · `Product insights` · `Transaction highlights` · `Strategic moves and news` · `Earnings call highlights` · `Annual report highlights` · `Customer and business insights` · `Financial summary` · `Ownership structure` · `Management profiles` · `Headcount and hiring trends` · `Competitive landscape` · `Wokelo insights` · `Web and social footprint` · `Market insights` · `Annexure` · `meta` · `qna`

**Use Cases:** Target deep-dives, investment memo inputs, client briefings, IC memo preparation, LP reporting.

**Best for:** Situations where you need a complete, structured intelligence package on a company — replacing hours of manual research with a single API call.

***

### 8. Industry Research

**Overview:** Generate a comprehensive sector coverage report covering market structure, deal activity, partnerships, market sizing, competitive landscape, regulatory environment, case studies, and more.

**Endpoint:** `POST /api/workflow_manager/start/` with `"workflow": "industry_research"`

**What you get:** A structured JSON report spanning market overview, key players, competitive dynamics, deal trends, regulations, and thematic signals.

**Use Cases:** Market entry analysis, client engagements, thematic research, fund thesis validation, new vertical entry, sector coverage initiation.

**Best for:** Situations where you need end-to-end sector intelligence — from sizing and structure to competitive dynamics and regulatory signals — in a single report.

***

### 9. Peer Comparison

**Overview:** Benchmark up to 5 companies side-by-side across key business and financial dimensions. Generates a structured comparison report with custom parameters.

**Endpoint:** `POST /api/workflow_manager/start/` with `"workflow": "peer_comparison"`

**What you get:** A structured comparison report covering product positioning, financials, headcount, funding, strategic priorities, and competitive differentiation across all input companies.

**Use Cases:** Competitive benchmarking, portfolio benchmarking, relative value analysis, IC presentation inputs.

**Best for:** Diligence and coverage workflows where you need a structured, side-by-side view of multiple companies — replacing manual comparison grids.

***

### 10. Earnings Analysis

**Overview:** Generate a structured report extracting key highlights, guidance, and sentiment from earnings calls and SEC filings for any public company.

**Endpoint:** `POST /api/workflow_manager/start/` with `"workflow": "earnings_analysis"`

**What you get:** Structured extraction of management commentary, forward guidance, analyst Q\&A highlights, sentiment signals, and comparison to prior period themes.

**Use Cases:** Earnings monitoring, portfolio review, public company coverage, long/short signal generation, consensus vs. actual tracking.

**Best for:** Public equity workflows requiring fast, structured extraction from earnings events — particularly useful for tracking guidance changes and sentiment shifts across multiple companies.

***

### 11. Custom Workflow

**Overview:** Build a custom research workflow in Wokelo's no-code agent builder — applying your own frameworks, section templates, and analytical methodologies — then trigger it via API in supported output formats (JSON, DOCX, PDF).

**Endpoint:** `POST /api/workflow_manager/start/` with your custom `"workflow"` identifier

**What you get:** Output in your configured format, following your defined structure and analytical framework. Supports Wokelo's full intelligence stack as underlying data sources.

**Use Cases:** Repeatable internal research, custom client deliverables, proprietary scoring models, white-label research delivery, automated report generation pipelines.

**Best for:** Teams with established research frameworks who want to automate report generation at scale — without being constrained to Wokelo's default report templates.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.