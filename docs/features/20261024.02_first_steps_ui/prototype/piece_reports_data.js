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
  }
 ]
};
