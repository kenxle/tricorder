// The page's only door to the data. Types come from @tricorder/schema, generated from
// schema/claim.py, so a field is never typed by hand here.
import type { Readout, Source } from "@tricorder/schema";

export interface RoomInfo {
  id: string;
  path: string;
  inputs: string[];
  has_readout: boolean;
}

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return (await res.json()) as T;
}

export const getRooms = () => fetch("/api/rooms").then((r) => json<RoomInfo[]>(r));

export const getReadout = (room: string) =>
  fetch(`/api/rooms/${encodeURIComponent(room)}/readout`).then((r) => json<Readout>(r));

export const buildReadout = (room: string) =>
  fetch(`/api/rooms/${encodeURIComponent(room)}/readout`, { method: "POST" }).then((r) => json<Readout>(r));

export const getSourceText = (room: string, source: Source) =>
  fetch(`/api/rooms/${encodeURIComponent(room)}/source`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(source),
  }).then((r) => json<{ text: string }>(r));

export const fileUrl = (room: string, uri: string) =>
  `/api/rooms/${encodeURIComponent(room)}/files/${uri.split("/").map(encodeURIComponent).join("/")}`;
