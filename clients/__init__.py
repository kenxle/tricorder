"""Every call that leaves the laptop goes through a client here.

`clients.llm` is the one door to the model. Outside sources (EDGAR, Akta,
Tavily, You.com, GitHub, Hacker News, the App Store, Crunchbase, Plaid) each
get one module, clients/<source>.py, with a mode switch read from
TRICORDER_<SOURCE>_MODE:

    off      the scan writes a gap that names the source
    sample   a recorded response in clients/samples/<source>/, no key, no network
    live     the real call; its answer is saved to cache/ with the time it was read

TRICORDER_OFFLINE=1 forces every source to sample or cache. Scans never call
a source directly; they call its client (ROADMAP.md, sponsor-adapters).
"""
