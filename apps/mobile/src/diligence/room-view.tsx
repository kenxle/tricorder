// The working page once the founder's data room is in: partly in or fully in.
// What stands out leads with the room's weighted flags, then each piece's verdict,
// then the report sections with their charts.
import type { ReactNode } from "react";
import { ScrollView, StyleSheet, View } from "react-native";

import { Action, Body, Card, Heading, Note, Row, useReadoutColors } from "../readout/ui";
import { Mark, RoomChip, WeightedFlags } from "./flags";
import { RevenueBars, RunwayBars } from "./room-charts";
import type { Room, RoomReport, RoomStateName } from "./room-data";
import { ROOM_COMPANY, ROOM_SLUG, VERDICT_LABEL, flagsForState, pieceLabel, sazabiRoom, shortFile, subtitle } from "./room-data";

const styles = StyleSheet.create({
  banner: { alignItems: "center", flexDirection: "row", flexWrap: "wrap", gap: 10 },
  cardTitle: { fontFamily: "ArchivoBold", fontSize: 20, lineHeight: 26 },
  company: { fontSize: 34, lineHeight: 40 },
  lead: { fontFamily: "ArchivoBold" },
  page: { alignSelf: "center", gap: 12, maxWidth: 880, padding: 16, width: "100%" },
  para: { gap: 6 },
  stack: { gap: 12 },
  verdict: { borderBottomWidth: 1, gap: 6, paddingVertical: 12 },
});

const TONE: Record<string, "strong" | "weak" | "thin" | "gap"> = {
  looking_strong: "strong",
  looking_weak: "weak",
  mixed: "gap",
  not_enough_in_the_room: "thin",
};

export const ReportSection = ({ report, drill }: { report: RoomReport; drill?: (ref: string) => void }) => (
  <Card>
    <Body style={styles.cardTitle}>{report.title}</Body>
    <Note>Built from Kimmy's expert knowledge</Note>
    {report.chart?.kind === "revenue" ? <RevenueBars chart={report.chart} /> : null}
    {report.chart?.kind === "cash" ? <RunwayBars chart={report.chart} /> : null}
    {report.paras.map((p) => (
      <View key={p.lead} style={styles.para}>
        <Body>
          <Body style={styles.lead}>{p.lead} </Body>
          {p.body}
        </Body>
        {drill ? (
          <Row>
            {p.refs.map((r) => (
              <Action key={r} onPress={() => drill(r)} title={`Evidence ${r}`} />
            ))}
          </Row>
        ) : null}
      </View>
    ))}
  </Card>
);

const Scroller = ({ embedded, children }: { embedded: boolean; children: ReactNode }) => {
  const colors = useReadoutColors();
  if (embedded) {
    return <View style={styles.stack}>{children}</View>;
  }
  return (
    <ScrollView contentContainerStyle={styles.page} style={{ backgroundColor: colors.bg }}>
      {children}
    </ScrollView>
  );
};

export const RoomView = ({
  state,
  room = sazabiRoom,
  company = ROOM_SLUG,
  embedded = false,
  onSteer,
  onMemo,
  onFinalize,
}: {
  state: RoomStateName;
  room?: Room;
  company?: string;
  embedded?: boolean;
  onSteer?: () => void;
  onMemo?: () => void;
  onFinalize?: () => void;
}) => {
  const colors = useReadoutColors();
  const s = room.states[state];
  const banner =
    state === "partial"
      ? `${ROOM_COMPANY} shared part of its data room: ${s.arrived.length} of ${s.files_total} files. The rest is on the open requests.`
      : `${ROOM_COMPANY} shared its data room: all ${s.files_total} files are in.`;
  return (
    <Scroller embedded={embedded}>
      {embedded ? null : <Heading style={styles.company}>{ROOM_COMPANY}</Heading>}
      <View style={styles.banner}>
        <Mark label={state === "partial" ? "Partly in" : "Room in"} tone={state === "partial" ? "gap" : "strong"} />
        <Body>{banner}</Body>
      </View>
      <Note>
        {room.synthetic_notice} Data as of {room.as_of}.
      </Note>

      {state === "full" ? (
        <>
          <Heading>From Kimmy's expert knowledge</Heading>
          {room.reports.map((r) => (
            <ReportSection key={r.key} report={r} />
          ))}
        </>
      ) : null}

      <Heading>What stands out</Heading>
      <WeightedFlags company={company} flags={flagsForState(room, state)} room={room} />
      {s.waiting.map((w) => (
        <Card key={w.piece}>
          <Mark label={`Waiting on ${w.files.map(shortFile).join(", ")}`} tone="gap" />
          <Body style={styles.cardTitle}>{pieceLabel(room, w.piece)}</Body>
          <Note>{subtitle(w.title)}</Note>
          <Body>{w.text}</Body>
        </Card>
      ))}

      <Heading>Each piece of the company</Heading>
      {room.pieces.map((p) => {
        const v = s.pieces[p.name];
        if (!v) {
          return null;
        }
        return (
          <View key={p.name} style={[styles.verdict, { borderColor: colors.line }]}>
            <Row>
              <Body style={styles.cardTitle}>{p.label}</Body>
              <Mark label={VERDICT_LABEL[v.verdict] ?? v.verdict} tone={TONE[v.verdict] ?? "thin"} />
              <Note>
                {v.agree} agree, {v.disagree} differ
              </Note>
            </Row>
            <Body>{v.reason}</Body>
            {v.waiting.map((f) => (
              <RoomChip key={f} source={{ locator: "waiting", uri: f }} />
            ))}
          </View>
        );
      })}

      <Row>
        {onSteer ? <Action onPress={onSteer} title="Steer the readout" /> : null}
        {onMemo ? <Action onPress={onMemo} primary title="Make the memo" /> : null}
        {onFinalize ? <Action onPress={onFinalize} primary title="Finalize" /> : null}
      </Row>
    </Scroller>
  );
};
