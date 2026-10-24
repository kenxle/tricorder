// Written by piece_reports.py. Do not edit by hand.
window.TC_PIECE_REPORTS_DATA = {
 "ploy": [
  {
   "key": "piece-retention",
   "piece": "retention",
   "title": "Retention",
   "knowledge": "knowledge/retention.md",
   "paras": [
    {
     "lead": "Only the model states it.",
     "refs": [
      "re-1"
     ],
     "body": "The model assumes monthly churn of 2.0%. No other file in the room states a retention figure, and the model does not say whether it counts customers or revenue."
    },
    {
     "lead": "What that means over a year.",
     "refs": [
      "re-1"
     ],
     "body": "Compounded for 12 months, 2.0% a month leaves 78.5% of the starting customers or revenue. One SaaS investor reads gross retention under 80% as a churn problem to fix before scaling."
    },
    {
     "lead": "The record is too short to test it.",
     "refs": [
      "tr-3"
     ],
     "body": "The customer file runs from 2026-01 to 2026-09: 9 months. A 12-month retention figure needs 12 months, so the room can neither confirm nor rebuild the model's churn."
    },
    {
     "lead": "Gross and net are both missing.",
     "refs": [],
     "body": "Net retention would show whether customers who stay spend more. Gross retention would show what is lost. The room shows neither, so the retention piece reads not enough in the room."
    }
   ],
   "asks": [
    "Does the 2.0% monthly churn count customers or revenue, and what data is it based on?",
    "A cohort export from 2026-01, with gross and net revenue retention at each month.",
    "Churn split by plan, with self-serve and enterprise apart."
   ],
   "chart": {
    "kind": "line",
    "unit": "percent",
    "x": [
     0,
     1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     10,
     11,
     12
    ],
    "x_title": "Months after a customer starts",
    "series": [
     {
      "name": "The model's 2.0% a month, compounded",
      "y": [
       100.0,
       98.0,
       96.04,
       94.12,
       92.24,
       90.39,
       88.58,
       86.81,
       85.08,
       83.37,
       81.71,
       80.07,
       78.47
      ],
      "style": "plan"
     }
    ],
    "line": {
     "y": 80,
     "label": "80%: one investor's gross retention line"
    },
    "mark": {
     "x": 8,
     "label": "Oldest customers in the file: 8 months in"
    },
    "end": "78.5% at 12 months",
    "label": "Share of customers or revenue left each month at the model's 2.0% monthly churn: 78.5% after 12 months, under the 80% line. The oldest customers in the file are 8 months in."
   },
   "needs": [
    "02_financials/financial_model.xlsx",
    "03_metrics/customer_mrr_by_month.csv",
    "04_customers/order_form_northwind_analytics.pdf"
   ]
  },
  {
   "key": "piece-unit_economics",
   "piece": "unit_economics",
   "title": "Unit economics",
   "knowledge": "knowledge/unit_economics.md",
   "paras": [
    {
     "lead": "What it costs to serve.",
     "refs": [
      "ue-2"
     ],
     "body": "September revenue was $233,500. The model counts $19,800 of hosting and $31,570 of support as cost of revenue, for a gross margin of 78.0%."
    },
    {
     "lead": "Inference is a delivery cost.",
     "refs": [
      "ue-3",
      "ue-1"
     ],
     "body": "Model inference cost $60,950 in September, and the ledger books it under research and development. The product runs the model to do each customer's work, so it belongs in cost of revenue. Counted there, gross margin is 51.9%. The deck says 78%."
    },
    {
     "lead": "Against the benchmarks.",
     "refs": [
      "ue-3"
     ],
     "body": "Bessemer's cloud companies average 65 to 70%. a16z sees AI companies often at 50 to 60%. At 51.9% the margin sits inside a16z's 50 to 60% range for AI companies. The deck's 78% is above Bessemer's 65 to 70% cloud average."
    },
    {
     "lead": "Prices check out. Acquisition cost is missing.",
     "refs": [
      "ue-4"
     ],
     "body": "The model's prices match the public pricing page. The room holds no acquisition cost or payback period, so what a customer earns against what it costs to win cannot be checked."
    }
   ],
   "asks": [
    "Model inference invoices for July to September, and how the cost moves with usage.",
    "Gross margin by plan, with inference in cost of revenue.",
    "Acquisition cost and payback by channel, with payback measured on gross profit."
   ],
   "chart": {
    "kind": "bars",
    "unit": "percent",
    "barmode": "stack",
    "x": [
     "The model's books",
     "With inference in cost of revenue"
    ],
    "range": [
     0,
     100
    ],
    "series": [
     {
      "name": "Gross profit",
      "y": [
       78.0,
       51.9
      ],
      "style": "good",
      "text": [
       "78.0% margin",
       "51.9% margin"
      ],
      "textposition": "inside",
      "textanchor": "start"
     },
     {
      "name": "Hosting and support",
      "y": [
       22.0,
       22.0
      ],
      "style": "plan"
     },
     {
      "name": "Model inference",
      "y": [
       0.0,
       26.1
      ],
      "style": "bad"
     }
    ],
    "lines": [
     {
      "y": 65,
      "label": "Bessemer: cloud software averages 65 to 70%",
      "style": "accent",
      "right": true
     },
     {
      "y": 55,
      "label": "a16z: AI companies often 50 to 60%",
      "style": "plan",
      "right": true,
      "below": true
     }
    ],
    "label": "Gross margin, each bar 100% of September revenue of $233,500: 78.0% on the model's books, 51.9% with model inference in cost of revenue. Bessemer's cloud average is 65 to 70%."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "02_financials/financial_model.xlsx",
    "02_financials/monthly_statements.xlsx"
   ]
  },
  {
   "key": "piece-customers",
   "piece": "customers",
   "title": "Customers",
   "knowledge": "knowledge/customers.md",
   "paras": [
    {
     "lead": "The largest contract is small.",
     "refs": [
      "cu-1"
     ],
     "body": "Halden Freight pays $18,000 a month: 7.7% of September revenue. Its order form agrees with the customer file, and the deck says no customer is above 10%."
    },
    {
     "lead": "The pilot is the biggest single payer.",
     "refs": [
      "tr-3",
      "cu-1"
     ],
     "body": "Northwind Analytics pays $30,000 a month for a 3-month pilot: 12.8% of September revenue. Counted as a customer, it is above the deck's 10%. If it does not convert, that revenue ends."
    },
    {
     "lead": "The rest is spread across many accounts.",
     "refs": [
      "tr-3"
     ],
     "body": "730 self-serve workspaces bring $141,500 a month, 60.6% of revenue. 5 enterprise contracts bring $62,000."
    },
    {
     "lead": "Paying, not just using.",
     "refs": [
      "tr-4"
     ],
     "body": "1,240 workspaces use credits and 736 of them pay. Paying accounts are the customers. Free use is interest."
    }
   ],
   "asks": [
    "Has Northwind Analytics signed an annual contract? If so, its term, price and notice period.",
    "Term, notice period and renewal date for each enterprise contract.",
    "The top three customers' share of revenue, month by month."
   ],
   "chart": {
    "kind": "bars",
    "unit": "percent",
    "orientation": "h",
    "x": [
     "Northwind Analytics, the pilot",
     "Halden Freight, largest contract",
     "The other 4 contracts",
     "Pro plans, 420 workspaces",
     "Starter plans, 310 workspaces"
    ],
    "height": 300,
    "series": [
     {
      "name": "Share",
      "y": [
       12.85,
       7.71,
       18.84,
       53.96,
       6.64
      ],
      "styles": [
       "bad",
       "mixed",
       "plan",
       "plan",
       "plan"
      ],
      "text": [
       "12.8%",
       "7.7%",
       "18.8%",
       "54.0%",
       "6.6%"
      ]
     }
    ],
    "lines": [
     {
      "y": 10,
      "label": "Deck: no customer above 10%",
      "style": "accent"
     },
     {
      "y": 20,
      "label": "20%: a common investor threshold",
      "style": "bad"
     }
    ],
    "label": "Share of September revenue of $233,500: the pilot 12.8%, the largest contract 7.7%, Pro plans 54.0%."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "03_metrics/customer_mrr_by_month.csv",
    "03_metrics/workspaces_by_plan.csv",
    "04_customers/order_form_northwind_analytics.pdf"
   ]
  },
  {
   "key": "piece-market",
   "piece": "market",
   "title": "Market",
   "knowledge": "knowledge/market.md",
   "paras": [
    {
     "lead": "Count times price.",
     "refs": [
      "ma-4",
      "ma-1",
      "ma-2"
     ],
     "body": "The deck counts 40,000 target companies and the model 36,000. At $3,600 a year each, that is $144,000,000 or $129,600,000. The company's own files disagree by 4,000 companies."
    },
    {
     "lead": "Which price.",
     "refs": [
      "ma-3",
      "tr-3",
      "tr-4"
     ],
     "body": "Both use the Pro plan's list price, which is a ceiling. The 735 workspaces on plans and contracts pay $3,322 a year on average today. At that price the model's count gives $119.61M."
    },
    {
     "lead": "How much is won so far.",
     "refs": [
      "tr-3",
      "ma-2"
     ],
     "body": "Recurring revenue of $2,442,000 a year is 1.9% of the model's market."
    },
    {
     "lead": "Both counts are the company's.",
     "refs": [],
     "body": "The deck and the model come from the founder, so two of them agreeing would still be one estimate. The room holds no outside source for how many companies could buy."
    }
   ],
   "asks": [
    "What makes up the 4,000 companies between the deck's count and the model's.",
    "The source behind the count, and what a target company has to look like to be in it.",
    "The market at the price paying workspaces pay today, by plan."
   ],
   "chart": {
    "kind": "bars",
    "unit": "usd",
    "barmode": "group",
    "x": [
     "Deck: 40,000 companies",
     "Model: 36,000 companies"
    ],
    "series": [
     {
      "name": "At the Pro list price, $3,600 a year",
      "y": [
       144000000,
       129600000
      ],
      "style": "plan",
      "text": [
       "$144.0M",
       "$129.6M"
      ]
     },
     {
      "name": "At what a paying workspace pays today, $3,322 a year",
      "y": [
       132897959.18367347,
       119608163.26530612
      ],
      "style": "mixed",
      "text": [
       "$132.90M",
       "$119.61M"
      ]
     }
    ],
    "label": "Market size, count times price: the deck's 40,000 companies and the model's 36,000, each at the Pro list price of $3,600 a year and at today's $3,322 a year per paying workspace."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "02_financials/financial_model.xlsx",
    "03_metrics/customer_mrr_by_month.csv",
    "03_metrics/workspaces_by_plan.csv",
    "04_customers/order_form_northwind_analytics.pdf"
   ]
  },
  {
   "key": "piece-team",
   "piece": "team",
   "title": "Team",
   "knowledge": "knowledge/team.md",
   "paras": [
    {
     "lead": "The headcount matches the public record.",
     "refs": [
      "te-1"
     ],
     "body": "The deck, the model and the YC page all say 14 people today. The company's files and the public record agreeing on headcount is a small green flag."
    },
    {
     "lead": "The hiring plan more than doubles it.",
     "refs": [
      "bu-2"
     ],
     "body": "The plan adds 22 people, which takes the team to 36. The model's burn carries 6 of them."
    },
    {
     "lead": "The hires the model leaves out.",
     "refs": [
      "bu-2"
     ],
     "body": "The other 16 hires add $268,000 a month once all have started, by month 11. Payroll is usually the largest part of burn, so a plan the model does not pay for makes the runway look longer than it is."
    },
    {
     "lead": "Who owns each function.",
     "refs": [],
     "body": "The room holds a founder bio and a hiring plan, but no org chart naming who leads sales, product and finance today. That is the next thing to ask for."
    }
   ],
   "asks": [
    "Which of the 22 hires the round pays for first, and the milestone each one supports.",
    "An org chart or payroll list naming everyone counted today, with contractors marked.",
    "Founder vesting schedules and retention terms for key people."
   ],
   "chart": {
    "kind": "bars",
    "unit": "count",
    "barmode": "stack",
    "x": [
     "Today",
     "After the hiring plan"
    ],
    "series": [
     {
      "name": "Team today",
      "y": [
       14,
       14
      ],
      "style": "plan"
     },
     {
      "name": "Hires the model's burn carries",
      "y": [
       0,
       6
      ],
      "style": "good"
     },
     {
      "name": "Hires outside the model's burn",
      "y": [
       0,
       16
      ],
      "style": "bad",
      "text": [
       "",
       "36 people"
      ],
      "textposition": "outside"
     }
    ],
    "label": "Team of 14 today. The hiring plan adds 22, to 36. The model's burn carries 6 of them and leaves 16 out."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "02_financials/financial_model.xlsx",
    "06_team/hiring_plan.csv"
   ]
  },
  {
   "key": "piece-the_pitch_itself",
   "piece": "the_pitch_itself",
   "title": "The pitch itself",
   "knowledge": "knowledge/the_pitch_itself.md",
   "paras": [
    {
     "lead": "The ask.",
     "refs": [
      "pi-1"
     ],
     "body": "A $25.0M Series A at $150.0M pre-money, so $175.0M post. The new money buys 14.29% of the company."
    },
    {
     "lead": "The price against revenue.",
     "refs": [
      "tr-1",
      "tr-3"
     ],
     "body": "The post-money is 62.5 times the deck's ARR and 71.7 times ARR rebuilt from the customer file. The pilot is the difference. Tricorder sets no line for the multiple. The partner weighs it against comparable rounds."
    },
    {
     "lead": "What the round buys.",
     "refs": [
      "pi-1",
      "bu-2"
     ],
     "body": "With the round in the bank and every planned hire paid, the cash lasts 47.3 months. Without the round, 24.1. YC advises raising enough to reach the next fundable milestone, usually 12 to 18 months out. 47.3 months is past that."
    },
    {
     "lead": "A pitch claim that holds.",
     "refs": [
      "pi-2"
     ],
     "body": "The deck says 13% of the YC batch use Ploy. The workspace file tags 13.5%, and the launch post agrees."
    }
   ],
   "asks": [
    "The use of funds by line, each tied to a dated milestone and to the hiring plan.",
    "The pro forma cap table after the round, with the option pool.",
    "Which ARR the $150.0M pre-money was set on: the deck's, or the one without the pilot."
   ],
   "chart": {
    "kind": "bars",
    "unit": "multiple",
    "x": [
     "Deck ARR, $2.8M",
     "Model ARR, $2,802,000",
     "Rebuilt ARR, $2,442,000"
    ],
    "series": [
     {
      "name": "Post-money as a multiple of ARR",
      "y": [
       62.5,
       62.46,
       71.66
      ],
      "styles": [
       "plan",
       "plan",
       "mixed"
      ],
      "text": [
       "62.5x",
       "62.5x",
       "71.7x"
      ]
     }
    ],
    "label": "Post-money of $175.0M as a multiple of ARR: Deck ARR, $2.8M 62.5x, Model ARR, $2,802,000 62.5x, Rebuilt ARR, $2,442,000 71.7x."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "02_financials/financial_model.xlsx",
    "03_metrics/customer_mrr_by_month.csv",
    "03_metrics/workspaces_by_plan.csv",
    "04_customers/order_form_northwind_analytics.pdf",
    "06_team/hiring_plan.csv"
   ]
  },
  {
   "key": "piece-legal_and_cap_table",
   "piece": "legal_and_cap_table",
   "title": "Legal and cap table",
   "knowledge": "knowledge/legal_and_cap_table.md",
   "paras": [
    {
     "lead": "The cap table matches the public record.",
     "refs": [
      "lc-1"
     ],
     "body": "The seed total on the cap table, $26,571,989, is the amount sold on the SEC Form D, to the dollar. A filing the company does not control agreeing with its own file is a small green flag."
    },
    {
     "lead": "The SAFEs and the holders agree too.",
     "refs": [
      "lc-2",
      "lc-3"
     ],
     "body": "$11,572,000 of SAFEs converted into the seed, the figure the Form D gives. The cap table lists 11 seed holders, the Form D's count."
    },
    {
     "lead": "No claims stated.",
     "refs": [
      "lc-4"
     ],
     "body": "The claims statement says there are no lawsuits, threatened claims or regulator contact. It is the company's own statement. A litigation and lien search would test it."
    },
    {
     "lead": "The pro forma is missing.",
     "refs": [],
     "body": "The room holds no pro forma cap table after the Series A. Without it, the ownership after the round cannot be rebuilt from its terms."
    }
   ],
   "asks": [
    "The pro forma cap table after the Series A, with SAFE conversions and the option pool.",
    "Signed copies of the seed stock purchase agreements, so each row ties to a paper.",
    "Founder vesting schedules and any side letters."
   ],
   "chart": {
    "kind": "bars",
    "unit": "usd",
    "barmode": "group",
    "x": [
     "Seed total sold",
     "From SAFEs that converted"
    ],
    "series": [
     {
      "name": "Cap table",
      "y": [
       26571989.0,
       11572000.0
      ],
      "style": "good",
      "text": [
       "$26.57M",
       "$11.57M"
      ]
     },
     {
      "name": "SEC Form D",
      "y": [
       26571989.0,
       11572000.0
      ],
      "style": "plan",
      "text": [
       "$26.57M",
       "$11.57M"
      ]
     }
    ],
    "label": "The cap table against the SEC Form D: $26,571,989 sold and $11,572,000 from SAFEs in both."
   },
   "needs": [
    "05_legal/cap_table.xlsx",
    "05_legal/claims_statement.pdf",
    "05_legal/safe_conversion_schedule.pdf"
   ]
  }
 ],
 "sazabi": [
  {
   "key": "piece-retention",
   "piece": "retention",
   "title": "Retention",
   "knowledge": "knowledge/retention.md",
   "paras": [
    {
     "lead": "What the room shows.",
     "refs": [
      "re-1"
     ],
     "body": "The 18 teams paying in 2026-06 paid $4,650 a month then and $5,700 in 2026-09. Net revenue retention is 122.6%. The deck says above 120%, and the customer file bears it out."
    },
    {
     "lead": "Revenue held better than customers.",
     "refs": [
      "re-1",
      "re-3"
     ],
     "body": "17 of the 18 teams still pay: 94.4% of customers. Revenue retention above customer retention means the teams that stay moved to bigger plans, which is what an investor wants to see."
    },
    {
     "lead": "Gross retention is not shown.",
     "refs": [
      "re-2"
     ],
     "body": "Net retention blends upgrades with losses. The room gives no gross retention, so the loss on its own is not visible. The customer file can produce it team by team."
    },
    {
     "lead": "Three months is a short record.",
     "refs": [
      "re-3"
     ],
     "body": "1 team left, which works out to 1.9% a month. With 18 teams, one more loss moves every percentage a long way. A 12-month figure needs data to 2027-06."
    }
   ],
   "asks": [
    "Gross revenue retention for the 2026-06 cohort, team by team.",
    "The 2026-07 and 2026-08 cohorts on the same basis.",
    "Why the team that left did so."
   ],
   "chart": {
    "kind": "bars",
    "unit": "usd",
    "barmode": "group",
    "x": [
     "Hobby",
     "Startup",
     "Growth"
    ],
    "x_title": "Plan in 2026-06",
    "series": [
     {
      "name": "2026-06: 18 teams",
      "y": [
       450.0,
       1200.0,
       3000.0
      ],
      "style": "plan"
     },
     {
      "name": "2026-09: 17 of them still paying",
      "y": [
       300.0,
       1400.0,
       4000.0
      ],
      "style": "good"
     }
    ],
    "label": "Monthly revenue from the teams paying in 2026-06, by the plan they started on: $4,650 then and $5,700 in 2026-09, net revenue retention of 122.6%."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "03_metrics/customer_mrr_by_month.csv"
   ]
  },
  {
   "key": "piece-unit_economics",
   "piece": "unit_economics",
   "title": "Unit economics",
   "knowledge": "knowledge/unit_economics.md",
   "paras": [
    {
     "lead": "What it costs to serve.",
     "refs": [
      "ue-2"
     ],
     "body": "September revenue in the model was $18,380. Cost of revenue is $4,000 of cloud after credits and $2,480 of model inference, for a gross margin of 64.7%."
    },
    {
     "lead": "Credits pay part of the bill.",
     "refs": [
      "ue-3",
      "ue-1"
     ],
     "body": "Cloud credits covered $2,900 of the $6,900 cloud bill. Credits run out, so the margin to plan on prices the cloud in full: 49.0%. The deck says 65%."
    },
    {
     "lead": "On recurring revenue alone.",
     "refs": [
      "tr-3"
     ],
     "body": "September revenue includes a one-time backfill. On recurring revenue of $14,580, with the cloud at full price, gross margin is 35.7%: below a16z's 50 to 60% for AI companies."
    },
    {
     "lead": "Prices check out. Acquisition cost is missing.",
     "refs": [
      "ue-4"
     ],
     "body": "The model's prices match the public pricing page. The room holds no acquisition cost or payback, so what a team earns against what it costs to win cannot be checked."
    }
   ],
   "asks": [
    "Cloud invoices for July to September, with the credit balance and the date the credits expire.",
    "What it costs to serve the free design partners, and where that cost sits.",
    "Acquisition cost and payback, with payback measured on gross profit."
   ],
   "chart": {
    "kind": "bars",
    "unit": "percent",
    "barmode": "stack",
    "x": [
     "The model's books",
     "At full cloud price"
    ],
    "range": [
     0,
     100
    ],
    "series": [
     {
      "name": "Gross profit",
      "y": [
       64.74,
       48.97
      ],
      "style": "good",
      "text": [
       "64.7% margin",
       "49.0% margin"
      ],
      "textposition": "inside",
      "textanchor": "start"
     },
     {
      "name": "Cloud paid in cash, and inference",
      "y": [
       35.26,
       35.26
      ],
      "style": "plan"
     },
     {
      "name": "Cloud paid by credits",
      "y": [
       0.0,
       15.78
      ],
      "style": "bad"
     }
    ],
    "lines": [
     {
      "y": 65,
      "label": "Bessemer: cloud software averages 65 to 70%",
      "style": "accent",
      "right": true
     },
     {
      "y": 55,
      "label": "a16z: AI companies often 50 to 60%",
      "style": "plan",
      "right": true,
      "below": true
     }
    ],
    "label": "Gross margin, each bar 100% of September revenue of $18,380: 64.7% on the model's books, 49.0% with the cloud bill at full price. Bessemer's cloud average is 65 to 70%."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "02_financials/financial_model.xlsx",
    "02_financials/monthly_statements.xlsx",
    "03_metrics/cloud_costs_by_month.csv",
    "03_metrics/customer_mrr_by_month.csv"
   ]
  },
  {
   "key": "piece-customers",
   "piece": "customers",
   "title": "Customers",
   "knowledge": "knowledge/customers.md",
   "paras": [
    {
     "lead": "One customer is a large share.",
     "refs": [
      "cu-1"
     ],
     "body": "Corvane Systems pays $4,500 a month: 30.9% of recurring revenue. Its order form agrees with the customer file. That is above the 20% many investors use as a threshold."
    },
    {
     "lead": "Many small plans behind it.",
     "refs": [
      "cu-2"
     ],
     "body": "31 teams on plans bring $8,900 a month together, $287 each on average."
    },
    {
     "lead": "Paying, not just signed up.",
     "refs": [
      "cu-2",
      "tr-4"
     ],
     "body": "32 teams pay out of 118 workspaces. 21 of the 50 design partners pay. The deck says all 50 do. Design partners show interest. The ones that pay are customers."
    },
    {
     "lead": "Usage beyond the plan.",
     "refs": [
      "tr-3"
     ],
     "body": "Recurring usage over plan adds $1,180 a month, 8.1% of recurring revenue. It moves with how much teams log, so it can fall as well as rise."
    }
   ],
   "asks": [
    "Corvane Systems's signed terms: length, notice period and renewal date.",
    "Which design partners are expected to pay, on which plan, and when.",
    "The top three customers' share of recurring revenue, month by month."
   ],
   "chart": {
    "kind": "bars",
    "unit": "percent",
    "orientation": "h",
    "x": [
     "Corvane Systems, the one contract",
     "Growth plans, 6 teams",
     "Startup plans, 11 teams",
     "Hobby plans, 14 teams",
     "Recurring usage over plan"
    ],
    "height": 300,
    "series": [
     {
      "name": "Share",
      "y": [
       30.86,
       41.15,
       15.09,
       4.8,
       8.09
      ],
      "styles": [
       "bad",
       "plan",
       "plan",
       "plan",
       "mixed"
      ],
      "text": [
       "30.9%",
       "41.2%",
       "15.1%",
       "4.8%",
       "8.1%"
      ]
     }
    ],
    "lines": [
     {
      "y": 20,
      "label": "20%: a common investor threshold",
      "style": "bad"
     }
    ],
    "label": "Share of recurring MRR of $14,580: Corvane Systems 30.9%, against a common 20% threshold."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "02_financials/monthly_statements.xlsx",
    "03_metrics/customer_mrr_by_month.csv",
    "03_metrics/workspaces_by_plan.csv"
   ]
  },
  {
   "key": "piece-market",
   "piece": "market",
   "title": "Market",
   "knowledge": "knowledge/market.md",
   "paras": [
    {
     "lead": "Count times price.",
     "refs": [
      "ma-1"
     ],
     "body": "The deck sizes the market at $1,440,000,000: 120,000 engineering teams at the Growth plan's $12,000 a year. No other file in the room states the count."
    },
    {
     "lead": "Which price.",
     "refs": [
      "ue-4",
      "cu-2",
      "tr-3"
     ],
     "body": "Growth is the top self-serve plan, so its price is a ceiling. The 32 paying teams bring $5,468 a year on average today. At that price the same count gives $656.1M."
    },
    {
     "lead": "How much is won so far.",
     "refs": [
      "tr-3"
     ],
     "body": "The deck's market is 8,230 times today's recurring revenue of $174,960 a year. A market that large rests on the count, so the count needs a source."
    },
    {
     "lead": "The count needs a source.",
     "refs": [],
     "body": "The room does not say where the count comes from, or what makes an engineering team a buyer. One company estimate is a starting point, not evidence."
    }
   ],
   "asks": [
    "Where the 120,000 engineering teams come from, and what a team has to look like to be in it.",
    "The market at the price paying teams pay today, by plan.",
    "Which segment the company wins first, and how many teams are in it."
   ],
   "chart": {
    "kind": "bars",
    "unit": "usd",
    "x": [
     "At the Growth list price, $12,000 a year",
     "At what a paying team pays today, $5,468 a year"
    ],
    "series": [
     {
      "name": "120,000 engineering teams",
      "y": [
       1440000000,
       656100000.0
      ],
      "styles": [
       "plan",
       "mixed"
      ],
      "text": [
       "$1.44B",
       "$656.1M"
      ]
     }
    ],
    "label": "Market size for the deck's 120,000 engineering teams: $1.44B at the Growth list price, $656.1M at what a paying team pays today."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "02_financials/financial_model.xlsx",
    "02_financials/monthly_statements.xlsx",
    "03_metrics/customer_mrr_by_month.csv",
    "03_metrics/workspaces_by_plan.csv"
   ]
  },
  {
   "key": "piece-team",
   "piece": "team",
   "title": "Team",
   "knowledge": "knowledge/team.md",
   "paras": [
    {
     "lead": "The team matches the public record.",
     "refs": [
      "te-1",
      "te-2"
     ],
     "body": "The model and the YC page say 10 people. The staff list and the launch post say 9 of them are engineers, 3 from Brex. Independent sources agreeing is a small green flag."
    },
    {
     "lead": "Almost everyone builds.",
     "refs": [
      "te-2"
     ],
     "body": "1 of the 10 works outside engineering. That is a fact to report, not a score. The question is who owns selling as the company moves from design partners to paying teams."
    },
    {
     "lead": "The hiring plan.",
     "refs": [
      "bu-2"
     ],
     "body": "The plan adds 6 people, to 16. The model's burn carries 4. The other 2 add $38,000 a month once they start, by month 6."
    }
   ],
   "asks": [
    "Which of the 6 hires the seed pays for first, and the milestone each one supports.",
    "Who owns sales today, and when the first sales hire starts.",
    "Founder vesting schedules and retention terms for the early Brex engineers."
   ],
   "chart": {
    "kind": "bars",
    "unit": "count",
    "barmode": "stack",
    "x": [
     "Today",
     "After the hiring plan"
    ],
    "series": [
     {
      "name": "Team today",
      "y": [
       10,
       10
      ],
      "style": "plan"
     },
     {
      "name": "Hires the model's burn carries",
      "y": [
       0,
       4
      ],
      "style": "good"
     },
     {
      "name": "Hires outside the model's burn",
      "y": [
       0,
       2
      ],
      "style": "bad",
      "text": [
       "",
       "16 people"
      ],
      "textposition": "outside"
     }
    ],
    "label": "Team of 10 today. The hiring plan adds 6, to 16. The model's burn carries 4 of them and leaves 2 out."
   },
   "needs": [
    "02_financials/financial_model.xlsx",
    "06_team/founder_bio_sherwood_callaway.pdf",
    "06_team/hiring_plan.csv"
   ]
  },
  {
   "key": "piece-the_pitch_itself",
   "piece": "the_pitch_itself",
   "title": "The pitch itself",
   "knowledge": "knowledge/the_pitch_itself.md",
   "paras": [
    {
     "lead": "The ask.",
     "refs": [
      "pi-1"
     ],
     "body": "An $8.0M seed on SAFEs at a $40.0M post-money cap. If it all converts at the cap, the seed owns 20.00%."
    },
    {
     "lead": "Called closed, partly unsigned.",
     "refs": [
      "pi-2",
      "lc-2"
     ],
     "body": "The deck calls the round closed. The SAFE schedule shows $5,250,000 signed and $2,750,000 of commitments with no signed SAFE: 34.4% of the round. A commitment is a promise until the paper is signed."
    },
    {
     "lead": "The price against revenue.",
     "refs": [
      "tr-3"
     ],
     "body": "The $40.0M cap is 229 times recurring ARR of $174,960. Tricorder sets no line for the multiple. At seed the price rests on more than revenue, and the partner weighs it against comparable rounds."
    },
    {
     "lead": "What the unsigned money changes.",
     "refs": [
      "bu-2",
      "pi-2"
     ],
     "body": "With every planned hire, the cash in the bank lasts 14.5 months. If the unsigned $2.75M comes in, 23.8. YC advises raising enough for the next fundable milestone, usually 12 to 18 months out. The signed money alone gives 14.5 months, inside that."
    }
   ],
   "asks": [
    "Who the unsigned commitments are, and when they sign.",
    "Signed copies of every SAFE, so the schedule ties to the papers.",
    "The use of funds by line, each tied to a dated milestone."
   ],
   "chart": {
    "kind": "bars",
    "unit": "usd",
    "barmode": "stack",
    "x": [
     "What the deck says",
     "What the SAFE schedule shows"
    ],
    "series": [
     {
      "name": "Called closed",
      "y": [
       8000000,
       0
      ],
      "style": "plan",
      "text": [
       "$8.0M",
       ""
      ]
     },
     {
      "name": "Signed SAFEs",
      "y": [
       0,
       5250000
      ],
      "style": "good",
      "text": [
       "",
       "$5.25M"
      ],
      "textposition": "inside"
     },
     {
      "name": "Commitments with no signed SAFE",
      "y": [
       0,
       2750000
      ],
      "style": "thin",
      "text": [
       "",
       "$2.75M unsigned"
      ]
     }
    ],
    "label": "The seed as the deck states it, $8.0M closed, and as the SAFE schedule shows it: $5.25M signed and $2.75M with no signed SAFE."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "02_financials/financial_model.xlsx",
    "02_financials/monthly_statements.xlsx",
    "03_metrics/customer_mrr_by_month.csv",
    "05_legal/cap_table.xlsx",
    "05_legal/safe_schedule.pdf",
    "06_team/hiring_plan.csv"
   ]
  },
  {
   "key": "piece-legal_and_cap_table",
   "piece": "legal_and_cap_table",
   "title": "Legal and cap table",
   "knowledge": "knowledge/legal_and_cap_table.md",
   "paras": [
    {
     "lead": "The cap table counts more than is signed.",
     "refs": [
      "lc-1",
      "lc-2"
     ],
     "body": "The cap table's seed total is $8,000,000, the amount in the company's post. The signed SAFEs add to $5,250,000 from 66 holders. The other $2,750,000 comes from 9 commitments with no signed SAFE. A row with no paper is a promise."
    },
    {
     "lead": "No Form D on file.",
     "refs": [
      "lc-3"
     ],
     "body": "The first SAFE was funded on 2026-02-17. A Form D is due 15 days after the first sale, so by 2026-03-04. EDGAR has 0 Form D filings for the company, and the room's as-of date is 210 days past the due date. A filing may sit under another legal name, so this is a question for the founder before it is a flag."
    },
    {
     "lead": "The round kept raising after it was announced.",
     "refs": [
      "lc-2",
      "pi-2"
     ],
     "body": "The press reported the company still raising on 2026-04-08. The company announced the seed on 2026-06-25, and SAFEs were still being signed until 2026-08-21. The deck calls the round closed."
    },
    {
     "lead": "No claims stated.",
     "refs": [
      "lc-4"
     ],
     "body": "The claims statement says there are no lawsuits, threatened claims or regulator contact. It is the company's own statement."
    }
   ],
   "asks": [
    "Was a Form D filed, and under what legal name? If not, why not?",
    "Who the 9 unsigned commitments are, and when they sign.",
    "Signed copies of every SAFE, and the pro forma cap table after the seed converts."
   ],
   "chart": {
    "kind": "timeline",
    "height": 340,
    "range": [
     "2026-01-20",
     "2026-10-28"
    ],
    "gap": {
     "from": "2026-03-04",
     "to": "2026-09-30",
     "label": "No Form D on EDGAR: 210 days past due",
     "mid": "2026-06-17"
    },
    "events": [
     {
      "date": "2026-02-17",
      "short": "First SAFE funded",
      "label": "First SAFE funded, 2026-02-17",
      "style": "accent"
     },
     {
      "date": "2026-03-04",
      "short": "Form D due",
      "label": "Form D due, 15 days after the first sale",
      "style": "bad"
     },
     {
      "date": "2026-04-08",
      "short": "Press: still raising",
      "label": "The press reports the company still raising, 2026-04-08",
      "style": "bad"
     },
     {
      "date": "2026-06-25",
      "short": "Company post: seed raised",
      "label": "The company's post announces the seed, 2026-06-25",
      "style": "plan"
     },
     {
      "date": "2026-08-21",
      "short": "Last SAFE signed",
      "label": "Last SAFE signed, 2026-08-21",
      "style": "plan"
     },
     {
      "date": "2026-09-30",
      "short": "Room as of",
      "label": "The room's as-of date. EDGAR has 0 Form D filings",
      "style": "bad"
     }
    ],
    "label": "The seed's dates: first SAFE funded 2026-02-17, Form D due 2026-03-04, press says still raising 2026-04-08, company post 2026-06-25, last SAFE signed 2026-08-21. EDGAR has 0 Form D filings as of 2026-09-30."
   },
   "needs": [
    "01_pitch/pitch_deck.pdf",
    "05_legal/cap_table.xlsx",
    "05_legal/claims_statement.pdf",
    "05_legal/safe_schedule.pdf"
   ]
  }
 ]
};
