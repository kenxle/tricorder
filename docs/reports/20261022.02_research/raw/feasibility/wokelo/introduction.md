> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Introduction

> Wokelo's API suite is purpose-built for developers building dealmaking AI infrastructure. It delivers structured, processed intelligence at the quality standard investment and advisory workflows demand. The underlying data is purpose-built for AI pipelines:

* Entities are resolved across a proprietary database of **20M+ private and public companies**.
* News signals are deduplicated across **1,000+ curated sources.**
* **Custom parameters and scoring logic** can be defined at query time.
* Every output is **agent-native, source-traced, and ready to plug** directly into your models, agents,  and workflows without additional processing.

## API Products

Wokelo’s API Suite consists of four types of APIs:

### **Discovery**

> **[Market Map](/market-map-doc)**
>
> Ranked, filtered company lists with custom parameters.

> **[Target Screening](/target-screening-doc)**
>
> Scored acquisition targets with custom filtering logic.

> **[Buyer Screening](/buyer-screening-doc)**
>
> Scored strategic and financial buyers with custom logic.

> **[Competitor List](/competitor-list-doc)**
>
> Find competitors of a given company.

> **[M\&A Activity](/acquisitions-doc)**
>
> Obtain in-depth acquisition activities of a given company.

> **[Fundraising Activity](/fundraise-doc)**
>
> Obtain funding activity, investor landscape, and funding stage analysis.

### **Workflow Automation**

> **[Company Research](/company-research-doc)**
>
> Trigger Wokelo's company research workflows and return in any format.

> **[Industry Research](/industry-research-doc)**
>
> Trigger Wokelo's industry research workflows, return in any format.

> **[Peer Comparison](/peer-comparison-doc)**
>
> Trigger Wokelo's peer comparison workflows and return in any format.

> **[Custom Workflow](/custom-workflow-automation-doc)**
>
> Trigger custom research workflows and return in any format.

Discovery APIs are request-based. Each request returns a request\_id which can be used to track status and retrieve results in JSON when complete. Workflow Automation APIs are executed within notebooks and outputs can be exported as PDF, PPT, DOC, or JSON.

## API structure

Wokelo’s API follows two primary patterns depending on the complexity of the operation:

**Synchronous APIs (instant response)**

* Company Search — Returns matching companies immediately in the HTTP response

**Asynchronous APIs (submit request, poll for status, retrieve results)**

* All the Discovery APIs return a request\_id
* All Workflow Automation APIs return a report\_id
* Poll for status, then retrieve results when complete. For request\_id, use Request result API to view the results. For report\_id, use Download Report API to download the report.

Eg. Company Research API will return a report\_id as a response. One has to use Download Report API to view the report output.

```json theme={"system"}
{
    "report_id": 123345
}
```

## Estimated Time

| **API** | **Approximate Time** |
| :- | :- |
| Market Map | 10-15 mins |
| Target Screening | 10-15 mins |
| Buyer Screening | 10-15 mins |
| Competitor List | 10-15 mins |
| M\&A Activity | 10-15 mins |
| Fundraising Activity | 10-15 mins |
| Company Research | 20-25 mins |
| Industry Research | 20-25 mins |
| Peer Comparison | 15-20 mins |
| Custom Workflow | Custom |


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.