import type { Claim, Readout } from "@tricorder/schema";
import * as Clipboard from "expo-clipboard";
import { useEffect, useRef, useState } from "react";
import { ActivityIndicator, FlatList, StyleSheet, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { AnnotationToolbar } from "../annotations/annotation-panel";
import { AnnotationScope } from "../annotations/context";
import { buildReadout, getReadout, getRooms, getSteerable } from "./api";
import type { RoomInfo } from "./api";
import { FounderRequests } from "./FounderRequests";
import { NativeSheet } from "./native-sheet";
import { SourceChip } from "./SourceChip";
import { SteerableOverview } from "./Steering";
import {
  Action,
  Body,
  Card,
  Heading,
  Note,
  Row,
  renderReadoutScroll,
  useReadoutColors,
} from "./ui";

export default function ReadoutScreen() {
  const colors = useReadoutColors();
  const [rooms, setRooms] = useState<RoomInfo[]>([]);
  const [room, setRoom] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [picker, setPicker] = useState(false);
  const [reload, setReload] = useState(0);
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  useEffect(() => {
    const abort = new AbortController();
    getRooms(abort.signal)
      .then((result) => {
        if (abort.signal.aborted) {
          return;
        }
        setRooms(result);
        setRoom(
          (current) =>
            current ||
            result.find((r) => r.id === "hollis_voice")?.id ||
            result[0]?.id ||
            ""
        );
      })
      .catch((error_: Error) => {
        if (!abort.signal.aborted) {
          setError(error_.message);
        }
      })
      .finally(() => {
        if (!abort.signal.aborted) {
          setLoading(false);
        }
      });
    return () => abort.abort();
  }, [reload]);
  async function openRebuilt(next: string) {
    // Read the new working-copy room list before switching, as on the web.
    try {
      const result = await getRooms();
      if (!mounted.current) {
        return;
      }
      setRooms(result);
      setRoom(next);
    } catch (error_) {
      if (mounted.current) {
        setError((error_ as Error).message);
      }
    }
  }
  return (
    <SafeAreaView style={[styles.screen, { backgroundColor: colors.bg }]}>
      <View style={styles.masthead}>
        <View>
          <Note style={styles.eyebrow}>THE WORKING READOUT</Note>
          <Heading>Data rooms</Heading>
        </View>
        <Action
          title={room ? `Room: ${room}` : "Choose room"}
          onPress={() => setPicker(true)}
          disabled={!rooms.length}
        />
      </View>
      {loading && <ActivityIndicator accessibilityLabel="Loading rooms" />}
      {error ? (
        <Card>
          <Body accessibilityRole="alert">{error}</Body>
          <Action
            title="Retry rooms"
            onPress={() => {
              setLoading(true);
              setError("");
              setReload((x) => x + 1);
            }}
          />
        </Card>
      ) : null}
      {!loading && !error && !rooms.length && (
        <Note>No rooms available yet.</Note>
      )}
      {room ? (
        <RoomReadout
          key={room}
          room={room}
          onRoom={(next) => void openRebuilt(next)}
        />
      ) : null}
      <NativeSheet visible={picker} onClose={() => setPicker(false)}>
        <View style={[styles.screen, { backgroundColor: colors.bg }]}>
          <Row>
            <Heading>Choose room</Heading>
            <Action title="Close rooms" onPress={() => setPicker(false)} />
          </Row>
          <FlatList
            renderScrollComponent={renderReadoutScroll}
            data={rooms}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <Card>
                <Action
                  title={item.id}
                  onPress={() => {
                    setRoom(item.id);
                    setPicker(false);
                  }}
                />
              </Card>
            )}
          />
        </View>
      </NativeSheet>
    </SafeAreaView>
  );
}

type RowItem = { key: string; title?: string } & (
  | { kind: "gap"; value: Readout["gaps"][number] }
  | { kind: "claim"; value: Claim }
  | { kind: "ask"; value: Readout["asks"][number] }
  | { kind: "empty" }
);
const rowScope = (room: string, item: RowItem) => {
  let id = "empty";
  if (item.kind === "claim") {
    const { id: claimId } = item.value;
    id = claimId;
  } else if (item.kind !== "empty") {
    id = item.value.what;
  }
  const labels = {
    ask: "Founder request",
    claim: "Unverified claim",
    empty: "Founder requests",
    gap: "Evidence gap",
  };
  return {
    id: `room:${room}/${item.kind}:${id}`,
    label: `${room} · ${labels[item.kind]}`,
  };
};

