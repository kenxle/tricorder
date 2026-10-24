import type { PythonAPI } from "@tricorder/schema/api";
import Constants from "expo-constants";
import { Platform } from "react-native";

// Native talks to the Expo server, which forwards only the readout's API routes.
// Python remains on loopback. Release builds need an explicitly configured server.
export function serverOrigin() {
  if (Platform.OS === "web") {
    return "";
  }
  const configured = process.env.EXPO_PUBLIC_API_URL?.replace(/\/$/, "");
  if (configured) {
    return configured;
  }
  const host = __DEV__ ? Constants.expoConfig?.hostUri : null;
  if (host) {
    return `http://localhost:${new URL(`http://${host}`).port || "8081"}`;
  }
  throw new Error(
    "Set EXPO_PUBLIC_API_URL to the running Expo server URL for this build."
  );
}
export function roomPath(room: string, suffix: string) {
  return `/api/rooms/${encodeURIComponent(room)}/${suffix}`;
}
export async function apiRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${serverOrigin()}${path}`, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });
  if (!response.ok) {
    const body = await response.text();
    let detail = body;
    try {
      detail = JSON.parse(body).detail ?? body;
    } catch {
      /* Keep a non-JSON error. */
    }
    throw new Error(`${response.status}: ${detail}`);
  }
  return response.json() as Promise<T>;
}
export type RoomInfo = PythonAPI["GET /api/rooms"]["output"][number];
export const getRooms = (signal?: AbortSignal) =>
  apiRequest<RoomInfo[]>("/api/rooms", { signal });
export const getReadout = (room: string, signal?: AbortSignal) =>
  apiRequest<PythonAPI["GET /api/rooms/{room}/readout"]["output"]>(
    roomPath(room, "readout"),
    { signal }
  );
export const getSteerable = (room: string, signal?: AbortSignal) =>
  apiRequest<PythonAPI["GET /api/rooms/{room}/steerable"]["output"]>(
    roomPath(room, "steerable"),
    { signal }
  );
export const buildReadout = (room: string) =>
  apiRequest<PythonAPI["POST /api/rooms/{room}/readout"]["output"]>(
    roomPath(room, "readout"),
    { method: "POST" }
  );
