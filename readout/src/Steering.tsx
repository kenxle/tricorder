import { useEffect, useMemo, useState, type KeyboardEvent, type ReactNode } from "react";
import type { Claim, Panel, Piece, PieceRevision, Readout, Source } from "../../schema/ts/claim";
import { PIECE_LABEL, VERDICT_LABEL } from "./labels";
import { getClaimSource, getSteerable, postSteer } from "./steerApi";
import "./steering.css";

// The overview, steerable: one box on the overview, on every piece and on
// every line, opened by a click. One sentence and Enter, nothing else (ROADMAP
// "steering"). Revised lines appear where the operator typed, tagged with who
// steered and when; the diff under them opens with what happened. How the
// sentence was read and who rebuilt the verdicts stay in the JSON, not here.

const EXAMPLE = "For example: treat the pilot as non-recurring";
const OVERVIEW = "overview";

type Steered = { rev: PieceRevision; n: number; panel: Panel | undefined; typedOn: string };

function changesOf(readout: Readout, n: number): Panel | undefined {
  return readout.panels.find((p) => p.name === `steer ${n}: what changed`);
}

function cell(panel: Panel | undefined, change: string, col: number): string | null {
  const row = panel?.rows.find((r) => r[0] === change);
  return row ? row[col] : null;
}

function possessive(author: string | null): string {
  return author ? `${author}'s` : "The operator's";
}

function when(at: string): string {
  const d = new Date(at);
  return Number.isNaN(d.getTime()) ? at : d.toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

function who(rev: PieceRevision): string {
  return `${possessive(rev.steer.author)} steer, ${when(rev.steer.at)}`;
}

/** The panel a line's text names in quotes, such as the cohort rows a retention figure sums. */
function namedPanel(readout: Readout, claim: Claim): Panel | undefined {
  return readout.panels.find((p) => !p.name.startsWith("steer ") && claim.text.includes(`'${p.name}'`));
}

/** Loads the steerable readout for a room: App.tsx mounts this in place of its Overview section. */
export function SteerableSection({ room, onReadout }: { room: string; onReadout?: (r: Readout) => void }) {
  const [readout, setReadout] = useState<Readout | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    setReadout(null);
    setError("");
    getSteerable(room).then(setReadout, (e: Error) => setError(e.message));
  }, [room]);
  if (error) return <p className="note">{error}</p>;
  if (!readout) return <p className="note">Loading the overview.</p>;
  return (
    <SteerableOverview
      key={readout.room}
      readout={readout}
      onReadout={(r) => {
        setReadout(r);
        onReadout?.(r);
      }}
    />
  );
}

