// Which claims go into the final memo. One shared store for every screen: the working page,
// the room view and the memo. Port of the prototype's memo_picks.js.
// Keys: insight:<n> (a What stands out card), claim:<n> (a numbered evidence row), flag:<claim_id>.
// Unset keys use the default: insights and flags are in, everything else is out.
import { useSyncExternalStore } from "react";

type Picks = Record<string, boolean>;
const STORAGE = "tricorder.memo.";
const mem: Record<string, Picks> = {};
const listeners = new Set<() => void>();
let version = 0;

const defaultIn = (key: string) => /^(insight|flag):/.test(key);

function load(company: string): Picks {
  if (mem[company]) return mem[company];
  let o: Picks = {};
  try {
    const raw = globalThis.localStorage?.getItem(STORAGE + company);
    o = raw ? (JSON.parse(raw) as Picks) : {};
  } catch {
    o = {};
  }
  mem[company] = o;
  return o;
}

export function getPick(company: string, key: string): boolean {
  const o = load(company);
  return Object.prototype.hasOwnProperty.call(o, key) ? !!o[key] : defaultIn(key);
}

export function setPick(company: string, key: string, value: boolean) {
  const o = load(company);
  o[key] = value;
  try {
    globalThis.localStorage?.setItem(STORAGE + company, JSON.stringify(o));
  } catch {
    // no storage on this platform; memory still holds it
  }
  version += 1;
  listeners.forEach((fn) => fn());
}

export function togglePick(company: string, key: string) {
  setPick(company, key, !getPick(company, key));
}

/** Every key the person has set for this company, with its state. */
export function listPicks(company: string): { key: string; in: boolean }[] {
  return Object.keys(load(company)).map((key) => ({ key, in: getPick(company, key) }));
}

export function resetPicks(company: string) {
  mem[company] = {};
  try {
    globalThis.localStorage?.removeItem(STORAGE + company);
  } catch {
    // ignore
  }
  version += 1;
  listeners.forEach((fn) => fn());
}

export function subscribePicks(fn: () => void) {
  listeners.add(fn);
  return () => {
    listeners.delete(fn);
  };
}

/** Re-renders the caller whenever any pick changes. */
export function useMemoPick(company: string, key: string): [boolean, () => void] {
  useSyncExternalStore(subscribePicks, () => version, () => version);
  return [getPick(company, key), () => togglePick(company, key)];
}
