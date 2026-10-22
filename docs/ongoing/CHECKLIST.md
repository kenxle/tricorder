# Checklist

## Charter

**What belongs:** Every item Tricorder looks for in a first pass, one row each. An item is a document in the data room, a check Tricorder runs on those documents, an outside-world item, or a question to ask the founder. Each row says when the item is expected (pre-seed, seed, Series A), where it comes from, which [FRAMEWORKS.md](FRAMEWORKS.md) entry checks it, and which published checklists name it.

**What does not:** How a check works: its inputs, prompt and output shape belong in [FRAMEWORKS.md](FRAMEWORKS.md). What the readout looks like belongs in [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md) and [STYLE_GUIDE.md](STYLE_GUIDE.md). Who the investors are belongs in [PERSONAS.md](PERSONAS.md).

**Level of detail:** One line per item, short enough to scan. A builder can tell from a row whether a scan covers the item and what to ask for when the room lacks it. [checklist.csv](checklist.csv) holds the same rows with a few more columns. Change the CSV and the table together, then rerun [checklist_counts.py](checklist_counts.py) and paste its output under "Counts".

**Sources:**

- [The writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), its 1:56 PM block (this checklist) and the blocks from 12:55 PM on (the readout's pieces, contracts as an input, accounting mislabels, the ask list, stage grouping)
- [The data-room research](../reports/20261022.02_research/research_data_room.md): the 30-document table in Part 1, its section 1.1 on DocSend's two checklist pages, and the red flags in Part 2, with [data_room_documents.csv](../reports/20261022.02_research/data_room_documents.csv), [data_room_flags.csv](../reports/20261022.02_research/data_room_flags.csv) and [data_room_files.csv](../reports/20261022.02_research/data_room_files.csv)
- [What a data room is](../reports/20261022.02_research/what_is_a_data_room.md)
- DocSend's two checklist pages, read through a browser and saved: [The Startup Fundraising Due Diligence Checklist](https://www.docsend.com/blog/due-diligence-checklist/) ([saved copy](../reports/20261022.02_research/raw/data_room/docsend_com_blog_due_diligence_checklist.txt)), shown as "DocSend checklist", and a seed investor's [4 Types of Documents Founders Must Have](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) ([saved copy](../reports/20261022.02_research/raw/data_room/docsend_com_blog_4_types_of_documents_founders_must_have.txt)), shown as "DocSend seed investor"
- [ROADMAP.md](ROADMAP.md), for which checks run on Saturday
- [The voice-of-the-customer research](../reports/20261022.02_research/research_voice_of_customer.md), for the associate's ten tabs and the pre-term-sheet checks
- [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md), "What Tricorder gathers before the data room is opened" and "The readout"
- [FRAMEWORKS.md](FRAMEWORKS.md), for the entry that checks each item
- [PERSONAS.md](PERSONAS.md), for what each stage usually has

## How the checklist is used

It drives three things.

- **The scans.** A scan looks for the items whose rows name its entry. A row marked "not checked yet" is a check still to write.
- **The readout's coverage panel.** For the company's stage, each item shows as found, checked or missing. The CSV's `hollis_voice_file` column says where each document sits in the demo room.
- **The ask list.** Each missing item marked "yes" at the company's stage becomes a request to the founder. An item marked "lighter" goes on the list as "if you have it". A missing document is a question for the operator, not a red flag (the data-room research, 1.5). An agent builds this part from now to Friday night, in the roadmap's checklist-coverage slice. Without it, the ask list comes only from the scans' gaps and the weak pieces ([FRAMEWORKS.md](FRAMEWORKS.md), "Ask list").

## How to read the rows

- **Pre-seed, seed, Series A.** "Yes" means expected. "Lighter" means a lighter version, or only if the company has it. "No" means left out at that stage. "Not stated" means the research's sources do not say.
- **Where the stage comes from.** A document row takes its letters from the data-room research's table (section 1.2). A check takes the letters of the documents it reads, and the least expected one wins. An outside-world item is public, so it is marked "yes" at every stage: at the earliest stage these items carry the first pass (writers' brief, 1:38 PM block). The CSV's `stage_basis` column gives the basis for each row.
- **Comes from.** "Data room" is a file the founder shares. "Outside" is a public source Tricorder reads itself. "Ask the founder" is something only the founder can give.
- **Checked by.** The FRAMEWORKS entry, by number and name. Every entry is built by the end of Saturday. A row with no mark is built by the team on Saturday, as the roadmap scopes it. Inside a row, "(now to Friday night)" marks an entry an agent builds before Saturday. The CSV's `check_status` column holds the row's status. "Not checked yet" means no entry checks it. [FRAMEWORKS.md](FRAMEWORKS.md), "When each entry runs", is the full list.
- **Named by.** The published checklists and guides that name the item, linked as the research links them. "None in the research" means no published list in the research names it. Those items come from the writers' brief, the organisers' tracks or a FRAMEWORKS entry.
- **Contracts.** FRAMEWORKS 1.13 (contract terms) reads every contract and compares its terms with how the customer is counted. On Saturday the model reads every contract in both demo rooms, and the script runs three of the six checks: notice against ARR (row C38), a pilot with no duty to convert (row C39) and the counted price against the contract's (row C42). It is fourth in the roadmap's demo fallback order. An agent builds the plan check (row C40), the signed-not-live check (row C41) and the missing-contract check (row C43) from now to Friday night (FRAMEWORKS 1.13, "Scope").
- **Market signals.** On Saturday, 3.1 and 3.2 show competitors only, from readings an agent saves this week (rows C49 and C50). The company's own signals are built from now to Friday night, in the outside-in slice (rows C88, C89 and C93).
- **DocSend.** DocSend's own checklist frames every item as diligence after a term sheet and names no stage, so the items only it names are marked "not stated" at every stage. That includes its 2026 group on AI and data governance. The seed investor's post names four must-haves for any fundraising data room (financial statements and projections, a reference list, current and pro forma cap tables, investment documents). The two rows only that post adds, C95 (the pro forma cap table) and C97 (the reference list), are marked "yes" at every stage. Rows the research already had keep their marks, with DocSend added to "Named by".
- **Rows a roadmap slice will check.** Some rows marked "not checked yet" have a slice that will add their check: C28 (the bank feed) in bank-check, C90 (investors) in outside-in, and C46 and C58 (reference calls) in reference-checks.

