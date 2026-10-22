"""Every scan is a package here: scans/<name>/ with scan.py, __main__.py,
prompts/ and tests/. A scan exists once its scan.py does.

The contract (ARCHITECTURE.md, "The scan interface"):

    scan.py defines   NAME: str
                      NEEDS: tuple of input kinds (scans.base.INPUT_KINDS)
                      run(room_dir: Path) -> ScanResult
    __main__.py       from scans.base import main; main(scan)
    command           python -m scans.<name> <room_dir>
    output            out/<room>/<name>.json

No scan imports another scan, and no scan reads another scan's output. Only
the memo does.
"""

# Every scan the roadmap names, in the order bin/smoke runs them. The memo
# runs last and is not in this list. A name here with no scan.py yet is
# reported as missing, and the readout shows it as a gap.
SCANS: tuple[str, ...] = (
    "redflags",    # FRAMEWORKS Scan 1: red-flag engine, deck vs books, mislabels, contract terms
    "comps",       # Scan 2: public comps from EDGAR, recent private rounds
    "signals",     # Scan 3: market signals, from cache/
    "video",       # Scan 4: pitch video claims with timestamps, interesting moments
    "claims",      # The claims workflow: every deck slide and video sentence, checked for support
    "readings",    # Model readings: the pilot clause, the cohort note
    "model",       # Financial model rebuild and unit economics (1.9), the scenario engine's numbers
    "frameworks",  # Scan 5: lean canvas, JTBD, BMC, five forces, SWOT, bottom-up TAM
    "founders",    # Scan 6: founder-market fit, passion and commitment
    "presence",    # Scan 7: web, Hacker News, Product Hunt, app stores, saved Reddit pages
    "outside",     # The associate's ten tabs, opened automatically
    "bank",        # The bank check, through Plaid, with the founder's consent
)
