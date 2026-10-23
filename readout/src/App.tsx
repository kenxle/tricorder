import { useEffect, useMemo, useState } from "react";
import type { Claim, Piece, Readout, Source } from "../../schema/ts/claim";
import { buildReadout, getReadout, getRooms, getSourceText, type RoomInfo } from "./api";
import { PIECE_LABEL, VERDICT_LABEL } from "./labels";
import { FounderRequests } from "./FounderRequests";

// The readout page skeleton: top flags, the overview, a piece's claims, a
// claim's source, gaps, the could-not-verify box and the ask list, in that
// order (ROADMAP.md, readout-page). Styling waits on STYLE_GUIDE.md.

export function App() {
  const [rooms, setRooms] = useState<RoomInfo[]>([]);
  const [room, setRoom] = useState<string>("");
  const [readout, setReadout] = useState<Readout | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    getRooms()
      .then((r) => {
        setRooms(r);
        setRoom((cur) => cur || r.find((x) => x.id === "hollis_voice")?.id || r[0]?.id || "");
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  useEffect(() => {
    if (!room) return;
    setReadout(null);
    setError("");
    getReadout(room).then(setReadout).catch(() => setError("No readout for this room yet."));
  }, [room]);

  return (
    <main className="page">
      <header className="masthead">
        <h1>Tricorder</h1>
        <select value={room} onChange={(e) => setRoom(e.target.value)} aria-label="Room">
          {rooms.map((r) => (
            <option key={r.id} value={r.id}>
              {r.id}
            </option>
          ))}
        </select>
        <button onClick={() => buildReadout(room).then(setReadout, (e: Error) => setError(e.message))}>Build readout</button>
      </header>
      {error && <p className="note">{error}</p>}
      {readout && <ReadoutView readout={readout} />}
    </main>
  );
}

function ReadoutView({ readout }: { readout: Readout }) {
  const claims = useMemo(() => new Map(readout.claims.map((c) => [c.id, c])), [readout]);
  const [order, setOrder] = useState<Piece[]>(readout.pieces);
  const [open, setOpen] = useState<string | null>(null);
  useEffect(() => setOrder(readout.pieces), [readout]);

  const move = (i: number, by: number) => {
    const next = [...order];
    const [p] = next.splice(i, 1);
    next.splice(Math.max(0, Math.min(next.length, i + by)), 0, p);
    setOrder(next);
  };

  const greens = readout.top_flags.filter((f) => f.kind === "green");
  const reds = readout.top_flags.filter((f) => f.kind === "red");

  return (
    <>
      {readout.synthetic_notice && <p className="banner">{readout.synthetic_notice}</p>}

      <section aria-label="Top flags">
        <h2>Top green and red flags</h2>
        {readout.top_flags.length === 0 && <p className="note">No flags yet.</p>}
        <ol className="flags">
          {[...greens, ...reds].map((f) => (
            <li key={`${f.kind}-${f.rank}`} className={`flag ${f.kind}`}>
              <button className="link" onClick={() => setOpen(f.piece)}>
                {f.text}
              </button>
            </li>
          ))}
        </ol>
      </section>

      <section aria-label="Overview">
        <h2>Overview</h2>
        {order.length === 0 && <p className="note">No piece verdicts yet. {readout.claims.length} claims from {readout.scans_run.join(", ") || "no scans"}.</p>}
        <ul className="pieces">
          {order.map((p, i) => (
            <li key={p.name} className={`piece ${p.verdict}`}>
              <div className="piece-row">
                <button className="link" onClick={() => setOpen(open === p.name ? null : p.name)}>
                  <strong>{PIECE_LABEL[p.name]}</strong> · {VERDICT_LABEL[p.verdict]}
                </button>
                <span className="counts">
                  {p.corroborating_sources} agree · {p.contradicting_sources} disagree
                </span>
                <button aria-label="Move up" onClick={() => move(i, -1)}>↑</button>
                <button aria-label="Move down" onClick={() => move(i, 1)}>↓</button>
              </div>
              <p className="reason">{p.reason}</p>
              {open === p.name && <ClaimList room={readout.room} claims={p.claim_ids.map((id) => claims.get(id)).filter((c): c is Claim => !!c)} all={claims} />}
            </li>
          ))}
        </ul>
      </section>

      {readout.gaps.length > 0 && (
        <section aria-label="Gaps">
          <h2>Gaps</h2>
          <ul>
            {readout.gaps.map((g, i) => (
              <li key={i}>
                {g.what} <span className="note">({g.why})</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {readout.unverified.length > 0 && (
        <section aria-label="Could not verify">
          <h2>Could not verify</h2>
          <ClaimList room={readout.room} claims={readout.unverified} all={claims} />
        </section>
      )}

      <section aria-label="Ask list">
        <h2>What to ask the founder for</h2>
        {readout.asks.length === 0 ? (
          <p className="note">Nothing to ask for.</p>
        ) : (
          <>
            <button onClick={() => navigator.clipboard.writeText(readout.asks.map((a) => `- ${a.what}`).join("\n"))}>Copy</button>
            <ul>
              {readout.asks.map((a, i) => (
                <li key={i}>
                  {a.what} <span className="note">{a.why}</span>
                </li>
              ))}
            </ul>
          </>
        )}
      </section>
      <FounderRequests room={readout.room} />
    </>
  );
}

function ClaimList({ room, claims, all }: { room: string; claims: Claim[]; all: Map<string, Claim> }) {
  return (
    <ul className="claims">
      {claims.map((c) => (
        <li key={c.id} className={`claim ${c.severity ?? ""}`}>
          {c.text}
          {c.sources.map((s, i) => (
            <SourceChip key={i} room={room} source={s} n={i + 1} />
          ))}
          {[...c.conflicts_with, ...c.corroborated_by].length > 0 && (
            <span className="note">
              {" "}
              {c.corroborated_by.length} agree, {c.conflicts_with.length} disagree
              {c.conflicts_with.map((id) => all.get(id)?.text).filter(Boolean).map((t) => ` · ${t}`)}
            </span>
          )}
        </li>
      ))}
    </ul>
  );
}

function SourceChip({ room, source, n }: { room: string; source: Source; n: number }) {
  const [text, setText] = useState<string | null>(null);
  return (
    <span className="source">
      <sup>
        <button
          className="link"
          title={`${source.uri} · ${source.locator}`}
          onClick={() => (text === null ? getSourceText(room, source).then((r) => setText(r.text), (e: Error) => setText(e.message)) : setText(null))}
        >
          [{n}]
        </button>
      </sup>
      {text !== null && (
        <span className="panel" role="note">
          <span className="note">
            {source.uri} · {source.locator}
          </span>
          <q>{source.quote}</q>
          <pre>{text.slice(0, 1200)}</pre>
        </span>
      )}
    </span>
  );
}
