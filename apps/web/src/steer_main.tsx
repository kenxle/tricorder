import type { Readout } from "@tricorder/schema";
import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import { getRooms } from "./api";
import type { RoomInfo } from "./api";
import { getSteerable } from "./steerApi";
import { SteerableOverview } from "./Steering";

import "./tokens.css";

// /steer.html: the steerable overview on its own, until App.tsx mounts
// SteerableOverview in place of its Overview section. ?room=<id> picks the room.

function SteerPage() {
  const [rooms, setRooms] = useState<RoomInfo[]>([]);
  const [room, setRoom] = useState<string>(
    () => new URLSearchParams(location.search).get("room") || "hollis_voice"
  );
  const [readout, setReadout] = useState<Readout | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getRooms().then(setRooms, (error_: Error) => setError(error_.message));
  }, []);
  useEffect(() => {
    setReadout(null);
    setError("");
    getSteerable(room).then(setReadout, (error_: Error) =>
      setError(error_.message)
    );
  }, [room]);

  return (
    <main className="page">
      <header className="masthead">
        <h1>Tricorder</h1>
        <select
          value={room}
          onChange={(e) => setRoom(e.target.value)}
          aria-label="Room"
        >
          {(rooms.length ? rooms.map((r) => r.id) : [room]).map((id) => (
            <option key={id} value={id}>
              {id}
            </option>
          ))}
        </select>
      </header>
      {error && <p className="note">{error}</p>}
      {readout?.synthetic_notice && (
        <p className="banner">{readout.synthetic_notice}</p>
      )}
      {readout && (
        <SteerableOverview
          key={readout.room}
          readout={readout}
          onReadout={setReadout}
        />
      )}
    </main>
  );
}

createRoot(document.querySelector("#root")!).render(
  <StrictMode>
    <SteerPage />
  </StrictMode>
);
