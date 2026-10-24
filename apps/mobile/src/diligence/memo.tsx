// The memo for the partners: the associate's working page distilled into a document about the
// company and its investment case. Every statement drills down to its claims and their sources.
// No PDF. The associate sends it with a button; the partner view then opens (partner.tsx).
import { useState } from "react";
import { ScrollView, StyleSheet, View } from "react-native";

import {
  Action,
  Body,
  Card,
  Heading,
  Note,
  Row,
  useReadoutColors,
} from "../readout/ui";
import { Mark, RoomChip, WeightedFlags } from "./flags";
import type { Room } from "./room-data";
import {
  ROOM_COMPANY,
  VERDICT_LABEL,
  flagsForState,
  sazabiRoom,
} from "./room-data";
import { ReportSection } from "./room-view";
import { SteerBar } from "./steering";

// Hook for memo-picks.ts (owned by the start/requests agent): pass the picked claim ids and the
// memo keeps only those. Undefined means every claim is in.
export type MemoPicks = readonly string[] | undefined;

function ClaimDrill({ room, id }: { room: Room; id: string }) {
  const colors = useReadoutColors();
  const c = room.claims[id];
  if (!c) {
    return null;
  }
  return (
    <View style={[styles.drill, { borderColor: colors.line }]}>
      <Row>
        <Note style={styles.mono}>{id}</Note>
        {c.mark ? (
          <Mark
            label={c.mark}
            tone={c.mark === "contradicted" ? "weak" : "strong"}
          />
        ) : null}
      </Row>
      <Body>{c.text}</Body>
      <Row>
        {c.sources.map((s) => (
          <RoomChip key={`${s.uri}${s.locator}`} source={s} />
        ))}
      </Row>
      {c.agree?.length ? <Note>Agrees: </Note> : null}
      <Row>
        {(c.agree ?? []).map((s) => (
          <RoomChip key={`a${s.uri}${s.locator}`} source={s} />
        ))}
      </Row>
      {c.disagree?.length ? <Note>Differs: </Note> : null}
      <Row>
        {(c.disagree ?? []).map((s) => (
          <RoomChip key={`d${s.uri}${s.locator}`} source={s} />
        ))}
      </Row>
    </View>
  );
}

export function MemoDocument({
  room = sazabiRoom,
  picks,
  steerable = true,
  focus,
}: {
  room?: Room;
  picks?: MemoPicks;
  steerable?: boolean;
  focus?: string | null;
}) {
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const picked = (id: string) => !picks || picks.includes(id);
  const toggle = (id: string) => setOpen((o) => ({ ...o, [id]: !o[id] }));
  const flags = flagsForState(room, "full").filter((f) => picked(f.claim_id));
  return (
    <View style={styles.doc}>
      <Heading style={styles.company}>{ROOM_COMPANY}</Heading>
      <Body>{room.memo_company}</Body>
      <Note>
        {room.synthetic_notice} Data as of {room.as_of}.
      </Note>

      <Heading>What stands out</Heading>
      <WeightedFlags flags={flags} room={room} />

      <Heading>Each piece of the company</Heading>
      {room.pieces.map((p) => {
        const ids = p.claim_ids.filter(picked);
        const key = `piece-${p.name}`;
        return (
          <Card key={p.name}>
            <Row>
              <Body
                style={[styles.title, focus === p.name ? styles.focus : null]}
              >
                {p.label}
              </Body>
              <Mark
                label={VERDICT_LABEL[p.verdict] ?? p.verdict}
                tone={
                  p.verdict === "looking_strong"
                    ? "strong"
                    : p.verdict === "looking_weak"
                      ? "weak"
                      : "gap"
                }
              />
            </Row>
            <Body>{p.reason}</Body>
            <Action
              onPress={() => toggle(key)}
              title={
                open[key]
                  ? "Hide the evidence"
                  : `Show the evidence (${ids.length})`
              }
            />
            {open[key]
              ? ids.map((id) => <ClaimDrill id={id} key={id} room={room} />)
              : null}
            {steerable ? <SteerBar label={p.label} /> : null}
          </Card>
        );
      })}

      {room.reports.map((r) => (
        <View key={r.key}>
          <ReportSection drill={(ref) => toggle(ref)} report={r} />
          {r.paras
            .flatMap((p) => p.refs)
            .filter(
              (ref, i, all) =>
                all.indexOf(ref) === i && open[ref] && picked(ref)
            )
            .map((ref) => (
              <ClaimDrill id={ref} key={ref} room={room} />
            ))}
        </View>
      ))}
    </View>
  );
}

export function MemoScreen({
  room = sazabiRoom,
  picks,
  onSend,
}: {
  room?: Room;
  picks?: MemoPicks;
  onSend?: () => void;
}) {
  const colors = useReadoutColors();
  return (
    <ScrollView
      contentContainerStyle={styles.page}
      style={{ backgroundColor: colors.bg }}
    >
      <Row>
        {onSend ? (
          <Action onPress={onSend} primary title="Send to the partners" />
        ) : null}
      </Row>
      <MemoDocument picks={picks} room={room} />
      <Row>
        {onSend ? (
          <Action onPress={onSend} primary title="Send to the partners" />
        ) : null}
      </Row>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  company: { fontSize: 34, lineHeight: 40 },
  doc: { gap: 12 },
  drill: { borderRadius: 8, borderWidth: 1, gap: 6, padding: 12 },
  focus: { textDecorationLine: "underline" },
  mono: { fontFamily: "PlexMono", fontSize: 12 },
  page: {
    alignSelf: "center",
    gap: 12,
    maxWidth: 880,
    padding: 16,
    width: "100%",
  },
  title: { fontFamily: "ArchivoBold", fontSize: 20, lineHeight: 26 },
});
