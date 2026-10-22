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
    S -->|out/room/scan.json| M[scans/memo<br/>quote check, link,<br/>pieces, flags, asks]
    M -->|out/room/readout.json| SV[server/app.py]
    SV --> P[readout/ page]
    P -->|one-sentence steer| SV
    SV -->|rerun the piece| S
    M --> E[eval/score.py<br/>against the answer key]
```

Every number on the right side was computed by a script on the left. The model reads words and quotes them; the quote checker finds every quote again before it reaches the page.
