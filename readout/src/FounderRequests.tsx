import { useEffect, useMemo, useRef, useState, type RefObject } from "react";
import "./FounderRequests.css";

// Requests to the founder: draft a message from the ask list, copy it or open it in the
// operator's own mail app, and add the founder's files when they reply. Tricorder never sends.
// Server: server/founder_requests_routes.py. Design: docs/features/20261023.02_founder_requests/.

interface Guidance { guide: string; title: string; what: string; form: string; good: string[]; path: string }
interface Item {
  number: number; lines: number[]; text: string; operator_why: string; piece: string; checklist_id: string | null;
  covers: string[]; if_you_have_it: boolean; ask_stage: string; top: number | null; title: string;
  guidance: Guidance | null; includes: string | null; in_room: string[]; rests_on_flag: boolean;
  requests: { checklist_id: string; name: string }[];
}
interface Held { number: number; title: string; files: string[] }
interface Lines {
  room: string; items: Item[]; default: number[]; held: Held[]; synthetic: boolean; copy_command: string | null;
  working_copy: string | null; mailto_max: number; upload_max_bytes: number; accepted: string[];
  by: string; reason: string; sender: string; fund: string;
}
interface Draft { subject: string; body: string; mailto: string; mailto_fits: boolean; items: Item[]; read_from: string | null; by: string }
interface Answer { checklist_id: string; item: string; status_before: string; status_after: string }
interface Received { original_name: string; saved: string; answers: Answer[]; note?: string }
interface Receipt {
  room: string; files: Received[]; scans_rerun: { scan: string; ok: boolean; error: string | null }[];
  asks_before: number | null; asks_after: number; summary: string[];
}

