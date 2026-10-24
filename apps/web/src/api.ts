// The page's only door to the data. Types come from @tricorder/schema, generated from
// schema/claim.py, so a field is never typed by hand here.
import type { Readout, Source } from "@tricorder/schema";
import { trpc } from "./trpc";
import type { RouterOutputs } from "./trpc";

export type RoomInfo = RouterOutputs["room"]["list"][number];

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return (await res.json()) as T;
}

export const getRooms = () => trpc.room.list.query();

export const getReadout = (room: string) => trpc.room.readout.query(room);

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
