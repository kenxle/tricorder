# Interface example: claim support

Everything in the JSON below was printed by a real run, not typed:

```sh
python3 docs/features/20261023.06_claim_support/spike/interface_example.py <scratch_out_dir>
```

The script runs the commands a user runs on `hollis_voice` and `brasswick` (`python3 -m scans.redflags`, `python3 -m scans.claims`, `python3 -m scans.memo`, then `python3 -m scans.memo.claim_support`), each with `TRICORDER_OUT_DIR` set to a scratch folder, and prints parts of the resulting `readout.json`. Run on 2026-10-23 at revision `727ff5b`. Both rooms are synthetic.

## What a consumer reads

The claims scan writes an ordinary `ScanResult` (`out/<room>/claims.json`):

- **One `Claim` per pitch figure,** with `scan` `claims`, `check.name` `claim_support` (or a planted entry's own check name for a spoken figure the deck contradicts: `spoken_arr_vs_claims_page`, `spoken_number_vs_claims_page`), `confidence` `computed`, and a text that starts with its label: `Supported:`, `Contradicted:` or `Unsupported:`. The first source is always the pitch itself (the slide, or the script line); the rest are the documents that agree or disagree. Severity is `flag` for contradicted and `info` otherwise.
- **The "claims table" Panel:** one row per claim, the columns below. The `claim id` column joins a row to its Claim.
- **The "claims table counts" Panel:** the label counts, where the figures came from, and whether the memo step has relabelled the table.
- **The "claims not counted" Panel:** figures on a worked-example slide (Brasswick has six), listed but not labelled.
- **One `Gap` per unsupported kind,** naming the document to ask for, with its checklist id in `would_need`.

After the merge, `scans.memo.claim_support.apply` relabels a supported or unsupported row that another scan has flagged, adds the flag to `conflicts_with`, and adds the flag's sources outside the pitch. The Brasswick example at the end shows one.

## The JSON

```json
{
  "claims_table_columns": [
    "claim id",
    "label",
    "where",
    "quote",
    "kind",
    "stated",
    "normalised",
    "spoken",
    "agrees",
    "disagrees",
    "should be backed by",
    "ask"
  ],
  "hollis_voice": {
    "supported": {
      "row": {
        "claim id": "claims-028",
        "label": "supported",
        "where": "slide 8; repeated at slide 14, claims page row (cites slide 8): 'Market size (company estimate) $252,000,000 8'",
        "quote": "At about $9,000 a year per clinic, that is a market near $252,000,000 (company estimate).",
        "kind": "market size",
        "stated": "near $252,000,000",
        "normalised": "market size: 252,000,000 USD",
        "spoken": "",
        "agrees": "financial model (MARKET_TAM_USD): 252,000,000",
        "disagrees": "",
        "should be backed by": "financial model (C19)",
        "ask": ""
      },
      "claim": {
        "id": "claims-028",
        "scan": "claims",
        "text": "Supported: The deck (slide 8) gives market size as near $252,000,000. Outside the pitch, financial model (MARKET_TAM_USD, 252,000,000) agrees.",
        "severity": "info",
        "confidence": "computed",
        "check": {
          "kind": "script",
          "name": "claim_support",
          "model": null
        },
        "value": {
          "number": 252000000.0,
          "unit": "USD",
          "label": "tam",
          "period": null
        },
        "sources": [
          {
            "kind": "file",
            "uri": "01_overview/pitch_deck.pdf",
            "locator": "slide 8",
            "start_s": null,
            "end_s": null,
            "quote": "At about $9,000 a year per clinic, that is a market near $252,000,000 (company\nestimate).",
            "retrieved_at": null
          },
          {
            "kind": "file",
            "uri": "01_overview/pitch_deck.pdf",
            "locator": "slide 14",
            "start_s": null,
            "end_s": null,
            "quote": "Market size (company estimate) $252,000,000 8",
            "retrieved_at": null
          },
          {
            "kind": "file",
            "uri": "02_financials/financial_model.xlsx",
            "locator": "MARKET_TAM_USD",
            "start_s": null,
            "end_s": null,
            "quote": "252000000",
            "retrieved_at": null
          }
        ],
        "conflicts_with": [],
        "corroborated_by": []
      }
    },
    "contradicted": {
      "row": {
        "claim id": "claims-056",
        "label": "contradicted",
        "where": "script line 15 (beat 0:35)",
        "quote": "Today we're at about three million dollars in annual recurring revenue.",
        "kind": "ARR",
        "stated": "about three million dollars",
        "normalised": "ARR: 3,000,000 USD a year, 2026-09",
        "spoken": "spoken, rounded (about), from the script",
        "agrees": "",
        "disagrees": "financial model (ARR_TOTAL): 2,240,868; metrics export (row 22): 2,240,868; revenue by customer (row 1984): 2,060,868; slide 3: $2.5M (same pitch)",
        "should be backed by": "financial model (C19), metrics export (C02), revenue by customer (C03)",
        "ask": "Please walk us from the source data to about three million dollars (script line 15 (beat 0:35)) (C71)."
      },
      "claim": {
        "id": "claims-056",
        "scan": "claims",
        "text": "Contradicted: The pitch video script (line 15, beat 0:35; the video is not recorded yet) gives ARR as about three million dollars, but financial model (ARR_TOTAL) says 2,240,868, 25.3% lower; metrics export (row 22) says 2,240,868, 25.3% lower; revenue by customer (row 1984) says 2,060,868, 31.3% lower; the deck (slide 3) says $2.5M.",
        "severity": "flag",
        "confidence": "computed",
        "check": {
          "kind": "script",
          "name": "spoken_arr_vs_claims_page",
          "model": null
        },
        "value": {
          "number": 3000000.0,
          "unit": "USD_per_year",
          "label": "arr",
          "period": "2026-09"
        },
        "sources": [
          {
            "kind": "file",
            "uri": "01_overview/pitch_video_script.md",
            "locator": "line 15",
            "start_s": null,
            "end_s": null,
            "quote": "Today we're at about three million dollars in annual recurring revenue.",
            "retrieved_at": null
          },
          {
            "kind": "file",
            "uri": "02_financials/financial_model.xlsx",
            "locator": "ARR_TOTAL",
            "start_s": null,
            "end_s": null,
            "quote": "2240868",
            "retrieved_at": null
          },
          {
            "kind": "file",
            "uri": "03_metrics/monthly_metrics.csv",
            "locator": "row 22",
            "start_s": null,
            "end_s": null,
            "quote": "2026-09,186739,2240868,212,357,72149",
            "retrieved_at": null
          },
          {
            "kind": "file",
            "uri": "03_metrics/customer_mrr_by_month.csv",
            "locator": "row 1984",
            "start_s": null,
            "end_s": null,
            "quote": "2026-09,C0087,Cedar & Pine Animal Hospitals,40,Group,Subscription,36000,0,36000",
            "retrieved_at": null
          },
          {
            "kind": "file",
            "uri": "01_overview/pitch_deck.pdf",
            "locator": "slide 3",
            "start_s": null,
            "end_s": null,
            "quote": "$2.5M\nARR",
            "retrieved_at": null
          }
        ],
        "conflicts_with": [],
        "corroborated_by": []
      }
    },
    "unsupported": {
      "row": {
        "claim id": "claims-018",
        "label": "unsupported",
        "where": "slide 7",
        "quote": "$349 $649 $1,099 Custom a month a month a month per agreement",
        "kind": "list price",
        "stated": "$349",
        "normalised": "list price: 349 USD a month",
        "spoken": "",
        "agrees": "",
        "disagrees": "",
        "should be backed by": "customer contracts (C34)",
        "ask": "Please send signed order forms that show the list price (C34), to back: $349."
      },
      "claim": {
        "id": "claims-018",
        "scan": "claims",
        "text": "Unsupported: The deck (slide 7) gives list price as $349. No document outside the pitch states it.",
        "severity": "info",
        "confidence": "computed",
        "check": {
          "kind": "script",
          "name": "claim_support",
          "model": null
        },
        "value": {
          "number": 349.0,
          "unit": "USD_per_month",
          "label": "price",
          "period": null
        },
        "sources": [
          {
            "kind": "file",
            "uri": "01_overview/pitch_deck.pdf",
            "locator": "slide 7",
            "start_s": null,
            "end_s": null,
            "quote": "$349 $649 $1,099 Custom\na month a month a month per agreement",
            "retrieved_at": null
          }
        ],
        "conflicts_with": [],
        "corroborated_by": []
      }
    }
  },
  "hollis_voice_counts": [
    [
      "claims",
      "64"
    ],
    [
      "supported",
      "39"
    ],
    [
      "contradicted",
      "8"
    ],
    [
      "unsupported",
      "17"
    ],
    [
      "from deck",
      "54"
    ],
    [
      "from script",
      "10"
    ],
    [
      "as of",
      "2026-09-30"
    ],
    [
      "video source",
      "script"
    ],
    [
      "not counted (examples)",
      "0"
    ],
    [
      "relabelled by the memo step",
      "yes"
    ]
  ],
  "hollis_voice_gap": {
    "what": "Not in the room: signed order forms that show the list price, to back 3 pitch claims on list price (slide 5: $349; slide 7: $349; slide 7: $1,099)",
    "why": "not stated in any document outside the pitch",
    "would_need": "signed order forms that show the list price (C34)",
    "piece": "unit_economics"
  },
  "brasswick_relabelled_by_memo_step": {
    "row": {
      "claim id": "claims-004",
      "label": "contradicted",
      "where": "slide 4; repeated at slide 12, claims page row (cites slide 4): 'Monthly revenue chart 2026-01 to 2026-09 4'",
      "quote": "Monthly revenue, January 2026 to September 2026",
      "kind": "chart months",
      "stated": "January 2026 to September 2026",
      "normalised": "chart months: 2026-01..2026-09",
      "spoken": "",
      "agrees": "metrics export (row 10): 2026-01..2026-09; metrics export (row 18): 2026-01..2026-09",
      "disagrees": "redflags deck_history_vs_metrics (redflags-010): Shows part of the history: the revenue chart on slide 4 starts at 2026-01, 8 months after the first revenue month in the books (2025-05); the months left out, 2025-05 to 2025-12, hold a peak of $84,090 in 2025-09; revenue then fell 28.2% to $60,400 in the chart's first month; revenue fell month on month in 2025-10, 2025-12.",
      "should be backed by": "metrics export (C02)",
      "ask": "Please walk us from the source data to January 2026 to September 2026 (slide 4) (C71)."
    },
    "claim": {
      "id": "claims-004",
      "scan": "claims",
      "text": "Contradicted: The deck (slide 4) gives chart months as January 2026 to September 2026, but the redflags scan's deck_history_vs_metrics check flags it: Shows part of the history: the revenue chart on slide 4 starts at 2026-01, 8 months after the first revenue month in the books (2025-05); the months left out, 2025-05 to 2025-12, hold a peak of $84,090 in 2025-09; revenue then fell 28.2% to $60,400 in the chart's first month; revenue fell month on month in 2025-10, 2025-12.",
      "severity": "flag",
      "confidence": "computed",
      "check": {
        "kind": "script",
        "name": "claim_support",
        "model": null
      },
      "value": null,
      "sources": [
        {
          "kind": "file",
          "uri": "01_overview/pitch_deck.pdf",
          "locator": "slide 4",
          "start_s": null,
          "end_s": null,
          "quote": "Monthly revenue, January 2026 to September 2026",
          "retrieved_at": null
        },
        {
          "kind": "file",
          "uri": "02_financials/financial_model.xlsx",
          "locator": "P&L!C9",
          "start_s": null,
          "end_s": null,
          "quote": "16625.0",
          "retrieved_at": "2026-10-23"
        },
        {
          "kind": "file",
          "uri": "02_financials/financial_model.xlsx",
          "locator": "P&L!G9",
          "start_s": null,
          "end_s": null,
          "quote": "84090.2",
          "retrieved_at": "2026-10-23"
        },
        {
          "kind": "file",
          "uri": "02_financials/financial_model.xlsx",
          "locator": "P&L!K9",
          "start_s": null,
          "end_s": null,
          "quote": "60399.89",
          "retrieved_at": "2026-10-23"
        }
      ],
      "conflicts_with": [
        "redflags-010"
      ],
      "corroborated_by": []
    }
  }
}
```

## Reading the example

- **Supported** (`claims-028`): Hollis slide 8's market size of $252,000,000. The claims page repeats it (a repeat, same voice, listed in `where` and as a second source), and the financial model's named cell `MARKET_TAM_USD` agrees. This is green flag GF2.
- **Contradicted** (`claims-056`): the script's "about three million dollars". The figure is marked spoken, rounded (about), from the script. The model, the metrics export and the revenue file all disagree, and so does the deck's own $2.5M, which is shown with "(same pitch)" because it is the founder's voice, not a second source. The check name is the one planted entry PF2b uses, so the answer key credits it.
- **Unsupported** (`claims-018`): a list price on slide 7. Nothing outside the pitch states it, so the row's ask line names signed order forms (checklist C34), and the gap groups every list-price figure into one ask.
- **Relabelled by the memo step** (Brasswick `claims-004`): the claims scan found the chart's months in the metrics export, so it read supported. The red-flag engine's `deck_history_vs_metrics` check flags the same chart for starting after a fall. The memo step makes it contradicted, keeps both readings in `agrees` and `disagrees`, and cites the P&L cells the flag cites.
