> For clean Markdown of any page, append `.md` to the page URL.
> Documentation index: https://you.com/docs/llms.txt (section indexes: append `/llms.txt` to any section URL).
> Search these docs: Docs MCP at https://you.com/docs/_mcp/server (`searchDocs`, no API key).
> Call live You.com APIs: Product MCP at https://api.you.com/mcp (keyless `?profile=free` exposes `you-search` and `you-discover`. Research and finance use `/mcp/research`, `/mcp/finance`, or `?tools=` on `/mcp`). To pick an API or integration path, call `you-discover` on that server instead of guessing.
> OpenAPI: https://you.com/docs/openapi.json—auth header `X-API-Key`, env `YDC_API_KEY`.

# Quickstart

You.com gives you real-time web intelligence through five APIs: Web Search, Answer, Contents, Research, and Finance Research. Two ways to get started—write code, or connect your agent.

#### [Make API Calls](#get-your-api-key)

Get an API key and run your first request in minutes. Try each API in the flow below.

#### [Give Your Agent Access](#give-your-agent-access)

Connect your IDE or agent to You.com with no code—Docs MCP server, You.com MCP server, or Agent Skills.

## Give Your Agent Access

Four ways to give your agent access, from zero setup to installed skills. [Build With Agents](/docs/agents) compares them and maps each job to an API.

#### Read the docs

Append `.md` to any page URL to get that page as Markdown, such as `you.com/docs/quickstart.md`. `you.com/docs/llms.txt` indexes the full site, and each section has its own index, such as `you.com/docs/api-reference/llms.txt`.

#### Docs MCP

Add the [Docs MCP server](/docs/agents/docs-mcp-server) to any MCP client. No API key is needed, and your agent gets a `searchDocs` tool that returns passages with source URLs.

```json
{
  "mcpServers": {
    "fern_mcp_you-com-docs": {
      "url": "https://you.com/docs/_mcp/server"
    }
  }
}
```

#### You.com MCP

