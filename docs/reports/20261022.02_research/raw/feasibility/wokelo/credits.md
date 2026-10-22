> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Credits

## How credits are calculated

Credits are calculated at a granular level based on individual tasks (e.g., sections, parameters, and number of API calls). Consumption depends on multiple factors, including models used, data pipelines ingested, and processing required.

Wokelo’s APIs span real-time enrichment, monitoring, insights generation, and workflow automation. As a result, credit usage varies based on the type and depth of output requested and generated.

Full visibility into credit usage is available to enterprise administrators.\
\
*Note: Credits consumed for each API is returned in the API response in the "credits\_consumed" field.*

## Credit construct by API type

| **API** | **Type** | **Variable** | **Credit Range** |
| :- | :- | :- | :- |
| Market Map, Target Screening, Buyer Screening | Discovery | Number of companies returned, fields enriched | \$\$ |
| Company and Industry Research | Workflow | Sections selected | \$\$\$ |
| Peer Comparison | Workflow | Sections selected | \$\$ |
| Earnings Analysis | Workflow | Earnings selected | \$ |
| Custom Workflow | Workflow | Custom configuration | Custom |

## Guidelines and Notes

* Credits are not charged for any section where no data is returned
* Workflow-level credit usage may also vary based on inputs such as files uploaded, custom fields selected, and similar variables
* Credit constructs are subject to periodic updates as underlying models, data partnerships, and pricing evolve
* For pricing discussions or credit limit adjustments, please contact [**sales@wokelo.ai**](mailto:sales@wokelo.ai)


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.