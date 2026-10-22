> ## Documentation Index
> Fetch the complete documentation index at: https://docs.akta.pro/llms.txt
> Use this file to discover all available pages before exploring further.

# akta.pro API Overview

> Introduction to the akta.pro API platform, its data products, and how to start building.

[akta.pro](http://akta.pro) builds private company data and signals API for the agent economy

> **Pitchbook-quality data, pay as you go**

> **100+ event signals and triggers**

> **Built for AI and agent workflows**

## Get started

> **[Get your API key](https://playground.akta.pro/signup)**
>
> Generate an API key in the Playground and start querying live data.

> **[Connect via MCP or CLI](https://docs.akta.pro/docs/developer-tools/mcp/setup)**
>
> Sign-up and connect to your agent — Claude, ChatGPT, VS Code etc.

**1. Create an API key**

* After logging in, open API Keys from the left sidebar.
* Enter a name for your API key (for example: `Production API Key` )
* Then click 'Add API key'.

**2. Copy and store your API key**

* The API key is shown once. Copy it immediately and store it somewhere safe. If it's lost, a new one will need to be created.
* Your key will look similar to this: `wk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

> [!WARNING]
>
> Never share your API key publicly or commit it to source control.

**3. Make your first API request**

Try company search endpoint to start with. Make sure to replace YOUR\_API\_KEY with the actual API key in the code snippets below.

```text cURL theme={null}
curl -G "https://api.akta.pro/api/v1/company/search/?query=canva" \
  -H "x-api-key: YOUR_API_KEY"
```

```text Python theme={null}
import requests

url = "https://api.akta.pro/api/v1/company/search/"
headers = {"x-api-key": "YOUR_API_KEY"}
params = {"query": "canva"}

response = requests.get(url, headers=headers, params=params)
data = response.json()

for company in data["data"]:
    print(company["name"], company["website"])
    print(company["company_status"], company["product_category"])
    print()
```

Now you can start exploring other endpoints such as [Company Data](/api-reference/company-data) and [News Signals](/api-reference/news-signals)

## Data API Products

> **[Company Data](/docs/company-data/overview)**
>
> 75+ data points for 20M+ private and public companies globally

> **[Alternative Signals](/docs/alternative-data)**
>
> Social media, jobs, reviews, headcount trends, website traffic

> **[Supporting APIs](/docs/supporting-apis)**
>
> Company and industry search to resolve UUIDs and taxonomy codes

> **[News Signals](/docs/news-signals/overview)**
>
> Live and historical news; entity resolved, de-duped, 80+ event signals

> **[List Generation](/docs/list-generation/overview)**
>
> Build targeted company lists using structured filters or natural language


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.