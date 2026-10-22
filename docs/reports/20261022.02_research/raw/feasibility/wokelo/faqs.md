> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# FAQs

## Access & Setup

> **How do I activate my Wokelo account?**
>
> Your account is provisioned by your organization admin or the Wokelo team. Once activated, you’ll receive login credentials via email, which can be used to access the platform and generate API tokens.

> **Where can I find my API credentials?**
>
> API credentials (`client_id`, `client_secret`) are available on the **API Credentials** page within the Wokelo platform. These are organization-level credentials and should be securely stored on your backend.

> **Can I request a separate API account for my organization?**
>
> Yes. Wokelo supports organization-level account provisioning, including separate API credentials for different teams or environments (e.g., staging vs production). Reach out to your account team to configure this.

## Usage, Credits & Performance

> **How can I track my remaining API credits?**
>
> Credit usage and remaining balance are available to enterprise admins within the platform. Credits are consumed based on API type, parameters selected, and output complexity.

> **How long does it take to generate an output?**
>
> Latency varies by API type:
>
> * **Real-time / lightweight APIs (e.g., Monitoring):** seconds
> * **Enrichment / Insights APIs:** typically seconds to a few minutes
> * **Workflow / deep analysis outputs:** can take around 20-25 minutes depending on sections selected
>
> All long-running requests return a `request_id` or report ID for asynchronous tracking

> **How should I handle latency in production?**
>
> Many Wokelo APIs are asynchronous and return a `request_id`, especially for deeper analysis and workflow-based outputs. Instead of blocking on a response, you should design your integration to:
>
> * Submit the request and persist the `request_id`
> * Track progress via status endpoints or webhooks
> * Fetch results once processing is complete
>
> Wokelo supports **webhooks** to notify your system when a request is completed, eliminating the need for constant polling. This is recommended for production use cases where you want to trigger downstream workflows (e.g., storing results, notifying users, or chaining analyses) as soon as outputs are ready.

> **Can I process requests in bulk?**
>
> Yes. Several APIs support **multi-entity inputs** (e.g., multiple companies in a single request). For large-scale usage, batching requests and handling them asynchronously is recommended. Our Company Enrichment Instant APIs are mostly used for batch processing and enrichment.

## Data & Coverage

> **How recent is the data provided by Wokelo?**
>
> Wokelo integrates real-time pipelines and continuously refreshed datasets. Most data elements (except company enrichment) are always pulled live. Certain other data elements (\<10%) we partner with providers we have a daily or weekly refresh cycle.

> **What should I do if I can’t find a company in search?**
>
> If a company is not found: All endpoints except company enrichment instant and monitoring support an on-demand addition of companies not available in our ever-growing database. For such cases based on website URL our agents will extract structured information and proceed with analysis asked
>
> If you face any issues, you can reach out to Wokelo support.

## Product & API Design

> **How are Wokelo APIs different from standard LLM APIs?**
>
> Wokelo APIs are **workflow-oriented, domain-specific, and powered by a large-scale proprietary + public company dataset (20M+ entities)**—not just generic prompt-response interfaces.
>
> Key differences:
>
> * **Data + reasoning combined**: Built on top of structured, continuously updated company and industry data—not just model priors
> * **Pre-built workflows**: Native support for investment use cases like market mapping, screening, diligence, and research—no need to design prompts or orchestration from scratch
> * **Deterministic inputs, structured outputs**: Use filters, parameters, and defined sections instead of free-form prompting; outputs are consistent and machine-readable
> * **Multi-step intelligence layer**: Combines enrichment, synthesis, and reasoning into a single API call rather than requiring multiple LLM interactions
> * **Production-ready by design**: Handles scale, async execution, and repeatability for enterprise workflows
>
> Wokelo combines **large-scale structured data with best-in-class agents** to deliver an industry-leading API platform—trusted by marquee financial institutions and enterprises for high-stakes decision-making.

> **I have a specific API or workflow requirement—how can I proceed?**
>
> Wokelo supports both **out-of-the-box APIs** and **custom workflows** tailored to your use case.
>
> You can:
>
> * Use existing APIs with configurable parameters and custom fields
> * Use custom workflows using the **Custom Workflow API** or notebooks
> * Request tailored endpoints, data integrations, or workflow configurations via your account team
>
> For more complex requirements (e.g., proprietary scoring models, custom datasets, or multi-step pipelines), the Wokelo team can help design and deploy **bespoke solutions aligned to your internal workflows**.

> **How are Wokelo APIs different from standard LLM APIs?**
>
> Wokelo APIs are **workflow-oriented, domain-specific, and powered by a large-scale proprietary + public company dataset (20M+ entities)**—not just generic prompt-response interfaces.
>
> Key differences:
>
> * **Data + reasoning combined**: Built on top of structured, continuously updated company and industry data—not just model priors
> * **Pre-built workflows**: Native support for investment use cases like market mapping, screening, diligence, and research—no need to design prompts or orchestration from scratch
> * **Deterministic inputs, structured outputs**: Use filters, parameters, and defined sections instead of free-form prompting; outputs are consistent and machine-readable
> * **Multi-step intelligence layer**: Combines enrichment, synthesis, and reasoning into a single API call rather than requiring multiple LLM interactions
> * **Production-ready by design**: Handles scale, async execution, and repeatability for enterprise workflows
>
> Wokelo combines **large-scale structured data with best-in-class agents** to deliver an industry-leading API platform—trusted by marquee financial institutions and enterprises for high-stakes decision-making.

> **I have a specific API or workflow requirement—how can I proceed?**
>
> Wokelo supports both **out-of-the-box APIs** and **custom workflows** tailored to your use case.
>
> You can:
>
> * Use existing APIs with configurable parameters and custom fields
> * Build custom workflows using the **Custom Workflow API** or notebooks
> * Request tailored endpoints, data integrations, or workflow configurations via your account team
>
> For more complex requirements (e.g., proprietary scoring models, custom datasets, or multi-step pipelines), the Wokelo team can help design and deploy **bespoke solutions aligned to your internal workflows**.

## Security

> **Where is my data stored?**
>
> Wokelo runs on secure cloud infrastructure with enterprise-grade controls, including encryption at rest and in transit, access isolation, and audit mechanisms.

> **Will Wokelo use my data to train its models?**
>
> No. Customer data is not used to train Wokelo’s internal models.
>
> If external AI providers are used, they are contractually restricted from retaining or training on customer data.

> **What admin controls are available and how can I access them?**
>
> Enterprise admins have access to:
>
> * API credential management
> * Usage and credit tracking
> * User access controls
> * Workflow and report visibility
>
> These controls are available within the Wokelo platform’s admin interface. Access is granted based on role permissions.

## Deployment

> **Do you offer VPC or private deployment options?**
>
> Yes. Wokelo supports enterprise deployments including VPC and private environment setups. Configuration depends on security and compliance requirements—contact your account team for details.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.