// The operator's name and fund are remembered in this browser only, for the sign-off.
const remembered = (key: string) => { try { return localStorage.getItem(`tricorder.fr.${key}`) ?? ""; } catch { return ""; } };
const remember = (key: string, value: string) => { try { localStorage.setItem(`tricorder.fr.${key}`, value); } catch { /* no storage */ } };

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
  const [numbers, setNumbers] = useState<number[]>([]);
  const [to, setTo] = useState("");
  const [sender, setSender] = useState(() => remembered("sender"));
  const [fund, setFund] = useState(() => remembered("fund"));
  const [by, setBy] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [copied, setCopied] = useState(false);
  const drawer = useRef<HTMLElement | null>(null);
  const intake = useRef<HTMLDivElement | null>(null);

  const load = () =>
    fetch(base(room)).then((r) => json<Lines>(r)).then((l) => {
      setLines(l); setSel(new Set(l.default)); setError("");
      setBy((b) => b || l.by);
      setSender((v) => v || l.sender); setFund((v) => v || l.fund);
    }, (e: Error) => { setLines(null); setError(e.message); });
  useEffect(() => { setDraft(null); load(); }, [room]); // eslint-disable-line react-hooks/exhaustive-deps

  const pick = (k: "top" | "need" | "all" | "none") => {
    if (!lines) return;
    setSel(new Set(lines.items.filter((i) => k === "all" || (k === "top" && i.top) ||
      (k === "need" && !i.if_you_have_it && i.ask_stage === "before_second_meeting")).map((i) => i.number)));
  };
  const toggle = (n: number) => setSel((s) => { const t = new Set(s); if (t.has(n)) t.delete(n); else t.add(n); return t; });

  const makeDraft = (wanted: number[], scroll = true) =>
    fetch(`${base(room)}/draft`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ numbers: wanted, to, sender, fund, by: by || null }),
    })
      .then((r) => json<Draft>(r))
      .then((d) => {
        setDraft(d); setNumbers(wanted); setSubject(d.subject); setBody(d.body); setCopied(false); setError("");
        if (scroll) requestAnimationFrame(() => drawer.current?.scrollIntoView?.({ block: "nearest" }));
      }, (e: Error) => setError(e.message));

  // A change to the date or the sign-off redoes the draft while the message is untouched;
  // once the operator has edited the message, a button offers it instead.
  const edited = draft !== null && body !== draft.body;
  const signoff = (f: (v: string) => void, key?: string) => (v: string) => { f(v); if (key) remember(key, v); };
  useEffect(() => {
    if (draft && !edited) { const t = setTimeout(() => makeDraft(numbers, false), 300); return () => clearTimeout(t); }
  }, [sender, fund, by]); // eslint-disable-line react-hooks/exhaustive-deps

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
        <button onClick={() => intake.current?.scrollIntoView?.({ block: "nearest" })}>Add the founder's reply</button>
        <button className="fr-primary fr-push" disabled={!chosen.length} onClick={() => makeDraft(chosen)}>
          {chosen.length ? `Draft request for ${chosen.length} selected` : "Draft request"}
        </button>
      </div>
      <div className="fr-layout">
        <ul className="fr-asks">
          {lines.items.map((i) => (
            <li key={i.number} className="fr-ask">
              <input type="checkbox" aria-label={`Select ${i.title}`} checked={sel.has(i.number)} onChange={() => toggle(i.number)} />
              <div>
                <div className="fr-title">{i.title}</div>
                <div>{i.text}</div>
                <div className="fr-meta">
                  <span>{PIECE[i.piece] ?? i.piece}</span>
                  {i.top && <span className="fr-chip fr-top">Top {i.top}</span>}
                  {i.rests_on_flag && <span className="fr-chip fr-late">A red flag rests on it</span>}
                  {i.if_you_have_it && <span className="fr-chip">If you have it</span>}
                  {i.ask_stage === "after_term_sheet" && <span className="fr-chip fr-late">After the term sheet</span>}
                </div>
                {i.in_room.length > 0 && <div className="fr-why">Already in the room: {i.in_room.join(", ")}. The line asks only for the rest.</div>}
                <div className="fr-why">For you, not sent: {i.operator_why}</div>
              </div>
              <div><button aria-label={`Draft request for ${i.title}`} onClick={() => makeDraft([i.number])}>Draft request</button></div>
            </li>
          ))}
          {lines.held.length > 0 && (
            <li className="fr-held">
              <div className="fr-title">Not asked for: the room already holds these</div>
              <ul>{lines.held.map((h) => <li key={h.number}>{h.title}: {h.files.join(", ")}</li>)}</ul>
            </li>
          )}
        </ul>
        <div className="fr-side">
          {draft && (
            <aside ref={drawer} className="fr-drawer" aria-label="Draft to the founder">
              <h3>Draft to the founder</h3>
              <p className="fr-trust">Tricorder never sends this. Copy it, or open it in your own mail app and send it from there.</p>
              <label htmlFor="fr-to">To</label>
              <input id="fr-to" type="email" placeholder="founder's email" value={to} onChange={(e) => setTo(e.target.value)} />
              <div className="fr-row">
                <div><label htmlFor="fr-by">Ask for it by</label>
                  <input id="fr-by" type="date" value={by} onChange={(e) => setBy(e.target.value)} /></div>
                <div><label htmlFor="fr-sender">Your name</label>
                  <input id="fr-sender" type="text" value={sender} onChange={(e) => signoff(setSender, "sender")(e.target.value)} /></div>
                <div><label htmlFor="fr-fund">Fund</label>
                  <input id="fr-fund" type="text" value={fund} onChange={(e) => signoff(setFund, "fund")(e.target.value)} /></div>
              </div>
              {edited && <p className="note"><button onClick={() => makeDraft(numbers, false)}>Redo the draft with these</button> This replaces your edits to the message.</p>}
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
          <AddReply lines={lines} room={room} box={intake} onDone={() => { load(); onRebuilt?.(); }} />
        </div>
      </div>
    </section>
  );
}

interface Pending { file: File; answers: string[] }

