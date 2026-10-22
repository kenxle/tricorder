"""Scan 1, the red-flag engine (FRAMEWORKS.md, Scan 1).

Scripts decide that a number is wrong; a model only reads clauses. Each
FRAMEWORKS entry is one module here with one function:

    def check(room: Path, ids: Ids) -> tuple[list[Claim], list[Gap]]

and is listed in scan.CHECKS. Deck against the books lives in
deck_vs_books.py, accounting mislabels (1.12) in mislabels.py, contract terms
(1.13) in contract_terms.py.
"""
