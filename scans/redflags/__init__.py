"""Scan 1, the red-flag engine (FRAMEWORKS.md, Scan 1).

Scripts decide that a number is wrong; a model only reads clauses. Each
FRAMEWORKS entry is one module here with one function:

    def check(room: Path, ids: Ids) -> tuple[list[Claim], list[Gap]]

or a third element, list[Panel], for an entry's own tables (1.12's checks and lines).

and is listed in scan.CHECKS. Deck against the books lives in
deck_vs_books.py, accounting mislabels (1.12) in mislabels.py, contract terms
(1.13) in contract_terms.py (Saturday: the model reading, checks 2 and 5) and
contract_terms_full.py (checks 1, 3, 4 and 6 and the clause notes). Both read the
contracts through contract_reader.py, once.
"""