function RoomReadout({
  room,
  onRoom,
}: {
  room: string;
  onRoom: (room: string) => void;
}) {
  const colors = useReadoutColors();
  const [readout, setReadout] = useState<Readout | null>(null);
  const [loading, setLoading] = useState(true);
  const [building, setBuilding] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);
  const request = useRef(0);
  const live = useRef(true);
  useEffect(() => {
    live.current = true;
    return () => {
      live.current = false;
    };
  }, []);
  async function load() {
    const id = ++request.current;
    try {
      const result = await getReadout(room);
      if (!live.current || request.current !== id) {
        return;
      }
      setReadout(result);
      // Steering may include revisions and a full-room source switch.
      const steered = await getSteerable(room);
      if (live.current && request.current === id) {
        setReadout(steered);
      }
    } catch (error_) {
      if (live.current && request.current === id) {
        setError((error_ as Error).message);
      }
    } finally {
      if (live.current && request.current === id) {
        setLoading(false);
      }
    }
  }
  // External-data synchronization: load only sets state after an awaited request.
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [room]);
  async function build() {
    if (building) {
      return;
    }
    const id = ++request.current;
    setBuilding(true);
    setLoading(false);
    setError("");
    try {
      const result = await buildReadout(room);
      if (live.current && request.current === id) {
        setReadout(result);
        setCopied(false);
      }
    } catch (error_) {
      if (live.current && request.current === id) {
        setError((error_ as Error).message);
      }
    } finally {
      if (live.current && request.current === id) {
        setBuilding(false);
      }
    }
  }
  async function copyAsks() {
    if (!readout) {
      return;
    }
    try {
      const ok = await Clipboard.setStringAsync(
        readout.asks.map((ask) => `- ${ask.what}`).join("\n")
      );
      if (live.current) {
        setCopied(ok);
        if (!ok) {
          setError("Could not copy the ask list.");
        }
      }
    } catch (error_) {
      if (live.current) {
        setError((error_ as Error).message);
      }
    }
  }
  const rows: RowItem[] = [];
  readout?.gaps.forEach((value, i) =>
    rows.push({
      key: `gap-${i}`,
      kind: "gap",
      title: i === 0 ? "Gaps" : undefined,
      value,
    })
  );
  readout?.unverified.forEach((value, i) =>
    rows.push({
      key: `unverified-${value.id}`,
      kind: "claim",
      title: i === 0 ? "Could not verify" : undefined,
      value,
    })
  );
  if (readout) {
    if (!readout.asks.length) {
      rows.push({
        key: "empty-asks",
        kind: "empty",
        title: "What to ask the founder for",
      });
    }
    readout.asks.forEach((value, i) =>
      rows.push({
        key: `ask-${i}`,
        kind: "ask",
        title: i === 0 ? "What to ask the founder for" : undefined,
        value,
      })
    );
  }
  const claims = new Map(
    [...(readout?.claims ?? []), ...(readout?.unverified ?? [])].map(
      (claim) => [claim.id, claim]
    )
  );
  return (
    <FlatList
      renderScrollComponent={renderReadoutScroll}
      style={styles.list}
      contentContainerStyle={styles.content}
      data={rows}
      keyExtractor={(item) => item.key}
      keyboardShouldPersistTaps="handled"
      ListHeaderComponent={
        <>
          <AnnotationToolbar />
          <Row>
            <Action
              title={building ? "Building readout…" : "Build readout"}
              disabled={building}
              onPress={() => void build()}
            />
            <Action
              title="Refresh readout"
              disabled={building || loading}
              onPress={() => {
                setLoading(true);
                setError("");
                setReadout(null);
                void load();
              }}
            />
          </Row>
          {(loading || building) && (
            <ActivityIndicator
              accessibilityLabel={
                building ? "Building readout" : "Loading readout"
              }
            />
          )}
          {error ? <Body accessibilityRole="alert">{error}</Body> : null}
          {readout && (
            <>
              <Heading style={styles.title}>
                {room.replaceAll("_", " ")}
              </Heading>
              <Note>
                Every claim sourced. Review the findings, inspect the evidence,
                and steer the readout.
              </Note>
              {readout.synthetic_notice && (
                <Note style={styles.eyebrow}>{readout.synthetic_notice}</Note>
              )}
              <FounderRequests
                room={room}
                onRebuilt={(next) =>
                  next === room ? void load() : onRoom(next)
                }
              />
              <Heading>What stands out</Heading>
              {!readout.top_flags.some((f) => f.kind === "green") && (
                <Note>No green headline from the linked evidence yet.</Note>
              )}
              {!readout.top_flags.some((f) => f.kind === "red") && (
                <Note>
                  No red headline with linked numeric comparisons yet. Check the
                  overview for flagged claims.
                </Note>
              )}
              {["green", "red"]
                .flatMap((kind) =>
                  readout.top_flags.filter((f) => f.kind === kind)
                )
                .map((flag) => (
                  <AnnotationScope
                    key={`${flag.kind}-${flag.rank}`}
                    id={`room:${room}/flag:${flag.piece}:${flag.text}`}
                    label={`${room} · ${flag.piece.replaceAll("_", " ")} · ${flag.kind} flag`}
                  >
                    <Card>
                      <Note
                        style={{
                          color:
                            flag.kind === "green" ? colors.green : colors.red,
                          fontFamily: "PlexMono",
                        }}
                      >
                        {flag.kind === "green" ? "● Green flag" : "▲ Red flag"}
                      </Note>
                      <Body>{flag.text}</Body>
                      <Action
                        title="Inspect finding"
                        onPress={() => setSelectedPiece(flag.piece)}
                      />
                    </Card>
                  </AnnotationScope>
                ))}
              <SteerableOverview
                key={room}
                readout={readout}
                onReadout={(next) => {
                  setReadout(next);
                  setCopied(false);
                }}
                selectedPiece={selectedPiece}
                onClosePiece={() => setSelectedPiece(null)}
              />
            </>
          )}
        </>
      }
      renderItem={({ item }) => (
        <>
          {item.title && <Heading>{item.title}</Heading>}
          {item.title === "What to ask the founder for" &&
          readout?.asks.length ? (
            <Row>
              <Action title="Copy" onPress={() => void copyAsks()} />
              {copied && <Note>Copied.</Note>}
            </Row>
          ) : null}
          <AnnotationScope {...rowScope(room, item)}>
            <Card>
              {item.kind === "gap" && (
                <>
                  <Body>{item.value.what}</Body>
                  <Note>{item.value.why}</Note>
                </>
              )}
              {item.kind === "ask" && (
                <>
                  <Body>{item.value.what}</Body>
                  <Note>{item.value.why}</Note>
                </>
              )}
              {item.kind === "empty" && <Note>Nothing to ask for.</Note>}
              {item.kind === "claim" && (
                <>
                  <Body>{item.value.text}</Body>
                  {item.value.sources.map((source, i) => (
                    <SourceChip
                      key={`${readout?.built_at}:${readout?.revisions.length}:${i}`}
                      room={room}
                      source={source}
                      n={i + 1}
                    />
                  ))}
                  {item.value.corroborated_by.length +
                    item.value.conflicts_with.length >
                    0 && (
                    <Note>
                      {item.value.corroborated_by.length} agree,{" "}
                      {item.value.conflicts_with.length} disagree
                      {item.value.conflicts_with
                        .map((id) => claims.get(id)?.text)
                        .filter(Boolean)
                        .map((text) => ` · ${text}`)}
                    </Note>
                  )}
                </>
              )}
            </Card>
          </AnnotationScope>
        </>
      )}
    />
  );
}
const styles = StyleSheet.create({
  content: {
    alignSelf: "center",
    gap: 16,
    maxWidth: 1200,
    paddingBottom: 48,
    width: "100%",
  },
  eyebrow: { fontFamily: "PlexMono", fontSize: 12 },
  list: { flex: 1 },
  masthead: {
    alignItems: "center",
    alignSelf: "center",
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 16,
    justifyContent: "space-between",
    maxWidth: 1200,
    paddingVertical: 16,
    width: "100%",
  },
  screen: { flex: 1, paddingHorizontal: 16 },
  title: {
    fontFamily: "ArchivoDisplay",
    fontSize: 44,
    letterSpacing: -1.6,
    lineHeight: 48,
    textTransform: "capitalize",
  },
});
