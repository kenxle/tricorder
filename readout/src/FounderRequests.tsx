import { useEffect, useMemo, useState } from "react";
import "./FounderRequests.css";

// Requests to the founder: draft a message from the ask list, copy it or open it in the
// operator's own mail app, and add the founder's files when they reply. Tricorder never sends.
// Server: server/founder_requests_routes.py. Design: docs/features/20261023.02_founder_requests/.

interface Guidance { guide: string; title: string; what: string; form: string; good: string[]; path: string }
interface Item {
  number: number; text: string; operator_why: string; piece: string; checklist_id: string | null;
  covers: string[]; if_you_have_it: boolean; ask_stage: string; top: number | null; title: string;
  guidance: Guidance | null;
}
interface Lines {
  room: string; items: Item[]; default: number[]; synthetic: boolean; copy_command: string | null;
  working_copy: string | null; mailto_max: number; upload_max_bytes: number; accepted: string[];
}
interface Draft { subject: string; body: string; mailto: string; mailto_fits: boolean; items: Item[]; read_from: string | null }
interface Receipt {
  room: string; saved: string; checklist_id: string; item: string; scans_rerun: { scan: string; ok: boolean; error: string | null }[];
  status_before: string; status_after: string; asks_before: number | null; asks_after: number; note?: string;
}

const base = (room: string) => `/api/rooms/${encodeURIComponent(room)}/founder-requests`;
async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    let detail = text;
    try { detail = JSON.parse(text).detail ?? text; } catch { /* plain text */ }
    throw new Error(String(detail));
  }
  return (await res.json()) as T;
}

const PIECE: Record<string, string> = {
  traction_and_revenue: "Traction and revenue", retention: "Retention", burn_and_runway: "Burn and runway",
  unit_economics: "Unit economics", customers: "Customers", market: "Market", comps: "Comps", team: "Team",
  the_pitch_itself: "The pitch itself",
};

function mailtoFor(to: string, subject: string, body: string) {
  const enc = encodeURIComponent;
  return `mailto:${enc(to).replace("%40", "@")}?subject=${enc(subject)}&body=${enc(body.replace(/\r?\n/g, "\r\n"))}`;
}

export function FounderRequests({ room, onRebuilt }: { room: string; onRebuilt?: () => void }) {
  const [lines, setLines] = useState<Lines | null>(null);
  const [error, setError] = useState("");
  const [sel, setSel] = useState<Set<number>>(new Set());
  const [draft, setDraft] = useState<Draft | null>(null);
  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [copied, setCopied] = useState(false);

  const load = () =>
    fetch(base(room)).then((r) => json<Lines>(r)).then((l) => { setLines(l); setSel(new Set(l.default)); setError(""); },
      (e: Error) => { setLines(null); setError(e.message); });
  useEffect(() => { setDraft(null); load(); }, [room]); // eslint-disable-line react-hooks/exhaustive-deps

  const pick = (k: "top" | "need" | "all" | "none") => {
    if (!lines) return;
    setSel(new Set(lines.items.filter((i) => k === "all" || (k === "top" && i.top) ||
      (k === "need" && !i.if_you_have_it && i.ask_stage === "before_second_meeting")).map((i) => i.number)));
  };
  const toggle = (n: number) => setSel((s) => { const t = new Set(s); if (t.has(n)) t.delete(n); else t.add(n); return t; });

  const makeDraft = (numbers: number[]) =>
    fetch(`${base(room)}/draft`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ numbers, to }) })
      .then((r) => json<Draft>(r))
      .then((d) => { setDraft(d); setSubject(d.subject); setBody(d.body); setCopied(false); }, (e: Error) => setError(e.message));

  const link = useMemo(() => mailtoFor(to, subject, body), [to, subject, body]);
  const copy = () => {
    const text = `Subject: ${subject}\n\n${body}`;
    (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject(new Error("no clipboard")))
      .then(() => setCopied(true), () => setCopied(false));
  };

  if (error && !lines) return <section aria-label="Requests to the founder" className="fr"><p className="note">Requests to the founder: {error}</p></section>;
  if (!lines) return null;
  const chosen = lines.items.filter((i) => sel.has(i.number)).map((i) => i.number);

  return (
    <section aria-label="Requests to the founder" className="fr">
      <h2>Requests to the founder</h2>
      <p className="note">Tick lines and draft one message, or draft one line on its own. Tricorder never sends it: copy it, or open it in your own mail app.</p>
      {error && <p className="fr-warn" role="alert">{error}</p>}
      <div className="fr-toolbar">
        <span className="note">Select:</span>
        <button onClick={() => pick("top")}>Top five</button>
        <button onClick={() => pick("need")}>All required</button>
        <button onClick={() => pick("all")}>All</button>
        <button onClick={() => pick("none")}>None</button>
        <button className="fr-primary fr-push" disabled={!chosen.length} onClick={() => makeDraft(chosen)}>
          {chosen.length ? `Draft request for ${chosen.length} selected` : "Draft request"}
        </button>
      </div>
      <div className={draft ? "fr-layout fr-drafting" : "fr-layout"}>
        <ul className="fr-asks">
          {lines.items.map((i) => (
            <li key={i.number} className="fr-ask">
              <input type="checkbox" aria-label={`Select line ${i.number}`} checked={sel.has(i.number)} onChange={() => toggle(i.number)} />
              <div>
                <div className="fr-title">{i.number}. {i.title}</div>
                <div>{i.text}</div>
                <div className="fr-meta">
                  <span>{PIECE[i.piece] ?? i.piece}</span>
                  {i.top && <span className="fr-chip fr-top">Top {i.top}</span>}
                  {i.if_you_have_it && <span className="fr-chip">If you have it</span>}
                  {i.ask_stage === "after_term_sheet" && <span className="fr-chip fr-late">After the term sheet</span>}
                </div>
                <div className="fr-why">For you, not sent: {i.operator_why}</div>
              </div>
              <div><button aria-label={`Draft request for line ${i.number}`} onClick={() => makeDraft([i.number])}>Draft request</button></div>
            </li>
          ))}
        </ul>
        {draft && (
          <aside className="fr-drawer" aria-label="Draft to the founder">
            <h3>Draft to the founder</h3>
            <label htmlFor="fr-to">To</label>
            <input id="fr-to" type="email" placeholder="founder's email" value={to} onChange={(e) => setTo(e.target.value)} />
            <label htmlFor="fr-subject">Subject</label>
            <input id="fr-subject" type="text" value={subject} onChange={(e) => setSubject(e.target.value)} />
            <label htmlFor="fr-body">Message (edit freely)</label>
            <textarea id="fr-body" value={body} onChange={(e) => setBody(e.target.value)} />
            <div className="fr-actions">
              <button className="fr-primary" onClick={copy}>Copy text</button>
              <a className="fr-btn" href={link}>Open in mail app</a>
              <button onClick={() => setDraft(null)}>Close</button>
              {copied && <span className="fr-ok" role="status">Copied.</span>}
            </div>
            {link.length > lines.mailto_max && (
              <p className="fr-warn">This message is long for a mail link, and some mail apps cut long links. Copy the text instead.</p>
            )}
            <details>
              <summary>Where the guidance comes from</summary>
              <ul className="note">
                {[...new Set(draft.items.filter((i) => i.guidance).map((i) => i.guidance!.path))].map((p) => <li key={p}><code>{p}</code></li>)}
                {draft.read_from && <li>Greeting and company read from {draft.read_from}</li>}
              </ul>
            </details>
          </aside>
        )}
      </div>
      <AddReply lines={lines} room={room} onDone={() => { load(); onRebuilt?.(); }} />
    </section>
  );
}