Add the [You.com MCP server](/docs/agents/mcp-server) with your API key. Without a key, use `https://api.you.com/mcp?profile=free`, which allows `you-search` and `you-discover` for 100 queries per day. [Scope Tools](/docs/agents/mcp-server#scope-tools) covers how to enable `you-research` and `you-finance`.

```json
{
  "mcpServers": {
    "ydc-server": {
      "type": "http",
      "url": "https://api.you.com/mcp",
      "headers": {
        "Authorization": "Bearer <YDC_API_KEY>"
      }
    }
  }
}
```

#### Agent Skills

[Agent Skills](/docs/agents/skills) are instruction packs that tell your agent which tool or API to use for web search, URL content extraction, cited research, finance research, and integration discovery. This command installs all of them, and the Agent Skills page lists each one and the platform plugins.

```bash
npx skills add youdotcom-oss/agent-skills
```

---

The five APIs:

* **[Web Search API](/docs/guides/search/quickstart)**—real-time web and news results as LLM-ready JSON
* **[Answer API](/docs/guides/answer/quickstart)**—a cited, synthesized answer from a single query
* **[Contents API](/docs/guides/contents/quickstart)**—clean Markdown or HTML from URLs you specify
* **[Research API](/docs/guides/research/quickstart)**—multi-step, cited answers to complex questions
* **[Finance Research API](/docs/guides/finance-research/quickstart)**—cited answers from a finance-optimized index

[Choose the Right API](/docs/choose-the-right-api) compares job fit, latency, and price for all five.

---

## Get Your API Key

Sign in or create an account, then get an API key here: [https://you.com/platform](https://you.com/platform).

> **Info**
>
> The code samples below read your key from an environment variable named `YDC_API_KEY`—the canonical variable name across our docs, SDKs, and integrations. Set it once (`export YDC_API_KEY="your-key"`) and the examples will pick it up. See [API key management](/docs/administration/api-keys) for best practices.

Each API has its own endpoint. Every request sends your API key in the `X-API-Key` header.

| API                  | Endpoint                                           | Guide                                     | API reference                                                                    |
| -------------------- | -------------------------------------------------- | ----------------------------------------- | -------------------------------------------------------------------------------- |
| Web Search API       | `POST https://ydc-index.io/v1/search` (also `GET`) | [Overview](/docs/guides/search)           | [/v1/search](/docs/api-reference/search/v1-search)                               |
| Contents API         | `POST https://ydc-index.io/v1/contents`            | [Overview](/docs/guides/contents)         | [/v1/contents](/docs/api-reference/contents)                                     |
| Answer API           | `POST https://api.you.com/v1/answer`               | [Overview](/docs/guides/answer)           | [/v1/answer](/docs/api-reference/answer/v1-answer)                               |
| Research API         | `POST https://api.you.com/v1/research`             | [Overview](/docs/guides/research)         | [/v1/research](/docs/api-reference/research/v1-research)                         |
| Finance Research API | `POST https://api.you.com/v1/finance_research`     | [Overview](/docs/guides/finance-research) | [/v1/finance_research](/docs/api-reference/finance-research/v1-finance_research) |

The Answer, Research, and Finance Research APIs run only on `api.you.com`. Sending one of those paths to `ydc-index.io` returns `403` with `{"message": "Missing Authentication Token"}`, even when the key is valid.

## Try the Web Search API

The Web Search API returns real-time web and news results as structured, LLM-ready JSON. Feed the results directly into your prompt to ground your AI in fresh information.

```python
from youdotcom import You

with You() as you:
    results = you.search(query="global birth rate trends", count=5)

    for result in results.results.web:
        print(result.title)
        print(result.url)
        highlights = result.contents.highlights if result.contents else None
        if highlights:
            print(highlights[0])
```

```typescript
const response = await fetch("https://ydc-index.io/v1/search", {
  method: "POST",
  headers: {
    "X-API-Key": process.env.YDC_API_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    query: "global birth rate trends",
    count: 5,
  }),
});

if (!response.ok) {
  throw new Error(`HTTP error: ${response.status}`);
}

const result = await response.json();

result.results?.web?.forEach((r) => {
  console.log(r.title, r.url);
  console.log(r.snippets?.[0]);
});
```

```curl
curl -X POST https://ydc-index.io/v1/search \
  -H "X-API-Key: $YDC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "global birth rate trends",
    "count": 5
  }'
```

The Python sample follows the SDK default and prints `contents.highlights`. The TypeScript and curl calls omit `extraction`, so raw `POST /v1/search` returns `snippets`. `you.search()` in the Python SDK 3.6.0 and later sends `knowledge="core"` and `extraction={"extraction_mode": "highlights"}` when you pass neither argument, and `snippets` is `None`. Knowledge adds no extra charge. See [Billing](/docs/administration/billing).

Pass both arguments as `None` for snippets:

```python
results = you.search(
    query="global birth rate trends",
    count=5,
    knowledge=None,
    extraction=None,
)
```

Highlights accepts `count` up to 50. The SDK default uses highlights, so a `count` above 50 needs `extraction=None` or `extraction_mode` set to `full_page`.

A raw `POST /v1/search` call returns JSON like this:

```json maxLines=20
{
  "results": {
    "web": [
      {
        "url": "https://www.worldbank.org/en/topic/population",
        "title": "Population | World Bank",
        "description": "The World Bank tracks global birth rate and population trends.",
        "snippets": [
          "Global fertility rates have declined significantly over the past five decades, falling from an average of 5 births per woman in 1960 to around 2.3 today."
        ],
        "page_age": "2025-10-01T00:00:00",
        "favicon_url": "https://ydc-index.io/favicon?domain=worldbank.org&size=128"
      }
    ]
  },
  "metadata": {
    "query": "global birth rate trends",
    "search_uuid": "a1b2c3d4-0000-0000-0000-000000000000",
    "latency": 0.38
  }
}
```

> **TypeScript, MCP, or the Python SDK**
>
> TypeScript and JavaScript have three paths. Use `fetch` against the REST APIs when the application needs the JSON. Use [`@youdotcom-oss/mcp`](https://www.npmjs.com/package/@youdotcom-oss/mcp), or the hosted server at `https://api.you.com/mcp`, when an agent should call the tools. Use the [Python SDK](/docs/integrations/python-sdk) when you want a typed client that tracks new API fields. The `@youdotcom-oss/sdk` package is deprecated.

### Ground a Model with Highlights

Snippets are the HTTP default. Raw `POST /v1/search` returns them when the body omits `extraction`. The Python SDK 3.6.0 and later defaults to highlights and `knowledge="core"`, so `you.search()` returns `contents.highlights` and `snippets` is `None`. Pass `knowledge=None` and `extraction=None` for snippets. The sample sets `extraction_mode` to `highlights`, which is what an HTTP client sends for the same excerpts.

```python
from youdotcom import You
from youdotcom.models import Extraction, ExtractionMode

with You() as you:
    results = you.search(
        query="global birth rate trends",
        count=5,
        extraction=Extraction(
            extraction_mode=ExtractionMode.HIGHLIGHTS,
        ),
    )

    if results.results and results.results.web:
        for result in results.results.web:
            if result.contents and result.contents.highlights:
                print(result.title)
                print(result.contents.highlights[0])
```

```typescript
const response = await fetch("https://ydc-index.io/v1/search", {
  method: "POST",
  headers: {
    "X-API-Key": process.env.YDC_API_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    query: "global birth rate trends",
    count: 5,
    extraction: {
      extraction_mode: "highlights",
    },
  }),
});

const result = await response.json();

result.results?.web?.forEach((r) => {
  if (r.contents?.highlights?.length) {
    console.log(r.title);
    console.log(r.contents.highlights[0]);
  }
});
```

```curl
curl -X POST https://ydc-index.io/v1/search \
  -H "X-API-Key: $YDC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "global birth rate trends",
    "count": 5,
    "extraction": {
      "extraction_mode": "highlights"
    }
  }'
```

See [Retrieve page content](/docs/guides/search/retrieve-page-content) for the token budget, `knowledge: "core"` for live licensed data, and pricing.

### Improve Accuracy with Full Page Extraction

Search results already include query-relevant text extracts from target pages. Use the `extraction` parameter with `extraction_mode: "full_page"` to fetch full page content for each result as clean Markdown or HTML.

This will naturally increase latency, but massively improves knowledge accuracy.

> **Warning**
>
> Full page extraction is billed at \$1.00 per 1,000 pages fetched live on top of the base Web Search API rate—the same price as the Contents API. With the default `count=10`, a call using `extraction_mode: "full_page"` crawls up to 20 pages and adds up to \$0.02 to the \$0.005 base cost. Pages served from cache are free. See [Billing](/docs/administration/billing) for how `extraction_source` changes the charge.

```python
from youdotcom import You
from youdotcom.models import Extraction, ExtractionFormat, ExtractionMode

with You() as you:
    results = you.search(
        query="global birth rate trends",
        count=5,
        extraction=Extraction(
            extraction_mode=ExtractionMode.FULL_PAGE,
            full_page={"extraction_formats": [ExtractionFormat.MARKDOWN]},
        ),
    )

    for result in results.results.web:
        if result.contents and result.contents.markdown:
            print(result.title)
            print(result.contents.markdown[:400])
```

```typescript
const response = await fetch("https://ydc-index.io/v1/search", {
  method: "POST",
  headers: {
    "X-API-Key": process.env.YDC_API_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    query: "global birth rate trends",
    count: 5,
    extraction: {
      extraction_mode: "full_page",
      full_page: {
        extraction_formats: ["markdown"],
      },
    },
  }),
});

if (!response.ok) {
  throw new Error(`HTTP error: ${response.status}`);
}

const result = await response.json();

result.results?.web?.forEach((r) => {
  if (r.contents?.markdown) {
    console.log(r.title);
    console.log(r.contents.markdown.slice(0, 400));
  }
});
```

```curl
curl -X POST https://ydc-index.io/v1/search \
  -H "X-API-Key: $YDC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "global birth rate trends",
    "count": 5,
    "extraction": {
      "extraction_mode": "full_page",
      "full_page": {
        "extraction_formats": ["markdown"]
      }
    }
  }'
```

Results that support extraction will include a `contents.markdown` field with the full page. For RAG pipelines that need deep context rather than highlights excerpts, this is the parameter to reach for.

[Web Search API Quickstart](/docs/guides/search/quickstart) · [Overview](/docs/guides/search)

## Try the Answer API

The Web Search API gives you the raw results. The Answer API does the next step—it retrieves web results, verifies every citation against the source text, and returns a Markdown answer with inline citations in one call. The fastest path from a question to a grounded answer, with no orchestration on your end.

```python
from youdotcom import You

with You() as you:
    response = you.answer(
        query="What are the main drivers of the global decline in birth rates?",
    )

    print(response.answer)

    print(f"\n--- {len(response.citations or [])} citations ---")
    for i, citation in enumerate(response.citations or [], 1):
        print(f"[{i}] {citation.source}")
```

```typescript
const response = await fetch("https://api.you.com/v1/answer", {
  method: "POST",
  headers: {
    "X-API-Key": process.env.YDC_API_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    query: "What are the main drivers of the global decline in birth rates?",
  }),
});

if (!response.ok) {
  throw new Error(`HTTP error: ${response.status}`);
}

const data = await response.json();

console.log(data.answer);

console.log(`\n--- ${data.citations.length} citations ---`);
data.citations.forEach((citation, i) => {
  console.log(`[${i + 1}] ${citation.source}`);
});
```

```curl
curl -X POST https://api.you.com/v1/answer \
  -H "X-API-Key: $YDC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main drivers of the global decline in birth rates?"
  }'
```

The response includes a Markdown answer with numbered inline citations, the sources cited, and the web results considered during synthesis:

```json maxLines=20
{
  "answer": "Global fertility rates have declined over the past five decades due to a combination of increased access to contraception, rising female education and labor force participation, higher costs of raising children, and urbanization. [[1, 2, 3]]",
  "citations": [
    {
      "source": "https://www.worldbank.org/en/topic/population",
      "excerpts": [
        "Global fertility rates have declined significantly over the past five decades, falling from an average of 5 births per woman in 1960 to around 2.3 today."
      ]
    }
  ],
  "results": {
    "web": [
      {
        "url": "https://www.worldbank.org/en/topic/population",
        "title": "Population | World Bank",
        "snippets": ["Global fertility rates have declined significantly over the past five decades..."]
      }
    ]
  }
}
```

Every citation is verified against the source text before the answer is returned—the `excerpts` are the verbatim passages the model used, so you can confirm accuracy without trusting the model alone. Use `freshness`, `country`, `language`, `include_domains`, `exclude_domains`, and `boost_domains` to steer results, same as the Web Search API.

[Answer API Quickstart](/docs/guides/answer/quickstart) · [Overview](/docs/guides/answer)

## Try the Contents API

The Contents API fetches content from URLs you specify as clean Markdown or HTML—no browser automation, no HTML parsing. One use: pass your competitors' pricing page URLs to a daily job and feed the Markdown to an LLM to monitor what changed.

```python
from youdotcom import You
from youdotcom.models import ContentsFormats

with You() as you:
    pages = you.contents(
        urls=[
            "https://competitor-a.com/pricing",
            "https://competitor-b.com/pricing",
        ],
        formats=[ContentsFormats.MARKDOWN],
    )

    for page in pages:
        print(f"=== {page.title} ===")
        print(page.markdown)
```

```typescript
const response = await fetch("https://ydc-index.io/v1/contents", {
  method: "POST",
  headers: {
    "X-API-Key": process.env.YDC_API_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    urls: [
      "https://competitor-a.com/pricing",
      "https://competitor-b.com/pricing",
    ],
    formats: ["markdown"],
  }),
});

if (!response.ok) {
  throw new Error(`HTTP error: ${response.status}`);
}

const pages = await response.json();

for (const page of pages) {
  console.log(`=== ${page.title} ===`);
  console.log(page.markdown?.slice(0, 500));
}
```

```curl
curl -X POST https://ydc-index.io/v1/contents \
  -H "X-API-Key: $YDC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://competitor-a.com/pricing", "https://competitor-b.com/pricing"],
    "formats": ["markdown"]
  }'
```

Each URL comes back as a structured object:

```json maxLines=20
[
  {
    "url": "https://competitor-a.com/pricing",
    "title": "Pricing — Competitor A",
    "markdown": "# Pricing\n\n## Starter\n$49/month...",
    "metadata": {
      "site_name": "Competitor A",
      "favicon_url": "https://ydc-index.io/favicon?domain=competitor-a.com&size=128"
    }
  }
]
```

[Contents API Quickstart](/docs/guides/contents/quickstart) · [Overview](/docs/guides/contents)

## Try the Research API

The Research API goes beyond a single web search. Give it a complex question and it runs multiple searches, reads through the sources, and synthesizes a thorough, citation-backed answer—so you don't have to. Control the depth with `research_effort` from `lite` to `frontier`.

```python
from youdotcom import You
from youdotcom.models import ResearchEffort

you = You()

res = you.research(
    input="What are the tradeoffs between microservices and monolithic architectures for high-traffic applications?",
    research_effort=ResearchEffort.STANDARD,
)

print(res.output.content[:500])
print(f"\nSources: {len(res.output.sources)}")
for source in res.output.sources:
    print(f"  - {source.title or 'Untitled'}: {source.url}")
```

```typescript
const response = await fetch("https://api.you.com/v1/research", {
  method: "POST",
  headers: {
    "X-API-Key": process.env.YDC_API_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    input: "What are the tradeoffs between microservices and monolithic architectures for high-traffic applications?",
    research_effort: "standard",
  }),
});

if (!response.ok) {
  throw new Error(`HTTP error: ${response.status}`);
}

const result = await response.json();

console.log(result.output.content.slice(0, 500));
console.log(`\nSources: ${result.output.sources.length}`);
result.output.sources.forEach((s) => {
  console.log(`  - ${s.title ?? s.url}: ${s.url}`);
});
```

```curl
curl -X POST https://api.you.com/v1/research \
  -H "X-API-Key: $YDC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What are the tradeoffs between microservices and monolithic architectures for high-traffic applications?",
    "research_effort": "standard"
  }'
```

The response includes a Markdown-formatted answer with inline citations and the list of sources used:

```json maxLines=20
{
  "output": {
    "content": "## Microservices vs Monolithic Architectures\n\nThe choice between microservices and monolithic architectures involves several key tradeoffs...\n\n### Scalability\nMicroservices allow independent scaling of individual components [[1, 3]]...",
    "content_type": "text",
    "sources": [
      {
        "url": "https://example.com/architecture-patterns",
        "title": "Architecture Patterns for High-Traffic Systems",
        "snippets": [
          "Microservices enable teams to scale individual services independently, reducing infrastructure costs for components with uneven load."
        ]
      }
    ]
  }
}
```

Use `research_effort` to control how deep the API digs—`lite` for quick answers, `standard` for a good balance, `deep` or `exhaustive` when thoroughness matters more than speed, or `frontier` for long-running deep research that requires [background requests](/docs/guides/research/background-requests). The Research API also supports [source control](/docs/guides/research/source-control) and [structured output](/docs/guides/research/structured-output) for domain filtering and structured JSON output.

[Research API Quickstart](/docs/guides/research/quickstart) · [Overview](/docs/guides/research)

## Try the Finance Research API

The Finance Research API works just like the Research API—same request shape, same response shape—but it searches a finance-optimized index instead of the open web: SEC filings, equity prices, fundamentals, macro indicators, and financial news. Use it for earnings analysis, due diligence, and market research.

It accepts two parameters: `input` (your financial question) and `research_effort` (`deep` or `exhaustive`).

```python
from youdotcom import You
from youdotcom.models import FinanceResearchEffort

with You() as you:
    res = you.finance_research(
        input="What were the key drivers of NVIDIA's revenue growth in fiscal year 2025?",
        research_effort=FinanceResearchEffort.DEEP,
    )

    print(res.output.content[:500])
    print(f"\nSources: {len(res.output.sources)}")
    for source in res.output.sources:
        print(f"  - {source.title or 'Untitled'}: {source.url}")
```

```typescript
const response = await fetch("https://api.you.com/v1/finance_research", {
  method: "POST",
  headers: {
    "X-API-Key": process.env.YDC_API_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    input: "What were the key drivers of NVIDIA's revenue growth in fiscal year 2025?",
    research_effort: "deep",
  }),
});

if (!response.ok) {
  throw new Error(`HTTP error: ${response.status}`);
}

const data = await response.json();

console.log(data.output.content.slice(0, 500));
console.log(`\nSources: ${data.output.sources.length}`);
(data.output.sources as { title?: string; url: string }[]).forEach((s) => {
  console.log(`  - ${s.title ?? "Untitled"}: ${s.url}`);
});
```

```curl
curl -X POST https://api.you.com/v1/finance_research \
  -H "X-API-Key: $YDC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What were the key drivers of NVIDIA'\''s revenue growth in fiscal year 2025?",
    "research_effort": "deep"
  }'
```

The response is the same shape as the Research API—a Markdown answer with inline citations and a list of sources, but every source comes from the financial index:

```json maxLines=20
{
  "output": {
    "content": "For fiscal year 2025, NVIDIA's revenue rose to **$130.5 billion, up 114% year over year**.[[1]] The main driver was Data Center demand...",
    "content_type": "text",
    "sources": [
      {
        "url": "https://investor.nvidia.com/financial-info/financial-reports/default.aspx",
        "title": "NVIDIA Corporation - Financial Reports"
      }
    ]
  }
}
```

The Finance Research API does not support `source_control`. If you need domain filtering, use the [Research API](/docs/guides/research). For structured JSON output, add an [`output_schema`](/docs/guides/finance-research/structured-output).

[Finance Research API Quickstart](/docs/guides/finance-research/quickstart) · [Overview](/docs/guides/finance-research)

---

## More Ways to Explore

### Explore the APIs Interactively

* [Web Search API playground](/docs/api-reference/search/v1-search?explorer=true)
* [Answer API playground](/docs/api-reference/answer/v1-answer?explorer=true)
* [Contents API playground](/docs/api-reference/contents?explorer=true)
* [Research API playground](/docs/api-reference/research/v1-research?explorer=true)
* [Finance Research API playground](/docs/api-reference/finance-research/v1-finance_research?explorer=true)

### Use the Python SDK

> **TypeScript, MCP, or the Python SDK**
>
> TypeScript and JavaScript have three paths. Use `fetch` against the REST APIs when the application needs the JSON. Use [`@youdotcom-oss/mcp`](https://www.npmjs.com/package/@youdotcom-oss/mcp), or the hosted server at `https://api.you.com/mcp`, when an agent should call the tools. Use the [Python SDK](/docs/integrations/python-sdk) when you want a typed client that tracks new API fields. The `@youdotcom-oss/sdk` package is deprecated.

### Fork a Sample App

The [Examples gallery](/docs/examples) has runnable apps built on each API, from a simple search page to research and finance research agents. Each comes with a live demo and an open-source GitHub repo.

### Try in Postman

Fork one of our pre-built collections, add your API key to the `production` environment, and send your first request without writing code.

#### [Web Search API](https://www.postman.com/youdotcom/you-com-api-workspace/collection/46015159-83118dc1-7279-49f6-893d-4c18b8163008)

#### [Research API](https://www.postman.com/youdotcom/you-com-api-workspace/collection/46015159-b2f6290f-99e7-46e0-9a73-1e5fcd0e81a3)

#### [Contents API](https://www.postman.com/youdotcom/you-com-api-workspace/collection/46015159-037d5564-c4b5-4e11-9cea-1e41a5eba4aa)

#### [Finance Research API](https://www.postman.com/youdotcom/you-com-api-workspace/collection/46015159-08727c0f-48d4-4a47-bf44-1841fbe13b03)

---

## Evaluate You.com

You.com provides an [open-source evaluation framework](https://github.com/youdotcom-oss/web-search-api-evals) and a reproducible methodology for [benchmarking search APIs](https://you.com/resources/the-you-dot-com-web-search-eval-harness)—so you can measure what actually matters: accuracy, latency, and information retrieval quality.

We're the only search API provider with peer-reviewed evaluation research. Our methodology was presented at the Association for the Advancement of Artificial Intelligence (AAAI) 2026 conference and received the Best Paper Award. Read the research:

1. [Stochasticity in Agentic Evaluations: Quantifying Inconsistency with Intraclass Correlation](https://arxiv.org/abs/2512.06710)
2. [Randomness in AI Benchmarks: What Makes an Eval Trustworthy?](https://you.com/resources/randomness-in-ai-benchmarks)

When starting your own evaluation, keep it simple: run `count=10` on a representative query set, then layer in full page extraction if highlights aren't providing enough context. The Python SDK 3.6.0 and later already requests highlights on that call.

* [How to Evaluate the Web Search API](/docs/guides/search/evaluate-us)—methodology, dataset recommendations (SimpleQA, FRAMES, FreshQA), latency benchmarking, and a production checklist
* [Agentic Web Search Playoffs](https://github.com/youdotcom-oss/agentic-web-search-playoffs)—open-source benchmark comparing web search providers in agentic workflows

Our team can also design and run custom benchmarks tailored to your domain and quality bar. [Talk to us](https://you.com/book-a-demo)

---

## Pricing

You.com uses pay-as-you-go pricing based on the API and usage. See the [Billing page](/docs/administration/billing) for complete pricing across all APIs.

| API                                                   | Use it for                                                            | Returns                                                                        | Latency                                                                  | Price                                                                                          |
| ----------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| [Web Search API](/docs/guides/search)                 | Ranked web and news results for your own model, RAG pipeline, or UI   | JSON results. Snippets by default, or highlights or full page via `extraction` | Retrieval only, no synthesis step, so it returns ahead of the Answer API | \$5.00 / 1k calls, up to 100 results per call. Full page add-on \$1.00 / 1k pages fetched live |
| [Contents API](/docs/guides/contents)                 | Page text from URLs you already have                                  | Markdown, HTML, metadata, or any combination                                   | Up to `crawl_timeout` per URL (default 10s). Cached pages return sooner  | \$1.00 / 1k pages                                                                              |
| [Answer API](/docs/guides/answer)                     | A cited answer from one search pass                                   | Markdown answer, citations with verbatim excerpts, and web results             | p50 2.67s                                                                | \$5.00 / 1k calls                                                                              |
| [Research API](/docs/guides/research)                 | Multi-step cited answers with depth control                           | Markdown or structured JSON, plus sources                                      | \< 10s (`lite`) through background-only (`frontier`)                     | \$12 / 1k (`lite`) through \$1,200 / 1k (`frontier`)                                           |
| [Finance Research API](/docs/guides/finance-research) | Cited answers about filings, prices, fundamentals, and financial news | Markdown answer plus sources                                                   | \< 120s (`deep`) or \< 300s (`exhaustive`)                               | \$110 / 1k (`deep`) or \$500 / 1k (`exhaustive`)                                               |

Track your usage and spending from the [analytics dashboard](https://you.com/platform/analytics). For volume discounts, annual pricing, and enterprise features, visit [you.com/pricing](https://you.com/pricing) or contact [api@you.com](mailto:api@you.com).