export function SteerableOverview({ readout, onReadout }: { readout: Readout; onReadout: (r: Readout) => void }) {
  const claims = useMemo(() => new Map([...readout.claims, ...readout.unverified].map((c) => [c.id, c])), [readout]);
  const steered: Steered[] = useMemo(
    () =>
      readout.revisions.map((rev, i) => {
        const panel = changesOf(readout, i + 1);
        return { rev, n: i + 1, panel, typedOn: cell(panel, "typed on", 3) ?? rev.steer.piece };
      }),
    [readout],
  );
  // Which steer added a line, and the check lines a scenario line replaced (shown as "before" in the diff).
  const addedBy = useMemo(() => {
    const m = new Map<string, Steered>();
    for (const s of steered) for (const id of s.rev.claims_added) m.set(id, s);
    return m;
  }, [steered]);
  const replaced = useMemo(() => new Set(steered.flatMap((s) => (s.panel?.rows ?? []).filter((r) => r[0] === "replaced").map((r) => r[1]))), [steered]);
  const pieceOf = useMemo(() => {
    const m = new Map<string, Piece["name"]>();
    for (const p of readout.pieces) for (const id of p.claim_ids) m.set(id, p.name);
    return m;
  }, [readout]);
  // A steer's own lines show under the place it was typed; a full-room read's lines show in their own pieces.
  const shownUnder = useMemo(() => {
    const m = new Map<string, string[]>();
    for (const s of steered) {
      if (s.typedOn === OVERVIEW) continue;
      m.set(`${s.n}`, s.rev.claims_added.filter((id) => pieceOf.get(id) === s.typedOn && claims.get(id)?.scan === "steering"));
    }
    return m;
  }, [steered, pieceOf, claims]);
  const underASteer = useMemo(() => new Set([...shownUnder.values()].flat()), [shownUnder]);
  const switched = steered.find((s) => cell(s.panel, "source", 3));

  const [order, setOrder] = useState<Piece[]>(readout.pieces);
  useEffect(() => setOrder(readout.pieces), [readout]);
  const [open, setOpen] = useState<Set<string>>(() => new Set(readout.pieces.filter((p) => p.verdict === "looking_weak").map((p) => p.name)));
  const [box, setBox] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string>("");
  const first = readout.revisions.length === 0;

  const send = (piece: string, claimId: string | null, sentence: string) => {
    const where = `${piece}:${claimId ?? ""}`;
    setBusy(where);
    setError("");
    postSteer(readout.room, { piece, sentence, claim_id: claimId })
      .then((r) => {
        setBox(null);
        if (piece !== OVERVIEW) setOpen((o) => new Set(o).add(piece));
        onReadout(r.readout);
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setBusy(null));
  };

  const toggle = (name: string) =>
    setOpen((o) => {
      const next = new Set(o);
      if (next.has(name)) next.delete(name);
      else next.add(name);
      return next;
    });
  const move = (i: number, by: number) => {
    const next = [...order];
    const [p] = next.splice(i, 1);
    next.splice(Math.max(0, Math.min(next.length, i + by)), 0, p);
    setOrder(next);
  };

  // A steer typed on a check line that its scenario line replaced shows with the piece, where the line was.
  const lineOf = (s: Steered) => (s.rev.steer.claim_id && !replaced.has(s.rev.steer.claim_id) ? s.rev.steer.claim_id : null);
  const steersOn = (typedOn: string, claimId: string | null) => steered.filter((s) => s.typedOn === typedOn && lineOf(s) === claimId);

  const line = (c: Claim, piece: string) => {
    const where = `${piece}:${c.id}`;
    return (
      <LineWithSteers
        key={c.id}
        claim={c}
        piece={piece}
        boxOpen={box === where}
        busy={busy === where}
        first={first}
        onOpen={() => setBox(where)}
        onClose={() => setBox(null)}
        onSend={(s) => send(piece, c.id, s)}
        ctx={ctx}
      />
    );
  };
  const ctx: Ctx = { readout, claims, addedBy, shownUnder, steersOn, line };

  return (
    <section aria-label="Overview">
      <div className="overview-head">
        <h2>Overview</h2>
        <button onClick={() => setBox(`${OVERVIEW}:`)}>Steer the overview</button>
      </div>
      {switched && (
        <p className="banner switch" role="status">
          Every piece reads {cell(switched.panel, "source", 3)}, the full room, instead of {cell(switched.panel, "source", 2)}. {who(switched.rev)}: "
          {switched.rev.steer.instruction}".
        </p>
      )}
      {box === `${OVERVIEW}:` && (
        <SteerBox busy={busy === `${OVERVIEW}:`} first={first} hint="On the overview, ask to read more: read the full room" onSend={(s) => send(OVERVIEW, null, s)} onClose={() => setBox(null)} />
      )}
      {steersOn(OVERVIEW, null).map((s) => (
        <Diff key={s.n} s={s} ctx={ctx} />
      ))}
      {error && (
        <p className="note" role="alert">
          {error}
        </p>
      )}
      <ul className="pieces">
        {order.map((p, i) => (
          <li key={p.name} className={`piece ${p.verdict}`} data-piece={p.name}>
            <div className="piece-row">
              <button className="link" aria-expanded={open.has(p.name)} onClick={() => toggle(p.name)}>
                <strong>{PIECE_LABEL[p.name]}</strong> · {p.status === "waiting_on_input" && p.claim_ids.length === 0 ? "Not assessed yet" : VERDICT_LABEL[p.verdict]}
              </button>
              <span className="counts">
                Source links: {p.corroborating_sources} agree · {p.contradicting_sources} disagree
              </span>
              <button
                onClick={() => {
                  setOpen((o) => new Set(o).add(p.name));
                  setBox(`${p.name}:`);
                }}
              >
                Steer this piece
              </button>
              <button aria-label="Move up" onClick={() => move(i, -1)}>
                ↑
              </button>
              <button aria-label="Move down" onClick={() => move(i, 1)}>
                ↓
              </button>
            </div>
            <p className={`reason ${p.reason_claim_ids.some((id) => claims.get(id)?.scan === "steering") ? "scenario-reason" : ""}`}>{p.reason}</p>
            {open.has(p.name) && (
              <>
                {box === `${p.name}:` && <SteerBox busy={busy === `${p.name}:`} first={first} onSend={(s) => send(p.name, null, s)} onClose={() => setBox(null)} />}
                {steersOn(p.name, null).map((s) => (
                  <div key={s.n} className="steered">
                    <ul className="claims">{(shownUnder.get(`${s.n}`) ?? []).map((id) => claims.get(id)).filter((c): c is Claim => !!c).map((c) => line(c, p.name))}</ul>
                    <Diff s={s} ctx={ctx} />
                  </div>
                ))}
                <ul className="claims">
                  {p.claim_ids
                    .filter((id) => !underASteer.has(id) && !replaced.has(id))
                    .map((id) => claims.get(id))
                    .filter((c): c is Claim => !!c)
                    .map((c) => line(c, p.name))}
                </ul>
              </>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}

type Ctx = {
  readout: Readout;
  claims: Map<string, Claim>;
  addedBy: Map<string, Steered>;
  shownUnder: Map<string, string[]>;
  steersOn: (typedOn: string, claimId: string | null) => Steered[];
  line: (c: Claim, piece: string) => ReactNode;
};

function LineWithSteers(props: {
  claim: Claim;
  piece: string;
  boxOpen: boolean;
  busy: boolean;
  first: boolean;
  onOpen: () => void;
  onClose: () => void;
  onSend: (s: string) => void;
  ctx: Ctx;
}) {
  const { ctx, claim } = props;
  return (
    <>
      <Line claim={claim} ctx={ctx} onSteer={props.onOpen} />
      {props.boxOpen && <SteerBox busy={props.busy} first={props.first} onSend={props.onSend} onClose={props.onClose} />}
      {ctx.steersOn(props.piece, claim.id).map((s) => (
        <li key={s.n} className="steered">
          <ul className="claims">
            {(ctx.shownUnder.get(`${s.n}`) ?? [])
              .map((id) => ctx.claims.get(id))
              .filter((c): c is Claim => !!c)
              .map((c) => ctx.line(c, props.piece))}
          </ul>
          <Diff s={s} ctx={ctx} />
        </li>
      ))}
    </>
  );
}

function Line({ claim, ctx, onSteer, before }: { claim: Claim; ctx: Ctx; onSteer?: () => void; before?: boolean }) {
  const by = ctx.addedBy.get(claim.id);
  const scenario = claim.scan === "steering";
  const panel = namedPanel(ctx.readout, claim);
  const [rows, setRows] = useState(false);
  const Tag = before ? "div" : "li";
  return (
    <Tag className={`claim ${scenario ? "scenario" : (claim.severity ?? "")}`} data-claim={claim.id}>
      {by && <span className={`tag ${scenario ? "yours" : "new"}`}>{scenario ? who(by.rev) : `new, ${who(by.rev)}`}</span>}
      {claim.text}
      {claim.sources.map((s, i) => (
        <SourceChip key={i} room={ctx.readout.room} claimId={claim.id} source={s} n={i + 1} />
      ))}
      {panel && (
        <button className="link rows-toggle" aria-expanded={rows} onClick={() => setRows(!rows)}>
          {rows ? "hide the rows" : `show the rows it sums (${panel.rows.length} ${panel.columns[0].toLowerCase()} lines)`}
        </button>
      )}
      {onSteer && (
        <button className="link steer-on" onClick={onSteer}>
          steer this line
        </button>
      )}
      {panel && rows && <RowsTable panel={panel} />}
    </Tag>
  );
}

function RowsTable({ panel }: { panel: Panel }) {
  return (
    <div className="rows-table" role="region" aria-label={panel.name}>
      <table>
        <thead>
          <tr>
            {panel.columns.map((c) => (
              <th key={c}>{c}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {panel.rows.map((r, i) => (
            <tr key={i}>
              {r.map((v, j) => (
                <td key={j}>{v}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SteerBox({ busy, first, hint, onSend, onClose }: { busy: boolean; first: boolean; hint?: string; onSend: (s: string) => void; onClose: () => void }) {
  const [text, setText] = useState("");
  const onKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && text.trim() && !busy) onSend(text.trim());
    if (e.key === "Escape") onClose();
  };
  return (
    <div className="steer">
      <input
        autoFocus
        aria-label="Steer in one sentence"
        placeholder={hint ?? (first ? EXAMPLE : "Say what is wrong, in one sentence. Press Enter.")}
        value={text}
        disabled={busy}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={onKey}
      />
      {busy && <span className="note">Steering</span>}
    </div>
  );
}

/** The note without its headline, the instruction it repeats, and the engineering footer (kept in the JSON). */
function said(rev: PieceRevision, headline: string): string {
  let rest = (rev.note ?? "").trim();
  if (headline && rest.startsWith(headline)) rest = rest.slice(headline.length).trim();
  rest = rest.replace(/^[^"]*? instruction: ".*?"\.\s*/, "");
  rest = rest.replace(/^Every piece now reads [^.]*\.\s*/, "");
  rest = rest.replace(/^\d+ new claims?, marked new( \([^)]*\))?\.\s*/, "");
  const cut = rest.indexOf("Read as ");
  return (cut >= 0 ? rest.slice(0, cut) : rest).trim();
}

function Diff({ s, ctx }: { s: Steered; ctx: Ctx }) {
  const { rev, n, panel } = s;
  const rows = panel?.rows ?? [];
  const headline = cell(panel, "headline", 3) ?? (rev.steer.kind === "more_info" ? "More info" : "Rewritten");
  const refused = headline.startsWith("Refused");
  return (
    <div className={`diff ${refused ? "refused" : ""}`} role="status" aria-label={`Steer ${n}`}>
      <h3>{headline}</h3>
      <p className="who">
        {who(rev)}: "{rev.steer.instruction}"
      </p>
      <ul>
        {rows
          .filter((r) => r[0] === "replaced")
          .map((r) => {
            const old = ctx.claims.get(r[1]);
            return (
              <li key={`r${r[1]}`} className="before">
                <span className="label">Before, the check's line (kept):</span>
                {old ? <Line claim={old} ctx={ctx} before /> : <span> {r[2]}</span>}
              </li>
            );
          })}
        {rows
          .filter((r) => r[0] === "dropped")
          .map((r) => (
            <li key={`d${r[1]}`}>Dropped: {r[2]}</li>
          ))}
        {rows
          .filter((r) => r[0] === "wording")
          .map((r) => (
            <li key={`w${r[1]}`}>
              Reworded: <s>{r[2]}</s> {r[3]}
            </li>
          ))}
        {rev.steer.kind === "more_info" && rev.claims_added.length > 0 && (
          <li>
            {rev.claims_added.length} new lines, marked new in their pieces. New sources: {[...new Set(rev.sources_added.map((x) => x.split(", ")[0]))].join("; ")}
          </li>
        )}
      </ul>
      <p>{said(rev, headline)}</p>
    </div>
  );
}

function SourceChip({ room, claimId, source, n }: { room: string; claimId: string; source: Source; n: number }) {
  const [text, setText] = useState<string | null>(null);
  const [from, setFrom] = useState<string>(room);
  const load = () =>
    getClaimSource(room, claimId, n - 1).then(
      (r) => {
        setFrom(r.room);
        setText(r.text);
      },
      (e: Error) => setText(e.message),
    );
  // The quote shows once: when the text at the locator is the quote itself, it is not repeated.
  const same = text !== null && text.trim() === source.quote.trim();
  return (
    <span className="source">
      <sup>
        <button className="link" title={`${source.uri} · ${source.locator}`} onClick={() => (text === null ? load() : setText(null))}>
          [{n}]
        </button>
      </sup>
      {text !== null && (
        <span className="panel" role="note">
          <span className="note">
            {from !== room ? `${from}, the full room: ` : ""}
            {source.uri} · {source.locator}
          </span>
          <q>{source.quote}</q>
          {!same && <pre>{text.slice(0, 1200)}</pre>}
        </span>
      )}
    </span>
  );
}
