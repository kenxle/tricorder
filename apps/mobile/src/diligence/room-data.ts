// Typed view of the prototype's synthetic Sazabi data room (fixtures/room-sazabi.json,
// extracted from docs/features/20261024.02_first_steps_ui/prototype/data.json).
// The readout API has no data-room merge yet, so the room view and memo read this fixture.
import roomJson from "./fixtures/room-sazabi.json";

export interface RoomSource {
  uri: string;
  locator?: string;
  quote?: string;
  public?: string;
}
export interface RoomValue {
  key: string;
  value: string;
  out?: boolean;
  source: RoomSource;
}
export interface RoomFlag {
  kind: "red" | "green";
  piece: string;
  claim_id: string;
  title: string;
  stated: RoomValue;
  found: RoomValue;
  others: RoomValue[];
  ask: string | null;
  relative_gap: number | null;
  basis: "disagreement" | "agreement" | "strength" | string;
  why?: string;
  strip?: { benchmark?: { label: string } } | null;
}
export interface RoomPiece {
  name: string;
  label: string;
  verdict: string;
  reason: string;
  agree: number;
  disagree: number;
  claim_ids: string[];
}
export interface RoomClaim {
  id: string;
  piece: string;
  text: string;
  display?: string;
  sources: RoomSource[];
  mark?: string;
  agree?: RoomSource[];
  disagree?: RoomSource[];
}
export interface RevenueChart {
  kind: "revenue";
  months: string[];
  recurring: number[];
  one_time: number[];
  recurring_label: string;
  one_time_label: string;
  deck_monthly: number;
  deck_label: string;
}
export interface CashChart {
  kind: "cash";
  as_of: string;
  series: {
    name: string;
    points: [number, number][];
    style: string;
    end: string;
  }[];
  baseline: number;
  baseline_label: string;
}
export interface RoomReport {
  key: string;
  title: string;
  paras: { lead: string; refs: string[]; body: string }[];
  asks: string[];
  chart?: RevenueChart | CashChart;
  needs: string[];
}
export interface RoomWaiting {
  piece: string;
  files: string[];
  requests: string[];
  title: string;
  text: string;
}
export interface RoomState {
  arrived: string[];
  files_total: number;
  shown: string[];
  flags: { green: string[]; red: string[] };
  waiting: RoomWaiting[];
  pieces: Record<
    string,
    {
      verdict: string;
      reason: string;
      agree: number;
      disagree: number;
      waiting: string[];
    }
  >;
}
export interface Room {
  synthetic_notice: string;
  as_of: string;
  top_flags: { green: RoomFlag[]; red: RoomFlag[] };
  extra_flags?: RoomFlag[];
  pieces: RoomPiece[];
  claims: Record<string, RoomClaim>;
  memo_company: string;
  reports: RoomReport[];
  states: { partial: RoomState; full: RoomState };
}

export type RoomStateName = "partial" | "full";

export const sazabiRoom = roomJson as unknown as Room;
export const ROOM_COMPANY = "Sazabi";

export function allFlags(room: Room): RoomFlag[] {
  return [
    ...room.top_flags.green,
    ...room.top_flags.red,
    ...(room.extra_flags ?? []),
  ];
}

// Ken, 1:22 PM: two sources that agree make a small green flag; two that disagree make a big red flag.
export type FlagWeight = "headline" | "big" | "small";
export function flagWeight(f: RoomFlag): FlagWeight {
  if (f.kind === "red" || f.basis === "disagreement") {
    return "big";
  }
  return f.basis === "agreement" ? "small" : "headline";
}

// Real strengths first, then big red flags worst first, then small green flags.
export function orderFlags(flags: RoomFlag[]): RoomFlag[] {
  const headline = flags.filter((f) => flagWeight(f) === "headline");
  const big = flags
    .filter((f) => flagWeight(f) === "big")
    .sort((a, b) => (b.relative_gap ?? 0) - (a.relative_gap ?? 0));
  const small = flags.filter((f) => flagWeight(f) === "small");
  return [...headline, ...big, ...small];
}

export function flagsForState(room: Room, state: RoomStateName): RoomFlag[] {
  const s = room.states[state];
  const all = allFlags(room);
  const ids = [...s.flags.green, ...s.flags.red];
  const picked = ids
    .map((id) => all.find((f) => f.claim_id === id))
    .filter((f): f is RoomFlag => f !== undefined);
  return orderFlags(picked);
}

export function pieceLabel(room: Room, name: string): string {
  return room.pieces.find((p) => p.name === name)?.label ?? name;
}

// "<piece>: <text>" titles show the text as a subtitle (Ken, 1:25 PM).
export function subtitle(t: string): string {
  const i = t.indexOf(": ");
  const rest = i === -1 ? t : t.slice(i + 2);
  return rest.charAt(0).toUpperCase() + rest.slice(1);
}

export function shortFile(f: string): string {
  return f.split("/").pop() ?? f;
}

export function sourceLabel(s: RoomSource): string {
  const file = shortFile(s.uri.split(", ")[0] ?? s.uri);
  return s.locator ? `${file}, ${s.locator}` : file;
}

// Exact dollars, no rounding (Ken: $5.25M, not $5.3M).
export function usd(n: number): string {
  return `$${Math.round(n).toLocaleString("en-US")}`;
}

export const VERDICT_LABEL: Record<string, string> = {
  looking_strong: "Looking strong",
  looking_weak: "Looking weak",
  mixed: "Mixed",
  not_enough_in_the_room: "Not enough in the room",
};
