// Weighted flags from the data room (Ken, 1:22 PM). Two disagreeing sources make a big red flag:
// heavy card, large title, one-line "why". Two agreeing sources make a small green flag: one
// compact line. Real strengths sit between, as a normal card.
import { StyleSheet, View } from "react-native";

import { Body, Note, useReadoutColors } from "../readout/ui";
import { MemoToggle } from "./diligence-bits";
import type { Room, RoomFlag, RoomSource, RoomValue } from "./room-data";
import { flagWeight, orderFlags, pieceLabel, sourceLabel } from "./room-data";

const styles = StyleSheet.create({
  ask: { gap: 4, marginTop: 4 },
  askLabel: { fontFamily: "PlexMono", fontSize: 12, letterSpacing: 1, textTransform: "uppercase" },
  bigCard: { borderRadius: 14, borderWidth: 3, gap: 12, marginVertical: 10, padding: 24 },
  bigTitle: { fontFamily: "ArchivoBold", fontSize: 24, lineHeight: 30 },
  chip: { alignSelf: "flex-start", borderRadius: 6, borderWidth: 1, paddingHorizontal: 8, paddingVertical: 2 },
  chipText: { fontFamily: "PlexMono", fontSize: 12, lineHeight: 18 },
  head: { alignItems: "center", flexDirection: "row", flexWrap: "wrap", gap: 8 },
  headlineCard: { borderRadius: 14, borderWidth: 1, gap: 10, marginVertical: 8, padding: 20 },
  headlineTitle: { fontFamily: "ArchivoBold", fontSize: 18, lineHeight: 24 },
  mark: { alignSelf: "flex-start", borderRadius: 999, borderWidth: 1, paddingHorizontal: 10, paddingVertical: 2 },
  markText: { fontFamily: "ArchivoBold", fontSize: 13, lineHeight: 20 },
  other: { alignItems: "center", flexDirection: "row", flexWrap: "wrap", gap: 8 },
  pair: { flexDirection: "row", flexWrap: "wrap", gap: 16 },
  pairCell: { flexBasis: 220, flexGrow: 1, gap: 4 },
  pairKey: { fontFamily: "PlexMono", fontSize: 12, textTransform: "uppercase" },
  pairValue: { fontFamily: "ArchivoBold", fontSize: 26, lineHeight: 32 },
  small: { alignItems: "center", borderBottomWidth: 1, flexDirection: "row", flexWrap: "wrap", gap: 8, paddingVertical: 4 },
  smallHead: { fontFamily: "ArchivoBold", marginTop: 8 },
  smallList: { gap: 2, marginTop: 8 },
  smallTitle: { flexShrink: 1, fontSize: 14, lineHeight: 20 },
  why: { fontSize: 14, lineHeight: 20 },
});

export const RoomChip = ({ source }: { source: RoomSource }) => {
  const colors = useReadoutColors();
  return (
    <View style={[styles.chip, { borderColor: colors.line }]}>
      <Body style={[styles.chipText, { color: colors.muted }]}>{sourceLabel(source)}</Body>
    </View>
  );
};

export const Mark = ({ tone, label }: { tone: "strong" | "weak" | "thin" | "gap"; label: string }) => {
  const colors = useReadoutColors();
  const color = { gap: colors.amber, strong: colors.green, thin: colors.muted, weak: colors.red }[tone];
  return (
    <View style={[styles.mark, { borderColor: color }]}>
      <Body style={[styles.markText, { color }]}>{label}</Body>
    </View>
  );
};

const Pair = ({ a, b }: { a: RoomValue; b: RoomValue }) => {
  const colors = useReadoutColors();
  return (
    <View style={styles.pair}>
      {[a, b].map((v) => (
        <View key={v.key} style={styles.pairCell}>
          <Note style={styles.pairKey}>{v.key}</Note>
          <Body style={[styles.pairValue, v.out ? { color: colors.red } : null]}>{v.value}</Body>
          <RoomChip source={v.source} />
        </View>
      ))}
    </View>
  );
};

export const BigFlag = ({ room, flag, company }: { room: Room; flag: RoomFlag; company?: string }) => {
  const colors = useReadoutColors();
  const big = flagWeight(flag) === "big";
  const red = flag.kind === "red";
  const cardStyle = big ? styles.bigCard : styles.headlineCard;
  return (
    <View style={[cardStyle, { backgroundColor: colors.surface, borderColor: big ? colors.red : colors.line }]}>
      <View style={styles.head}>
        <Mark label={red ? "Red flag" : "Green flag"} tone={red ? "weak" : "strong"} />
        <Note>{pieceLabel(room, flag.piece)}</Note>
        {company ? <MemoToggle company={company} pickKey={`flag:${flag.claim_id}`} /> : null}
      </View>
      <Body style={big ? styles.bigTitle : styles.headlineTitle}>{flag.title}</Body>
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
    </View>
  );
};

export const SmallFlag = ({ room, flag, company }: { room: Room; flag: RoomFlag; company?: string }) => {
  const colors = useReadoutColors();
  return (
    <View style={[styles.small, { borderColor: colors.line }]}>
      <Mark label="Small green flag" tone="strong" />
      <Body style={styles.smallTitle}>{flag.title}</Body>
      <Note style={styles.smallTitle}>{pieceLabel(room, flag.piece)}</Note>
      <RoomChip source={flag.stated.source} />
      <RoomChip source={flag.found.source} />
      {company ? <MemoToggle company={company} pickKey={`flag:${flag.claim_id}`} /> : null}
    </View>
  );
};

export const WeightedFlags = ({ room, flags, company }: { room: Room; flags: RoomFlag[]; company?: string }) => {
  const ordered = orderFlags(flags);
  const big = ordered.filter((f) => flagWeight(f) !== "small");
  const small = ordered.filter((f) => flagWeight(f) === "small");
  return (
    <View>
      {big.map((f) => (
        <BigFlag company={company} flag={f} key={f.claim_id} room={room} />
      ))}
      {small.length > 0 ? (
        <View style={styles.smallList}>
          <Note style={styles.smallHead}>Small green flags: sources that agree</Note>
          {small.map((f) => (
            <SmallFlag company={company} flag={f} key={f.claim_id} room={room} />
          ))}
        </View>
      ) : null}
    </View>
  );
};
