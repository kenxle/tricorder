# The system

How a company's files become the page. Each box is a folder in the repo ([ARCHITECTURE.md](../ARCHITECTURE.md), "Folder layout").

```mermaid
flowchart LR
    subgraph In[Inputs]
        R[A data room<br/>data_room/ or rooms/]
        I[Inbox webhook<br/>inbox/]
        B[Bank, with consent<br/>Plaid]
        O[Outside sources<br/>clients/ and cache/]
    end
    I --> R
    R --> S
    B --> S
    O --> S
    subgraph S[Scans, one process each]
        S1[scans/redflags]
        S2[scans/comps]
        S3[scans/video]
        S4[other scans]
    end
    RD[schema/readers.py] -.-> S
    LLM[clients/llm.py<br/>words only] -.-> S
    S -->|out/room/scan.json| M[scans/memo<br/>quote check, link, claim support,<br/>pieces, flags, coverage, asks]
    M -->|out/room/readout.json| SV[server/app.py<br/>behind local_guard.py]
    SC[schema/claim.py] -->|schema.export| TS[packages/schema/ src types]
    TS -.->|@tricorder/schema| P[apps/web/ page]
    SV --> P
    P -->|one-sentence steer| ST[steering/]
    ST -->|rerun the piece| S
    P -->|ask list| FR[founder_requests/<br/>draft, never sent]
    FR -->|a reply's files<br/>into rooms/room_live| R
    SV --> MO[memo/<br/>memo.html and memo.pdf]
    ST -->|every revision| SD[store/<br/>store_data/ per fund]
    M --> E[eval/score.py<br/>against the answer key]
```

The founder's reply goes into a working copy of the room, so the waiting scans run again and the merge rebuilds the readout. A sample room in `data_room/` is never written.

Every number on the right side was computed by a script on the left. The model reads words and quotes them; the quote checker finds every quote again before it reaches the page.
