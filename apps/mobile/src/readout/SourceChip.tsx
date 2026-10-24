import type { Source } from "@tricorder/schema";
import type { PythonAPI } from "@tricorder/schema/api";
import { useEffect, useRef, useState } from "react";
import { ActivityIndicator } from "react-native";

import { AnnotationScope } from "../annotations/context";
import { apiRequest, roomPath } from "./api";
import { Action, Body, Card, Note } from "./ui";

interface SourceProps {
  room: string;
  source: Source;
  n: number;
  claimId?: string;
  revision?: string;
}
export function SourceChip(props: SourceProps) {
  return (
    <SourceContent
      key={JSON.stringify([
        props.room,
        props.claimId,
        props.source,
        props.revision,
      ])}
      {...props}
    />
  );
}
function SourceContent({
  room,
  source,
  n,
  claimId,
}: {
  room: string;
  source: Source;
  n: number;
  claimId?: string;
}) {
  const [open, setOpen] = useState(false);
  const [text, setText] = useState<string | null>(null);
  const [from, setFrom] = useState(room);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const controller = useRef<AbortController | null>(null);
  useEffect(() => () => controller.current?.abort(), []);
  async function load() {
    setOpen(true);
    setError("");
    setLoading(true);
    controller.current?.abort();
    const abort = new AbortController();
    controller.current = abort;
    try {
      if (claimId) {
        const result = await apiRequest<
          PythonAPI["GET /api/rooms/{room}/claims/{claim_id}/sources/{i}"]["output"]
        >(
          roomPath(
            room,
            `claims/${encodeURIComponent(claimId)}/sources/${n - 1}`
          ),
          { signal: abort.signal }
        );
        setFrom(result.room);
        setText(result.text);
      } else {
        const result = await apiRequest<{ text: string }>(
          roomPath(room, "source"),
          { body: JSON.stringify(source), method: "POST", signal: abort.signal }
        );
        setText(result.text);
      }
    } catch (error_) {
      if (!abort.signal.aborted) {
        setError((error_ as Error).message);
      }
    } finally {
      if (!abort.signal.aborted) {
        setLoading(false);
      }
    }
  }
  return (
    <>
      <Action
        title={`${open ? "Hide" : "Source"} [${n}] · ${source.locator}`}
        onPress={() => (open ? setOpen(false) : void load())}
      />
      {open && (
        <AnnotationScope
          id={`room:${room}/source:${source.uri}:${source.locator}`}
          label={`${room} · Source ${n} · ${source.locator}`}
        >
          <Card>
            <Note>
              {from === room ? "" : `${from}, the full room: `}
              {source.uri} · {source.locator}
            </Note>
            <Body>{source.quote}</Body>
            {loading && (
              <ActivityIndicator accessibilityLabel="Loading source" />
            )}
            {error ? (
              <>
                <Body accessibilityRole="alert">{error}</Body>
                <Action title="Retry source" onPress={() => void load()} />
              </>
            ) : null}
            {text !== null && text.trim() !== source.quote.trim() && (
              <Body style={{ fontFamily: "monospace", fontSize: 13 }}>
                {text.slice(0, 1200)}
              </Body>
            )}
          </Card>
        </AnnotationScope>
      )}
    </>
  );
}
