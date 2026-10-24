# Traction and revenue: expert knowledge

This file gives the model an investor's qualitative lens. Scripts remain the source of computed figures and thresholds. Do not turn the qualitative guidance here into universal numeric benchmarks.

## First-pass company lens

Before interpreting a metric, establish:

- What the company is building.
- How the business is doing.
- What the company is raising and what it will use the money for.
- The founders' backgrounds and why they may be able to make this company successful.
- How the relevant vertical is doing overall.

The KPI dashboard speaks most directly to business performance. Use the deck, founder bios, use-of-funds plan, and market materials for the other questions; do not infer them from the dashboard alone.

## Choose traction evidence by business model

### Games

- For a shipped game, examine games shipped and sales.
- For a new game concept, examine social traction around the title, including trailer impressions, media publicity, and Steam wishlists; also examine the sales forecast.
- Treat wishlists and community size as real signals to investigate, not as proof of future sales. Their meaning depends on game quality, target audience size, and competition. Forecasting game success is especially uncertain.
- Ask whether the team can deliver what it has promised and why the reported numbers are unusually strong.

### B2B

- Examine customer traction among the intended target clients, POCs, evidence of willingness to pay, paid customers, and the pricing and revenue model.
- A POC without a clear conclusion is weak evidence of demand. Low engagement among target clients is concerning.
- Willingness to pay is a stronger signal than an inconclusive POC. Distinguish stated interest from a paid customer.

## Reading the KPI dashboard

The dashboard is one view of performance, not the full company story. Interpret its metrics in the context of the company's vertical, product, target customer, and business model. For B2B, connect headline traction to engagement from target clients, POC outcomes, willingness to pay, paid customers, and the pricing model. For games, connect the headline to shipped titles and sales, or for an unreleased title to wishlists, community, trailer reach, publicity, audience size, quality, competition, and a cautiously read forecast.

Strong-looking dashboard figures still call for two questions: can the company deliver the promise behind them, and why are the figures so good? Investigate the underlying evidence and explanation before treating a headline number as proof of durable traction.

## Monthly revenue by customer

When reviewing the raw monthly customer-revenue file for a B2B company, start with signed contracts, subscribers, and transaction history. Use the file as customer-level evidence to test the dashboard's business-performance story.

- For a subscription business, pre-orders and a credit card on file make a customer more likely to be real; verify the related subscription and transaction history.
- For a contract-based business, signed contract value counts as traction in this expert lens. Label it as contracted or booked value, separately from recognized revenue and cash collected. A contract's total value is not automatically ARR or MRR.
- Revenue dependence on one or a few customers is concerning in general. Do not dismiss concentration simply because the company is early.
- Easy cancellation, a short pilot, or a long implementation before launch makes the signed contract value a low-strength traction signal.

## Financial model: revenue forecast

Revenue forecasts should be supported by relevant benchmarks and customer contract evidence. Keep the status of the evidence visible: signed contracts and pipeline are different strengths of support, and neither should be presented as revenue already earned. Benchmarks must fit the business model: B2B and gaming forecasts require very different comparisons. For B2B, Kimmy's first reference point is industry peers. Compare peers broadly across growth, customer count, pricing and contract size, sales cycle, retention, and other relevant measures. Do not assume a generic average is comparable.

For gaming, benchmark the forecast against the performance of games in the same genre, comparing sales and revenue across the launch period, first year, and lifetime. These comparison windows come from expert input in this working session; no numeric peer benchmarks have been supplied.

### Separate traction, revenue, and recurring run rate

Kimmy confirmed this distinction for the model and its financial analysis: booked traction counts, while revenue and ARR/MRR remain separate.

- **Signed contracts:** count signed value as booked traction, with term and recurring portion visible. Keep booked value separate from revenue recognized as the service is delivered and cash collected. For signed recurring commitments that are not live, report committed ARR separately from live ARR. [a16z: bookings versus revenue](https://a16z.com/16-startup-metrics/); [Bessemer: ARR and CARR](https://www.bvp.com/atlas/scaling-to-100-million).
- **Pre-orders:** treat paid or committed pre-orders as evidence of demand, especially for a game, but show them as orders/bookings until delivery and do not put one-time pre-orders in ARR/MRR.
- **Pilots:** show paid pilot activity as revenue/traction in its own line. Do not annualize a temporary pilot into ARR/MRR unless it converts into an active recurring contract.
- **One-time sales and services:** include them in total revenue when earned, but separate them from recurring product revenue. Exclude one-time fees and professional services from ARR/MRR. [a16z: recurring revenue](https://a16z.com/16-startup-metrics/).
- **Variable usage charges:** show usage revenue separately and examine its pattern over time. Do not turn a single variable-usage month into subscription ARR by multiplying it by 12. [a16z: 16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/).

These are reporting distinctions, not claims that non-recurring revenue is worthless. They let the investor see demand without overstating the durable recurring base. For transaction-led businesses and games, use the business's own sales and usage measures rather than forcing every dollar into SaaS ARR/MRR.

## Stage expectations

- **B2B at Series A:** expect meaningful revenue, a business entering a real growth stage, and high customer adoption. These are qualitative expectations; no numeric cutoff for "meaningful" or "high adoption" has been supplied.
- **Gaming at Series A:** expect the game to have shipped. Expert input supplied a heuristic of EBITDA over 18 months above 15x development cost. This is Kimmy's judgment, not an externally sourced industry benchmark; treat it as a context-dependent expert heuristic, not a universal pass/fail rule.

## Sources and boundaries

- The KPI dashboard source guide describes the document, stage expectations, metric definitions, consistency checks, and common ARR/MRR pitfalls: [KPI dashboard or metrics export](../docs/reports/20261022.03_document_guides/kpi-dashboard-or-metrics-export.md).
- The qualitative company-screening and business-model guidance above comes from expert input in this working session. It is not a sourced numeric benchmark.
- No stage-specific numeric benchmark has been supplied here. Do not invent one. Where a comparison is needed, use sourced evidence specific to the vertical and business model, and show its context.
