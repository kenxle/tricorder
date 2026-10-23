import { useMemo, useState, type KeyboardEvent, type ReactNode } from "react";
import type { Claim, Panel, PieceRevision, Readout, Source } from "../../schema/ts/claim";
import { getSourceText } from "./api";
import { PIECE_LABEL, VERDICT_LABEL } from "./labels";
import { postSteer } from "./steerApi";
import "./steering.css";

// The overview, steerable: one box on every piece and on every line, opened by
// a click. One sentence and Enter, nothing else (ROADMAP "steering"). The
// revised lines appear where the operator typed, tagged, with the diff under
// them in BRAND.md's words ("A steered piece"). Mount it in App.tsx in place
// of the Overview section; until then /steer.html serves it on its own.

type Added = { rev: PieceRevision; n: number; tag: "your steer" | "new"; room: string | null };

function changesOf(readout: Readout, n: number): Panel | undefined {
  return readout.panels.find((p) => p.name === `steer ${n}: what changed`);
}

function sourceRoomOf(panel: Panel | undefined): string | null {
  const row = panel?.rows.find((r) => r[0] === "source");
  return row ? row[3] : null;
}

export function SteerableOverview({ readout, onReadout }: { readout: Readout; onReadout: (r: Readout) => void }) {
  const claims = useMemo(() => new Map(readout.claims.map((c) => [c.id, c])), [readout]);
  const added = useMemo(() => {
    const m = new Map<string, Added>();
    readout.revisions.forEach((rev, i) => {
      const room = sourceRoomOf(changesOf(readout, i + 1));
      for (const id of rev.claims_added) m.set(id, { rev, n: i + 1, tag: id.startsWith("steer") ? "your steer" : "new", room });
    });
    return m;
  }, [readout]);
  const [open, setOpen] = useState<Set<string>>(() => new Set(readout.pieces.filter((p) => p.verdict === "looking_weak").map((p) => p.name)));
  const [box, setBox] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string>("");

  const send = (piece: string, claimId: string | null, sentence: string) => {
    const where = `${piece}:${claimId ?? ""}`;
    setBusy(where);
    setError("");
    postSteer(readout.room, { piece, sentence, claim_id: claimId })
      .then((r) => {
        setBox(null);
        setOpen((o) => new Set(o).add(piece));
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

  const revs = (piece: string, claimId: string | null) =>
    readout.revisions.map((rev, i) => ({ rev, n: i + 1 })).filter(({ rev }) => rev.steer.piece === piece && (rev.steer.claim_id ?? null) === claimId);

  const renderAdded = (rev: PieceRevision): ReactNode[] =>
    rev.claims_added
      .map((id) => claims.get(id))
      .filter((c): c is Claim => !!c)
      .map((c) => {
        const where = `${rev.steer.piece}:${c.id}`;
        return (
          <LineWithSteers
            key={c.id}
            room={readout.room}
            claim={c}
            added={added.get(c.id)}
            boxOpen={box === where}
            busy={busy === where}
            onOpen={() => setBox(where)}
            onClose={() => setBox(null)}
            onSend={(s) => send(rev.steer.piece, c.id, s)}
            revisions={revs(rev.steer.piece, c.id)}
            renderAdded={renderAdded}
            claims={claims}
            readout={readout}
          />
        );
      });

  return (
    <section aria-label="Overview">
      <h2>Overview</h2>
      {error && (
        <p className="note" role="alert">
          {error}
        </p>
      )}
      <ul className="pieces">
        {readout.pieces.map((p) => (
          <li key={p.name} className={`piece ${p.verdict}`} data-piece={p.name}>
            <div className="piece-row">
              <button className="link" aria-expanded={open.has(p.name)} onClick={() => toggle(p.name)}>
                <strong>{PIECE_LABEL[p.name]}</strong> · {VERDICT_LABEL[p.verdict]}
              </button>
              <span className="counts">
                {p.corroborating_sources} agree · {p.contradicting_sources} disagree
              </span>
              <button
                onClick={() => {
                  setOpen((o) => new Set(o).add(p.name));
                  setBox(`${p.name}:`);
                }}
              >
                Steer this piece
              </button>
            </div>
            <p className="reason">{p.reason}</p>
            {open.has(p.name) && (
              <>
                {box === `${p.name}:` && <SteerBox busy={busy === `${p.name}:`} onSend={(s) => send(p.name, null, s)} onClose={() => setBox(null)} />}
                {revs(p.name, null).map(({ rev, n }) => (
                  <div key={n}>
                    <ul className="claims">{renderAdded(rev)}</ul>
                    <Diff rev={rev} n={n} claims={claims} panel={changesOf(readout, n)} />
                  </div>
                ))}
                <ul className="claims">
                  {p.claim_ids
                    .filter((id) => !added.has(id))
                    .map((id) => claims.get(id))
                    .filter((c): c is Claim => !!c)
                    .map((c) => (
                      <LineWithSteers
                        key={c.id}
                        room={readout.room}
                        claim={c}
                        boxOpen={box === `${p.name}:${c.id}`}
                        busy={busy === `${p.name}:${c.id}`}
                        onOpen={() => setBox(`${p.name}:${c.id}`)}
                        onClose={() => setBox(null)}
                        onSend={(s) => send(p.name, c.id, s)}
                        revisions={revs(p.name, c.id)}
                        renderAdded={renderAdded}
                        claims={claims}
                        readout={readout}
                      />
                    ))}
                </ul>
              </>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}

function LineWithSteers(props: {
  room: string;
  claim: Claim;
  added?: Added;
  boxOpen: boolean;
  busy: boolean;
  onOpen: () => void;
  onClose: () => void;
  onSend: (s: string) => void;
  revisions: { rev: PieceRevision; n: number }[];
  renderAdded: (rev: PieceRevision) => ReactNode[];
  claims: Map<string, Claim>;
  readout: Readout;
}) {
  return (
    <>
      <Line room={props.room} claim={props.claim} added={props.added} onSteer={props.onOpen} />
      {props.boxOpen && <SteerBox busy={props.busy} onSend={props.onSend} onClose={props.onClose} />}
      {props.revisions.map(({ rev, n }) => (
        <li key={n} className="steered">
          <ul className="claims">{props.renderAdded(rev)}</ul>
          <Diff rev={rev} n={n} claims={props.claims} panel={changesOf(props.readout, n)} />
        </li>
      ))}
    </>
  );
}

function Line({ room, claim, added, onSteer }: { room: string; claim: Claim; added?: Added; onSteer: () => void }) {
  const sourceRoom = added?.room ?? room;
  return (
    <li className={`claim ${claim.severity ?? ""}`} data-claim={claim.id}>
      {added && <span className={`tag ${added.tag === "your steer" ? "yours" : "new"}`}>{added.tag}</span>}
      {claim.text}
      {claim.sources.map((s, i) => (
        <SourceChip key={i} room={sourceRoom} source={s} n={i + 1} />
      ))}
      <button className="link steer-on" onClick={onSteer}>
        steer this line
      </button>
    </li>
  );
}

function SteerBox({ busy, onSend, onClose }: { busy: boolean; onSend: (s: string) => void; onClose: () => void }) {
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
        placeholder="Say what is wrong, in one sentence. Press Enter."
        value={text}
        disabled={busy}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={onKey}
      />
      {busy && <span className="note">Steering</span>}
    </div>
  );
}

function Diff({ rev, n, claims, panel }: { rev: PieceRevision; n: number; claims: Map<string, Claim>; panel?: Panel }) {
  const more = rev.steer.kind === "more_info";
  const rows = panel?.rows ?? [];
  // The note is the record, in BRAND.md's words. Its first sentence is the heading;
  // how it was read and rebuilt goes last, in muted text.
  const rest = (rev.note ?? "").replace(/^(Rewritten|More info) on your instruction: ".*?"\.\s*/, "");
  const cut = rest.indexOf("Read as ");
  const said = cut >= 0 ? rest.slice(0, cut).trim() : rest;
  const how = cut >= 0 ? rest.slice(cut) : "";
  return (
    <div className="diff" role="status" aria-label={`Steer ${n}`}>
      <h3>
        {more ? "More info on your instruction" : "Rewritten on your instruction"}: "{rev.steer.instruction}"
      </h3>
      <ul>
        {rev.claims_added.map((id) => (
          <li key={`a${id}`}>Added: {claims.get(id)?.text ?? id}</li>
        ))}
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
        {rev.sources_added.length > 0 && <li>New sources: {rev.sources_added.join("; ")}</li>}
        {rev.claims_added.length === 0 && rows.every((r) => r[0] !== "dropped" && r[0] !== "wording") && <li>No line added, dropped or reworded.</li>}
      </ul>
      <p>{said}</p>
      <p className="note">
        {how} Revision {n}, kept.
      </p>
    </div>
  );
}

function SourceChip({ room, source, n }: { room: string; source: Source; n: number }) {
  const [text, setText] = useState<string | null>(null);
  return (
    <span className="source">
      <sup>
        <button
          className="link"
          title={`${room}: ${source.uri} · ${source.locator}`}
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