## Counts

From [checklist_counts.py](checklist_counts.py), run on [checklist.csv](checklist.csv):

```
Items: 109

By piece
  traction and revenue: 13
  retention: 5
  burn and runway: 11
  unit economics: 4
  customers and contracts: 13
  market: 4
  comps: 2
  team: 7
  the pitch itself: 14
  legal and cap table: 21
  AI and data governance: 8
  outside world: 7

By kind
  document: 46
  check: 45
  outside: 14
  ask: 4

By where it comes from
  data room: 90
  outside: 14
  founder: 5

By stage expectation
  stage: yes, lighter, no, not stated
  Pre-seed: 34, 21, 29, 25
  Seed: 51, 40, 2, 16
  Series A: 90, 6, 0, 13

By whether a check exists
  yes: 72
  no: 37

By check status
  now to Friday night: 38
  Saturday: 34
  not checked yet: 37

No check yet, by piece
  traction and revenue: 3
  retention: 1
  burn and runway: 1
  unit economics: 0
  customers and contracts: 4
  market: 0
  comps: 0
  team: 3
  the pitch itself: 4
  legal and cap table: 12
  AI and data governance: 8
  outside world: 1
```

## The checklist

### Traction and revenue

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C01 | Audited or reviewed financials (document) | no | no | lighter | Data room | 1.11 What the room cannot settle (asks for it when missing) (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C02 | KPI dashboard or metrics export (MRR, ARR, customers, churn) (document) | lighter | yes | yes | Data room | 1.5 Deck-against-model reconciliation; 1.8 Vanity metric check; 1.12 Accounting mislabels (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| C03 | Monthly revenue by customer (document) | not stated | lighter | yes | Data room | 1.2 ARR definition check; 1.3 Cohort retention rebuild; 1.6 Customer concentration; 1.12 Accounting mislabels (now to Friday night) | [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/) |
| C04 | Investor update archive (document) | no | lighter | yes | Data room | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room) |
| C05 | ARR rebuilt from contracts and revenue rows: subscription lines only, no pilot, one-time fee or services | no | lighter | yes | Data room: revenue by customer by month; customer contracts | 1.2 ARR definition check | [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [a16z 16 more](https://a16z.com/16-more-startup-metrics/), [Bessemer](https://www.bvp.com/atlas/scaling-to-100-million), [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [Lighter MRR](https://www.lightercapital.com/blog/four-metrics-to-track-when-raising-capital-for-your-saas-company), [Lighter CMRR](https://www.lightercapital.com/blog/how-to-calculate-committed-mrr-cmrr), [CRV](https://www.crv.com/content/what-is-a-data-room) |
| C06 | MRR column matches the subscription rows | not stated | lighter | yes | Data room: metrics export; revenue by customer by month | 1.12 Accounting mislabels, kind a (now to Friday night) | [Lighter MRR](https://www.lightercapital.com/blog/four-metrics-to-track-when-raising-capital-for-your-saas-company), [a16z 16 metrics](https://a16z.com/16-startup-metrics/) |
| C07 | Revenue is what was delivered, not bookings or billings | not stated | lighter | yes | Data room: monthly P&L; revenue by customer by month with billings | 1.12 Accounting mislabels, kind b (now to Friday night) | [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) |
| C08 | Revenue is net, not gross transaction value or pass-through money | lighter | yes | yes | Data room: monthly P&L; a revenue export with a volume column | 1.12 Accounting mislabels, kind c (now to Friday night) | none in the research |
| C09 | Cash collected ahead of delivery is not counted as earned | not stated | lighter | yes | Data room: monthly P&L and balance sheet; revenue by customer by month with billings | 1.12 Accounting mislabels, kind g (now to Friday night) | none in the research |
| C10 | One-time fees kept out of MRR, ARR and recurring revenue | not stated | lighter | yes | Data room: metrics export; revenue by customer by month | 1.12 Accounting mislabels, kind h (now to Friday night) | [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [a16z 16 more](https://a16z.com/16-more-startup-metrics/), [Bessemer](https://www.bvp.com/atlas/scaling-to-100-million) |
| C11 | A cumulative count (sign-ups, downloads) is not shown as active customers | lighter | yes | yes | Data room: metrics export; the deck | 1.8 Vanity metric check | [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [a16z 16 more](https://a16z.com/16-more-startup-metrics/) |
| C12 | Earlier investor updates agree with today's numbers | no | lighter | yes | Data room: investor update archive | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room) |
| C13 | Reviewed or audited numbers match management numbers | no | no | lighter | Data room: audited or reviewed financials; monthly P&L | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |

### Retention

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C14 | Cohort or retention export (document) | no | lighter | yes | Data room | 1.3 Cohort retention rebuild | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room), [Peony](https://www.peony.ink/blog/series-a-data-room), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C15 | Gross and net retention rebuilt from revenue by customer and compared with the deck | no | lighter | yes | Data room: revenue by customer by month; cohort export | 1.3 Cohort retention rebuild | [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [a16z 16 more](https://a16z.com/16-more-startup-metrics/), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/), [SaaStr GRR](https://www.saastr.com/dear-saastr-were-at-13m-arr-and-growing-but-our-grr-is-slipping-what-should-we-do/), [SaaStr top 10](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/), [Janz on Chen](https://andrewchen.com/the-easiest-spreadsheet-for-churn-mrr-and-cohort-analysis-guest-post/) |
| C16 | Newer cohorts do at least as well as older ones | no | lighter | yes | Data room: revenue by customer by month; cohort export | 1.3 Cohort retention rebuild | [a16z 16 more](https://a16z.com/16-more-startup-metrics/) |
| C17 | No cohorts or periods left out, and enough months of history | no | lighter | yes | Data room: revenue by customer by month; cohort export | 1.3 Cohort retention rebuild | [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/) |
| C18 | Customers who keep paying but use the product far less (stealth churn) | not stated | lighter | yes | Data room: usage data in the metrics export; revenue by customer by month | not checked yet | [SaaStr stealth churn](https://www.saastr.com/stealth-ai-churn-are-your-customers-starting-to-leave-already/) |

### Burn and runway

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C19 | Financial model, 3 to 5 years (document) | yes | yes | yes | Data room | 1.4 Burn against the hiring plan and runway; 1.5 Deck-against-model reconciliation; 1.12 Accounting mislabels (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room), [Peony](https://www.peony.ink/blog/series-a-data-room), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [NFX](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C20 | Historical P&L, balance sheet, cash flow (monthly) (document) | lighter | yes | yes | Data room | 1.4 Burn against the hiring plan and runway; 1.12 Accounting mislabels (now to Friday night) | [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [BCV](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/), [CRV](https://www.crv.com/content/what-is-a-data-room), [DocSend](https://www.docsend.com/blog/virtual-data-room-for-startups/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C21 | Bank statements (3 to 12 months) (document) | no | lighter | yes | Data room | 1.11 What the room cannot settle (ties deposits to revenue when present) (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups), [Peony](https://www.peony.ink/blog/series-a-data-room), [SaaStr on diligence](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) |
| C22 | Hiring plan and future org (document) | lighter | yes | yes | Data room | 1.4 Burn against the hiring plan and runway | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Kruze cash forecast](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/) |
| C23 | Expense ledger or expense breakdown by function (document) | not stated | not stated | yes | Data room | 1.7 Gross margin composition; 1.9 Unit economics recompute (now to Friday night); 1.12 Accounting mislabels (now to Friday night) | [CRV](https://www.crv.com/content/what-is-a-data-room) |
| C24 | Payroll rebuilt from the hiring plan, burn and runway recomputed and compared with the deck | lighter | yes | yes | Data room: financial model; monthly P&L; hiring plan | 1.4 Burn against the hiring plan and runway | [Kruze cash forecast](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/), [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [SaaStr top 10](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/), [NFX](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising) |
| C25 | Contractors counted in headcount and burn | lighter | yes | yes | Data room: expense ledger; monthly P&L; hiring plan | 1.12 Accounting mislabels, kind e (now to Friday night) | none in the research |
| C26 | Capitalised costs do not keep cash spend off the P&L | lighter | yes | yes | Data room: expense ledger; monthly P&L; the model's cash tab | 1.12 Accounting mislabels, kind f (now to Friday night) | none in the research |
| C27 | Revenue in the deck reaches the bank | no | lighter | yes | Data room: bank statements; monthly P&L | 1.11 What the room cannot settle (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups), [SaaStr on diligence](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) |
| C28 | Bank feed through a banking connector: deposits against revenue rows, outflows against burn | no | lighter | yes | Ask the founder: the founder consents to connect the company's bank account (roadmap item, writers' brief 1:52 PM block) | not checked yet | none in the research |
| C29 | Current monthly burn and the bank balance behind it | lighter | yes | yes | Ask the founder: the current figures | 1.11 What the room cannot settle (writes the ask) (now to Friday night) | [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |

### Unit economics

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C30 | Unit economics (CAC, LTV, payback) (document) | no | lighter | yes | Data room | 1.9 Unit economics recompute (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [Peony](https://www.peony.ink/blog/series-a-data-room), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C31 | Gross margin rebuilt with every delivery cost: hosting, model inference, support | lighter | yes | yes | Data room: expense ledger; monthly P&L | 1.7 Gross margin composition; 1.12 Accounting mislabels, kind d | [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [a16z 16 more](https://a16z.com/16-more-startup-metrics/), [Tunguz](https://tomtunguz.com/not-all-revenue-dollars-are-created-equal/), [Stripe](https://stripe.com/en-se/resources/more/saas-gross-margin-explained-what-it-is-and-why-it-is-important), [Bessemer](https://www.bvp.com/atlas/scaling-to-100-million), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C32 | CAC, payback and LTV recomputed from spend and customer counts | not stated | lighter | yes | Data room: monthly P&L; metrics export; revenue by customer by month | 1.9 Unit economics recompute (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| C33 | Blended CAC does not hide weak paid channels | not stated | lighter | yes | Data room: monthly P&L; metrics export; revenue by customer by month | 1.9 Unit economics recompute (now to Friday night) | [a16z 16 metrics](https://a16z.com/16-startup-metrics/) |

### Customers and contracts

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C34 | Customer contracts and order forms (top ten) (document) | no | lighter | yes | Data room | 1.2 ARR definition check; 1.6 Customer concentration; 1.13 Contract terms | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Peony](https://www.peony.ink/blog/series-a-data-room), [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C35 | Customer references and letters of intent (document) | no | lighter | yes | Data room | 1.11 What the room cannot settle (asks for it when missing) (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Peony](https://www.peony.ink/blog/series-a-data-room), [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/), [CRV](https://www.crv.com/content/what-is-a-data-room), [SaaStr on diligence](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C36 | Sales pipeline snapshot (document) | no | lighter | yes | Data room | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) |
| C37 | Customer concentration: top-one and top-three share against the deck's claim | not stated | lighter | yes | Data room: revenue by customer by month; the largest customer's contract | 1.6 Customer concentration | [a16z 16 more](https://a16z.com/16-more-startup-metrics/), [MicroVentures](https://microventures.com/revenue-concentration-risk-when-one-customer-is-too-many), [Peony](https://www.peony.ink/blog/series-a-data-room), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) |
| C38 | A customer who can leave on short notice is not counted as a year of ARR | no | lighter | yes | Data room: customer contracts; revenue by customer by month; the model's ARR build | 1.13 Contract terms | [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C39 | A pilot or trial with no duty to convert is not counted as recurring | no | lighter | yes | Data room: customer contracts; revenue by customer by month; monthly P&L | 1.2 ARR definition check; 1.13 Contract terms | [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) |
| C40 | The plan keeps no revenue past a contract's end, and does not treat an auto-renewal as certain | no | lighter | yes | Data room: customer contracts; the model's plan columns | 1.13 Contract terms (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C41 | A signed contract that has not gone live is not counted as revenue | no | lighter | yes | Data room: customer contracts; revenue by customer by month | 1.13 Contract terms (now to Friday night) | [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/), [Lighter CMRR](https://www.lightercapital.com/blog/how-to-calculate-committed-mrr-cmrr) |
| C42 | The counted price matches the contract's price and discount | no | lighter | yes | Data room: customer contracts; revenue by customer by month | 1.13 Contract terms | none in the research |
| C43 | Every counted customer line has a contract in the room | no | lighter | yes | Data room: the model's ARR build; revenue by customer by month; customer contracts | 1.13 Contract terms (now to Friday night) | [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Peony](https://www.peony.ink/blog/series-a-data-room) |
| C44 | Letters of intent and verbal agreements kept out of revenue and bookings | no | lighter | yes | Data room: letters of intent; customer contracts | not checked yet | [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) |
| C45 | Sales pipeline against the growth plan | no | lighter | yes | Data room: pipeline snapshot; financial model | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/) |
| C46 | Customer reference calls | no | lighter | yes | Ask the founder: names of customers to call | not checked yet | [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/), [CRV](https://www.crv.com/content/what-is-a-data-room), [SaaStr on diligence](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |

### Market

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C47 | Market sizing and competitive landscape (document) | yes | yes | yes | Data room | 5.6 TAM, SAM and SOM, bottom-up (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C48 | Bottom-up TAM, SAM and SOM against the deck's market size | yes | yes | yes | Data room: the deck's market slide; competitor and pricing signals | 5.6 TAM, SAM and SOM, bottom-up (now to Friday night) | [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| C49 | Competitors' hiring, headcount, web traffic and reviews against the deck's competition slide | yes | yes | yes | Outside: Akta signals; careers pages; app store ratings | 3.1 Hiring, web traffic and reviews (this week's readings, shown on Saturday) | none in the research |
| C50 | Published pricing and announced customer wins, for the company and its competitors | yes | yes | yes | Outside: pricing pages; news search; Akta News Signals | 3.2 Pricing changes and customer wins (this week's readings, shown on Saturday) | none in the research |

### Comps

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C51 | Public comparable companies, each with the reason it is a fair comp | yes | yes | yes | Outside: SEC EDGAR filings | 2.1 Public comps from EDGAR | none in the research |
| C52 | Recent private rounds of similar size, and whether the ask is in line | yes | yes | yes | Outside: SEC Form D data sets; search | 2.2 Recent private rounds | none in the research |

### Team

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C53 | Founder bios (document) | yes | yes | yes | Data room | 6.1 Founder-market fit; 6.2 Passion and commitment (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [DocSend](https://www.docsend.com/blog/virtual-data-room-for-startups/) |
| C54 | Key team bios and org chart (document) | lighter | yes | yes | Data room | 6.1 Founder-market fit (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C55 | Founder-market fit from dated public work: roles, shipped projects, talks, writing (never LinkedIn scraping) | yes | yes | yes | Outside: founder bios; GitHub; personal sites; talks; arXiv | 6.1 Founder-market fit; 6.2 Passion and commitment (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| C56 | The people in the plan exist | lighter | yes | yes | Outside: key team bios; public profiles | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C57 | Background checks on the founders | not stated | not stated | not stated | Outside: a background check, after the term sheet | not checked yet | [SaaStr on diligence](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) |
| C58 | Founder reference calls | not stated | not stated | not stated | Ask the founder: names of people who know the founders | not checked yet | [Form Ventures](https://formventures.substack.com/p/team-talks-ii-founder-reference-calls), [First Round](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C97 | Reference list: management, customers, current investors, advisors (document) | yes | yes | yes | Data room | 1.11 What the room cannot settle (asks for customer references when missing) (now to Friday night) | [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |

### The pitch itself

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C59 | Cover note and document index (document) | yes | yes | yes | Data room | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room) |
| C60 | Pitch deck (document) | yes | yes | yes | Data room | 1.1 Deck claim extraction; 1.5 Deck-against-model reconciliation | [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [Peony](https://www.peony.ink/blog/series-a-data-room), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C61 | One-page summary (document) | yes | yes | yes | Data room | 1.1 Deck claim extraction; 1.5 Deck-against-model reconciliation (now to Friday night) | [YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C62 | Founder video or recorded intro (document) | lighter | lighter | lighter | Data room | 4.1 Claim extraction with timestamps; 4.3 Three-way disagreement check | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C63 | Product roadmap and demo (document) | yes | yes | yes | Data room | 1.1 Deck claim extraction; 3.2 Pricing changes and customer wins (now to Friday night) | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C64 | Every number on the deck pulled out as a claim and tied to a file | yes | yes | yes | Data room: the deck and its claims page | 1.1 Deck claim extraction | [Peony](https://www.peony.ink/blog/series-a-data-room), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) |
| C65 | Deck numbers match the model and the metrics export | lighter | yes | yes | Data room: the deck; financial model; metrics export | 1.5 Deck-against-model reconciliation | [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [CRV](https://www.crv.com/content/what-is-a-data-room), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C66 | Numbers spoken on the video match the deck | lighter | lighter | lighter | Data room: pitch video, transcribed with timestamps | 4.1 Claim extraction with timestamps; 4.3 Three-way disagreement check | none in the research |
| C67 | The ask on the deck matches the round in the cap table | yes | yes | yes | Data room: the deck's ask slide; cap table | 1.10 Cap table reconciliation | none in the research |
| C68 | Product roadmap against the use of funds | yes | yes | yes | Data room: product roadmap; the deck's use of funds | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) |
| C69 | No stale document that disagrees with current numbers | yes | yes | yes | Data room: every file's date against the deck's as-of date | not checked yet | [CRV](https://www.crv.com/content/what-is-a-data-room), [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room) |
| C70 | No chart with a truncated y-axis, or a cumulative chart for a metric that should not be cumulative | yes | yes | yes | Data room: the deck's charts | 1.8 Vanity metric check (cumulative columns only; truncated axes not checked) | [a16z 16 metrics](https://a16z.com/16-startup-metrics/), [a16z 16 more](https://a16z.com/16-more-startup-metrics/) |
| C71 | The founder walks from the source data to each flagged number | yes | yes | yes | Ask the founder: one line per flag | 1.11 What the room cannot settle (writes the ask) (now to Friday night) | [Hustle Fund red flags](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore) |
| C96 | Use of funds plan for this round (document) | lighter | lighter | lighter | Data room | not checked yet | [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |

### Legal and cap table

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C72 | Cap table, fully diluted (document) | yes | yes | yes | Data room | 1.10 Cap table reconciliation | [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [CRV](https://www.crv.com/content/what-is-a-data-room), [Peony](https://www.peony.ink/blog/series-a-data-room), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups), [Ellty](https://www.ellty.com/blog/how-investors-review-a-data-room), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C73 | 409A valuation (document) | no | lighter | yes | Data room | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Peony](https://www.peony.ink/blog/series-a-data-room) |
| C74 | Incorporation documents and bylaws (document) | yes | yes | yes | Data room | not checked yet | [Cooley GO](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room), [DocSend](https://www.docsend.com/blog/virtual-data-room-for-startups/), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C75 | Prior financing: SAFEs, notes, term sheets (document) | yes | yes | yes | Data room | 1.10 Cap table reconciliation (reads the SAFE terms) | [Cooley GO](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C76 | IP and invention assignment agreements (document) | lighter | yes | yes | Data room | 1.11 What the room cannot settle (asks for it when missing) (now to Friday night) | [CRV](https://www.crv.com/content/what-is-a-data-room), [Cooley GO](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups), [Peony](https://www.peony.ink/blog/series-a-data-room), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C77 | Board and stockholder minutes (document) | lighter | yes | yes | Data room | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [Peony](https://www.peony.ink/blog/series-a-data-room), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C78 | Employment, advisory and option grant records (document) | no | lighter | yes | Data room | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [SeedLegals](https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [Peony](https://www.peony.ink/blog/series-a-data-room), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C79 | Tax returns (three years) (document) | not stated | not stated | yes | Data room | 1.11 What the room cannot settle (asks for it when missing) (now to Friday night) | [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C80 | Disclosure of claims, disputes and regulatory inquiries (document) | yes | yes | yes | Data room | not checked yet | [Cooley GO](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C81 | Cap table adds to 100 percent fully diluted, every SAFE converts at its cap, the option pool is shown | yes | yes | yes | Data room: cap table; SAFE and note terms | 1.10 Cap table reconciliation | [a16z data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/), [CRV](https://www.crv.com/content/what-is-a-data-room), [Peony](https://www.peony.ink/blog/series-a-data-room), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups) |
| C82 | Every instrument and grant on the cap table has a document | no | lighter | yes | Data room: cap table; financing documents; grant records | 1.10 Cap table reconciliation (now to Friday night) | [Cooley GO](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [SeedLegals](https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C83 | Every founder and contractor signed an IP assignment | lighter | yes | yes | Data room: IP and invention assignment agreements | 1.11 What the room cannot settle (checks the file is there; signatures not read) (now to Friday night) | [CRV](https://www.crv.com/content/what-is-a-data-room), [Cooley GO](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups) |
| C84 | Incorporation papers and minutes match the cap table and approve each financing | lighter | yes | yes | Data room: incorporation documents; board and stockholder minutes | not checked yet | [Cooley GO](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [CRV](https://www.crv.com/content/what-is-a-data-room) |
| C85 | 409A valuation is current | no | lighter | yes | Data room: 409A valuation | not checked yet | [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) |
| C86 | Tax returns were filed | not stated | not stated | yes | Data room: tax returns | 1.11 What the room cannot settle (checks the file is there) (now to Friday night) | [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) |
| C87 | Claims, disputes and regulatory inquiries read and listed | yes | yes | yes | Data room: disclosure of claims and disputes | not checked yet | [Cooley GO](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/), [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C95 | Pro forma cap table, after this round (document) | yes | yes | yes | Data room | 1.10 Cap table reconciliation | [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) |
| C98 | Material agreements with obligations over $25,000 (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C99 | Insurance policies (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C100 | Loans, liens and other encumbrances on the company (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C101 | Patents, trademarks, copyrights and domain names (document) | lighter | lighter | lighter | Data room | not checked yet | [DocSend seed investor](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |

### AI and data governance

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C102 | AI model documentation: architecture, training, performance and validation (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C103 | Training data provenance and the rights to use it (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C104 | Agreements with third-party AI service providers (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C105 | Data privacy compliance (GDPR, CCPA and other regional rules) (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C106 | AI ethics and bias testing policies (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C107 | Responsible AI framework: internal guidelines (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C108 | Model security: theft, adversarial attacks, prompt injection (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |
| C109 | Preparation for emerging AI regulation (document) | not stated | not stated | not stated | Data room | not checked yet | [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) |

### Outside world

| Id | Item | Pre-seed | Seed | Series A | Comes from | Checked by | Named by |
|---|---|---|---|---|---|---|---|
| C88 | Traffic: web traffic and its trend for the company | yes | yes | yes | Outside: Akta's web traffic signal | 3.1 Hiring, web traffic and reviews (for the company itself) (now to Friday night) | [the associate's ten tabs](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| C89 | Reviews: ratings, review counts and what reviewers complain about | yes | yes | yes | Outside: app store pages; review sites found by search | 3.1 Hiring, web traffic and reviews (for the company itself); 7.1 Footprint: web, Hacker News, Product Hunt and app stores (now to Friday night) | [the associate's ten tabs](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| C90 | Investors: who has invested, how much and when, checked against the cap table | yes | yes | yes | Outside: Crunchbase; SEC Form D; press | not checked yet | [the associate's ten tabs](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| C91 | Co-founder issues: how long the founders have worked together, who left, public disputes | yes | yes | yes | Outside: founder bios; GitHub; personal sites; talks; press | 6.2 Passion and commitment (tenure only) (now to Friday night) | [the associate's ten tabs](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| C92 | Whether the story matches what is online: each deck claim against the website, press, Hacker News and Product Hunt | yes | yes | yes | Outside: the website; Hacker News; Product Hunt; search | 7.1 Footprint: web, Hacker News, Product Hunt and app stores (now to Friday night) | [the associate's ten tabs](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) |
| C93 | The company's own hiring: open roles and headcount trend against the hiring plan | yes | yes | yes | Outside: Akta job posts and headcount trends; careers page | 3.1 Hiring, web traffic and reviews (for the company itself) (now to Friday night) | none in the research |
| C94 | Reddit threads about the company or its competitors | yes | yes | yes | Outside: Reddit pages saved by hand; never fetched by a script | 7.2 Reddit threads saved by hand (now to Friday night) | none in the research |
