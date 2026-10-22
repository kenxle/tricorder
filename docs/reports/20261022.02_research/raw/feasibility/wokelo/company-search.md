> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Company Search

> Search for companies using name, website, or ticker. Returns a list of companies with their permalink and other attributes.

## Overview

Search for companies using name, website or ticker. It returns a list of companies with their permalink and other attributes.

## Endpoint Details

* **Method:** GET
* **Endpoint:** `/api/enterprise/company/search`

## Authentication requirements

* Include a valid JWT token in your request header
* If you don't have a token yet, you can get one from the `/auth/token/` endpoint first.

## Request

#### Header Parameters

**Authorization** `string` *required*

JWT token obtained from the Authentication request

#### URL Parameters

**query** `string` *required*

The search query string (e.g., company name, website or ticker).

Examples: Tesla OR `https://tesla.com` OR TSLA

**search\_by** `string`

Field to search by. Supported value: `name`, `website`, `ticker`

**company\_type** `string`

Filter by company type. Supported values: `private`, `public`, `all`

Note: Use `all` to return all types. (This is the default value is nothing is mentioned)

## Response

**Successful Response Fields**

Returns a JSON object with the following structure:

**status** `string`

`"success"` if the request was processed successfully.

**data** `array`

List of matching company objects.

**count** `integer`

Total number of results returned.

**Company Object Fields**

| Field | Description |
| - | - |
| `name` | Company name. |
| `permalink` | Unique identifier/slug for the company. |
| `short_description` | Brief description of the company. |
| `founded_year` | Year the company was founded. |
| `ipo_status` | IPO status (e.g., `private`, `public`). |
| `hq` | Headquarters location. |
| `industries` | Industry or sector the company operates in. |
| `website` | Company website URL. |
| `ticker` | Stock ticker symbol (if applicable). |
| `country_code` | ISO country code. |
| `country` | Full country name. |
| `domain` | Company domain name. |
| `last_funding_round` | Most recent funding round (e.g., `Seed`, `Pre Seed` etc) |

**Sample Response**

```json theme={"system"}
{
    "status": "success",
    "data": [
        {
            "name": "Wokelo AI",
            "permalink": "wokelo-ai",
            "short_description": "Wokelo builds purpose-built AI agents for dealmaking and consulting, designed by domain-experts to power sourcing, diligence and strategy.",
            "founded_year": "2023",
            "ipo_status": "private",
            "hq": "Seattle, United States",
            "industries": "AI Investment Research Platform",
            "website": "https://www.wokelo.ai/",
            "ticker": "",
            "country_code": "US",
            "country": "United States",
            "domain": "wokelo.ai",
            "last_funding_round": "Seed"
        }
    ],
    "count": 10
}
```

```json 200 theme={"system"}
{
    "status": "success",
    "data": [
        {
            "name": "Wokelo AI",
            "permalink": "wokelo-ai",
            "short_description": "Wokelo builds purpose-built AI agents for dealmaking and consulting.",
            "founded_year": "2023",
            "ipo_status": "private",
            "hq": "Seattle, United States",
            "industries": "AI Investment Research Platform",
            "website": "https://www.wokelo.ai/",
            "ticker": "",
            "country_code": "US",
            "country": "United States",
            "domain": "wokelo.ai",
            "last_funding_round": "Seed"
        }
    ],
    "count": 10
}
```


## OpenAPI

````yaml GET /api/enterprise/company/search
openapi: 3.0.3
info:
  title: Wokelo API
  description: >
    Wokelo provides four categories of APIs for company and market intelligence:


    1. **Enrichment** – Company and Industry data using Wokelo database and
    alternative data. Supports multi-company requests.

    2. **Discovery** – Workflows for specific use-cases such as market map,
    target screening, and buyer screening.

    3. **Monitoring** – Real-time news monitoring for companies.

    4. **Workflow Automation** – Wokelo and custom research workflows executed
    within notebooks.


    Enrichment and Discovery APIs are managed through async requests; use the
    Supporting APIs to track status and export results in JSON.

    Workflow APIs are executed within notebooks and support export to PDF, PPT,
    DOC, or JSON.


    **Authentication:** All endpoints (except `/auth/token/`) require a Bearer
    JWT token in the `Authorization` header.
  version: 1.0.0
  contact:
    url: https://docs.wokelo.ai/contact
servers:
  - url: https://api.wokelo.ai
    description: Production server
security: []
tags:
  - name: Authentication
    description: Obtain JWT tokens for API access
  - name: Enrichment
    description: Retrieve structured data for companies and industries
  - name: Discovery
    description: Identify companies via market maps, buyer and target screening
  - name: Monitoring
    description: Real-time company news monitoring
  - name: Workflow Automation
    description: Research notebooks for companies, industries, and custom workflows
  - name: Supporting APIs
    description: >-
      Utility endpoints for search, file upload, request management, and report
      retrieval
externalDocs:
  description: Official Wokelo API Documentation
  url: https://docs.wokelo.ai/overview
paths:
  /api/enterprise/company/search:
    get:
      tags:
        - Supporting APIs
      summary: Company Search
      description: >-
        Search for companies using name, website, or ticker. Returns a list of
        companies with their permalink and other attributes.
      operationId: companySearch
      parameters:
        - name: query
          in: query
          required: true
          schema:
            type: string
          description: The search query string (e.g., company name, website or ticker).
          example: wokelo
        - name: search_by
          in: query
          required: false
          schema:
            type: string
            enum:
              - name
              - website
              - ticker
          description: 'Field to search by. Supported values: `name`, `website`, `ticker`.'
        - name: company_type
          in: query
          required: false
          schema:
            type: string
            enum:
              - private
              - public
              - all
            default: all
          description: Filter by company type. Use `all` to return all types (default).
      responses:
        '200':
          description: Search results returned successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: success
                  data:
                    type: array
                    description: List of matching company objects.
                    items:
                      type: object
                      properties:
                        name:
                          type: string
                          description: Company name.
                        permalink:
                          type: string
                          description: Unique identifier/slug for the company.
                        short_description:
                          type: string
                          description: Brief description of the company.
                        founded_year:
                          type: string
                          description: Year the company was founded.
                        ipo_status:
                          type: string
                          description: IPO status.
                          example: private
                        hq:
                          type: string
                          description: Headquarters location.
                        industries:
                          type: string
                          description: Industry or sector the company operates in.
                        website:
                          type: string
                          format: uri
                          description: Company website URL.
                        ticker:
                          type: string
                          description: Stock ticker symbol (if applicable).
                        country_code:
                          type: string
                          description: ISO country code.
                          example: US
                        country:
                          type: string
                          description: Full country name.
                        domain:
                          type: string
                          description: Company domain name.
                        last_funding_round:
                          type: string
                          description: Most recent funding round (e.g., Seed, Pre Seed).
                  count:
                    type: integer
                    description: Total number of results returned.
                    example: 10
              example:
                status: success
                data:
                  - name: Wokelo AI
                    permalink: wokelo-ai
                    short_description: >-
                      Wokelo builds purpose-built AI agents for dealmaking and
                      consulting.
                    founded_year: '2023'
                    ipo_status: private
                    hq: Seattle, United States
                    industries: AI Investment Research Platform
                    website: https://www.wokelo.ai/
                    ticker: ''
                    country_code: US
                    country: United States
                    domain: wokelo.ai
                    last_funding_round: Seed
                count: 10
        '401':
          description: Unauthorized – invalid or missing JWT token
      security:
        - bearerAuth: []
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from the `/auth/token/` endpoint.

````

This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.