function AddReply({ lines, room, box, onDone }: { lines: Lines; room: string; box: RefObject<HTMLDivElement | null>; onDone: () => void }) {
  const [pending, setPending] = useState<Pending[]>([]);
  const [busy, setBusy] = useState(false);
  const [receipt, setReceipt] = useState<Receipt | null>(null);
  const [error, setError] = useState("");
  const target = lines.synthetic ? lines.working_copy ?? `${room}_live` : room;
  // Every request a file can answer, by its plain name; a merged line offers each of its documents.
  const requests = lines.items.flatMap((i) => i.requests.map((r) => ({
    id: r.checklist_id, label: i.requests.length > 1 ? `${i.title}: ${r.name}` : i.title,
  })));
  const label = new Map(requests.map((r) => [r.id, r.label]));

  const choose = (files: FileList | null) =>
    setPending((p) => [...p, ...[...(files ?? [])].map((file) => ({ file, answers: [] as string[] }))]);
  const set = (k: number, f: (p: Pending) => Pending | null) =>
    setPending((p) => p.flatMap((x, j) => (j === k ? [f(x)].filter((y): y is Pending => y !== null) : [x])));
  const ready = pending.length > 0 && pending.every((p) => p.answers.length > 0);

  const b64 = (f: File) => f.arrayBuffer().then((buf) => {
    const bytes = new Uint8Array(buf);
    let bin = "";
    for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  });

  const add = async () => {
    if (!ready) return;
    setBusy(true); setError(""); setReceipt(null);
    try {
      if (lines.synthetic && !lines.working_copy) {
        await fetch(`${base(room)}/copy`, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" }).then((r) => json(r));
      }
      // Checklist ids, not line numbers: a line number only means something in this room's readout.
      const files = await Promise.all(pending.map(async (p) => ({
        name: p.file.name, data: await b64(p.file),
        answers: p.answers.join(","),
      })));
      const r = await fetch(`${base(target)}/batch`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ files }),
      }).then((x) => json<Receipt>(x));
      setReceipt(r); setPending([]);
      onDone();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div ref={box} className="fr-intake" aria-label="Add the founder's reply">
      <h3>Add the founder's reply</h3>
      {lines.synthetic && <p className="note">This is a sample room, so the files go into a working copy of it.</p>}
      <label htmlFor="fr-file">Files from the reply</label>
      <input id="fr-file" type="file" multiple accept={lines.accepted.join(",")} onChange={(e) => { choose(e.target.files); e.target.value = ""; }} />
      {pending.map((p, k) => (
        <div key={`${p.file.name}-${k}`} className="fr-pending" aria-label={`File ${p.file.name}`}>
          <div className="fr-title">{p.file.name} <button aria-label={`Remove ${p.file.name}`} onClick={() => set(k, () => null)}>Remove</button></div>
          {p.answers.map((n) => (
            <span key={n} className="fr-chip">{label.get(n)}
              <button className="fr-x" aria-label={`Not ${label.get(n)}`} onClick={() => set(k, (x) => ({ ...x, answers: x.answers.filter((m) => m !== n) }))}>x</button>
            </span>
          ))}
          <label htmlFor={`fr-answers-${k}`}>{p.answers.length ? "It also answers" : "It answers"}</label>
          <select id={`fr-answers-${k}`} value="" onChange={(e) => { const n = e.target.value; if (n) set(k, (x) => ({ ...x, answers: [...x.answers, n] })); }}>
            <option value="">Pick a request</option>
            {requests.filter((r) => !p.answers.includes(r.id)).map((r) => <option key={r.id} value={r.id}>{r.label}</option>)}
          </select>
        </div>
      ))}
      <div className="fr-actions">
        <button className="fr-primary" disabled={!ready || busy} onClick={add}>
          {busy ? "Adding and rerunning" : pending.length > 1 ? `Add ${pending.length} files to the room` : "Add to the room"}
        </button>
        <span className="note">Up to {Math.round(lines.upload_max_bytes / 1048576)} MB a file.</span>
      </div>
      {error && <p className="fr-warn" role="alert">{error}</p>}
      {receipt && (
        <div role="status" aria-label="What changed">
          <ul className="fr-steps">
            {receipt.files.map((f) => (
              <li key={f.saved}>{f.original_name} is saved as <code>{f.saved}</code>{f.note ? `. ${f.note}` : "."}</li>
            ))}
          </ul>
          <p className="fr-title">What changed</p>
          <ul className="fr-steps">
            {receipt.summary.map((s) => <li key={s}>{s}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