function AddReply({ lines, room, onDone }: { lines: Lines; room: string; onDone: () => void }) {
  const [answers, setAnswers] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [receipt, setReceipt] = useState<Receipt | null>(null);
  const [error, setError] = useState("");
  const target = lines.synthetic ? lines.working_copy ?? `${room}_live` : room;

  const add = async () => {
    if (!file || !answers) return;
    setBusy(true); setError(""); setReceipt(null);
    try {
      if (lines.synthetic && !lines.working_copy) {
        await fetch(`${base(room)}/copy`, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" }).then((r) => json(r));
      }
      // A line number only means something in this room's readout; the copy is sent the checklist id.
      const item = lines.items.find((i) => String(i.number) === answers);
      const q = new URLSearchParams({ answers: item?.checklist_id ?? answers, name: file.name });
      const r = await fetch(`${base(target)}/files?${q}`, { method: "POST", body: file }).then((x) => json<Receipt>(x));
      setReceipt(r);
      onDone();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="fr-intake" aria-label="Add a file from the founder">
      <h3>Add a file from the founder</h3>
      {lines.synthetic && (
        <p className="note">{room} is a synthetic room checked into the repo, so Tricorder never writes into it. Files go to a copy, rooms/{target}{lines.working_copy ? "" : ", made with the first file"}.</p>
      )}
      <label htmlFor="fr-answers">This file answers</label>
      <select id="fr-answers" value={answers} onChange={(e) => setAnswers(e.target.value)}>
        <option value="">Pick the request</option>
        {lines.items.filter((i) => i.checklist_id).map((i) => <option key={i.number} value={String(i.number)}>{i.number}. {i.title}</option>)}
      </select>
      <label htmlFor="fr-file">File</label>
      <input id="fr-file" type="file" accept={lines.accepted.join(",")} onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <div className="fr-actions">
        <button className="fr-primary" disabled={!file || !answers || busy} onClick={add}>{busy ? "Adding and rerunning" : "Add to the room"}</button>
        <span className="note">Up to {Math.round(lines.upload_max_bytes / 1048576)} MB.</span>
      </div>
      {error && <p className="fr-warn" role="alert">{error}</p>}
      {receipt && (
        <ul className="fr-steps" role="status" aria-label="What happened">
          <li>Saved as <code>rooms/{receipt.room}/{receipt.saved}</code>.</li>
          <li>Scans that were waiting ran again: {receipt.scans_rerun.length ? receipt.scans_rerun.map((s) => `${s.scan}${s.ok ? "" : " (failed)"}`).join(", ") : "none"}.</li>
          <li>{receipt.item}: {receipt.status_before} before, {receipt.status_after} now.</li>
          <li>Ask list: {receipt.asks_before ?? "no readout"} lines before, {receipt.asks_after} now. The readout of {receipt.room} was rebuilt.</li>
          {receipt.note && <li>{receipt.note}</li>}
        </ul>
      )}
    </div>
  );
}
