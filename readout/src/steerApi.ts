// Steering's door to the server (server/steering_routes.py). Types come from
// schema/ts, generated from schema/claim.py; the response wrapper is steering's own.
import type { Panel, PieceRevision, Readout } from "../../schema/ts/claim";

export interface SteerResponse {
  readout: Readout;
  revision: PieceRevision;
  changes: Panel;
  reading: { kind: "rewrite" | "more_info"; path: "model" | "rules"; fallback_why: string | null };
  source_room: string;
  rebuilt_by: string;
  store: { saved: boolean; version: number | null; new: boolean | null; why: string | null };
}

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = await res.text();
    try {
      detail = (JSON.parse(detail) as { detail?: string }).detail ?? detail;
    } catch {
      /* not JSON; keep the text */
    }
    throw new Error(detail);
  }
  return (await res.json()) as T;
}

export const getSteerable = (room: string) =>
  fetch(`/api/rooms/${encodeURIComponent(room)}/steerable`).then((r) => json<Readout>(r));

export const postSteer = (room: string, body: { piece: string; sentence: string; claim_id?: string | null }) =>
  fetch(`/api/rooms/${encodeURIComponent(room)}/steer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }).then((r) => json<SteerResponse>(r));

/** The text at a line's i-th source, read from the room the line reads (the full room after a switch). */
export const getClaimSource = (room: string, claimId: string, i: number) =>
  fetch(`/api/rooms/${encodeURIComponent(room)}/claims/${encodeURIComponent(claimId)}/sources/${i}`).then((r) =>
    json<{ room: string; text: string }>(r),
  );
