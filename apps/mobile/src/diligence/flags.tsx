// Weighted flags from the data room. Two disagreeing sources make a big red flag with a
// one-line "why"; two agreeing sources make a small green flag on one line.
import { StyleSheet, View } from "react-native";

import { Body, Card, Note, useReadoutColors } from "../readout/ui";
import type { Room, RoomFlag, RoomSource, RoomValue } from "./room-data";
import { flagWeight, orderFlags, pieceLabel, sourceLabel } from "./room-data";

export function RoomChip({ source }: { source: RoomSource }) {
  const colors = useReadoutColors();
  return (
    <View style={[styles.chip, { borderColor: colors.line }]}>
      <Body style={[styles.chipText, { color: colors.muted }]}>
        {sourceLabel(source)}
      </Body>
    </View>
  );
}

export function Mark({
  tone,
  label,
}: {
  tone: "strong" | "weak" | "thin" | "gap";
  label: string;
}) {
  const colors = useReadoutColors();
  const color = {
    gap: colors.amber,
    strong: colors.green,
    thin: colors.muted,
    weak: colors.red,
  }[tone];
  return (
    <View style={[styles.mark, { borderColor: color }]}>
      <Body style={[styles.markText, { color }]}>{label}</Body>
    </View>
  );
}

function Pair({ a, b }: { a: RoomValue; b: RoomValue }) {
  const colors = useReadoutColors();
  return (
    <View style={styles.pair}>
      {[a, b].map((v) => (
        <View key={v.key} style={styles.pairCell}>
          <Note style={styles.pairKey}>{v.key}</Note>
          <Body
            style={[styles.pairValue, v.out ? { color: colors.red } : null]}
          >
            {v.value}
          </Body>
          <RoomChip source={v.source} />
        </View>
      ))}
    </View>
  );
}

export function BigFlag({ room, flag }: { room: Room; flag: RoomFlag }) {
  const red = flag.kind === "red";
  return (
    <Card>
      <View style={styles.head}>
        <Mark
          label={red ? "Red flag" : "Green flag"}
          tone={red ? "weak" : "strong"}
        />
        <Note>{pieceLabel(room, flag.piece)}</Note>
      </View>
      <Body style={styles.title}>{flag.title}</Body>
      {flag.why ? <Note style={styles.why}>{flag.why}</Note> : null}
      <Pair a={flag.stated} b={flag.found} />
      {flag.others.map((o) => (
        <View key={o.key} style={styles.other}>
          <Note>
            {o.key}: {o.value}
          </Note>
          <RoomChip source={o.source} />
        </View>
      ))}
      {flag.ask ? (
        <View style={styles.ask}>
          <Note style={styles.askLabel}>Ask the founder</Note>
          <Body>{flag.ask}</Body>
        </View>
      ) : null}
    </Card>
  );
}

export function SmallFlag({ room, flag }: { room: Room; flag: RoomFlag }) {
  return (
    <View style={styles.small}>
      <Mark label="Small green flag" tone="strong" />
      <Body style={styles.smallTitle}>{flag.title}</Body>
      <Note>{pieceLabel(room, flag.piece)}</Note>
      <RoomChip source={flag.stated.source} />
      <RoomChip source={flag.found.source} />
    </View>
  );
}

export function WeightedFlags({
  room,
  flags,
}: {
  room: Room;
  flags: RoomFlag[];
}) {
  const ordered = orderFlags(flags);
  const big = ordered.filter((f) => flagWeight(f) !== "small");
  const small = ordered.filter((f) => flagWeight(f) === "small");
  return (
    <View>
      {big.map((f) => (
        <BigFlag flag={f} key={f.claim_id} room={room} />
      ))}
      {small.length > 0 ? (
        <View style={styles.smallList}>
          <Note style={styles.smallHead}>
            Small green flags: sources that agree
          </Note>
          {small.map((f) => (
            <SmallFlag flag={f} key={f.claim_id} room={room} />
          ))}
        </View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  ask: { gap: 4, marginTop: 4 },
  askLabel: {
    fontFamily: "PlexMono",
    fontSize: 12,
    letterSpacing: 1,
    textTransform: "uppercase",
  },
  chip: {
    alignSelf: "flex-start",
    borderRadius: 6,
    borderWidth: 1,
    paddingHorizontal: 8,
    paddingVertical: 2,
  },
  chipText: { fontFamily: "PlexMono", fontSize: 12, lineHeight: 18 },
  head: {
    alignItems: "center",
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
  },
  mark: {
    alignSelf: "flex-start",
    borderRadius: 999,
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 2,
  },
  markText: { fontFamily: "ArchivoBold", fontSize: 13, lineHeight: 20 },
  other: {
    alignItems: "center",
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
  },
  pair: { flexDirection: "row", flexWrap: "wrap", gap: 16 },
  pairCell: { flexBasis: 220, flexGrow: 1, gap: 4 },
  pairKey: { fontFamily: "PlexMono", fontSize: 12, textTransform: "uppercase" },
  pairValue: { fontFamily: "ArchivoBold", fontSize: 22, lineHeight: 28 },
  small: {
    alignItems: "center",
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
    paddingVertical: 6,
  },
  smallHead: { fontFamily: "ArchivoBold", marginTop: 8 },
  smallList: { gap: 4, marginTop: 8 },
  smallTitle: { fontSize: 15 },
  title: { fontFamily: "ArchivoBold", fontSize: 20, lineHeight: 26 },
  why: { fontSize: 13, lineHeight: 19 },
});
