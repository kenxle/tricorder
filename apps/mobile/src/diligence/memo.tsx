// The memo for the partners: the associate's working page distilled into a document about the
// company and its investment case. Every statement drills down to its claims and their sources.
// No PDF. The associate sends it with a button; the partner view then opens (partner.tsx).
// Which flags and claims are in comes from the shared store in memo-picks.ts.
import { useState, useSyncExternalStore } from "react";
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
import { MemoToggle } from "./diligence-bits";
import { Mark, RoomChip, WeightedFlags } from "./flags";
import { getPick, listPicks, subscribePicks } from "./memo-picks";
import type { Room } from "./room-data";
import {
  ROOM_COMPANY,
  ROOM_SLUG,
  VERDICT_LABEL,
  flagsForState,
  sazabiRoom,
} from "./room-data";
import { ReportSection } from "./room-view";
import { SteerBar } from "./steering";

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

const claimKey = (id: string) => `roomclaim:${id}`;

// Flags use the store's default (in). A room claim is in unless the person took it out.
const useInMemo = (company: string) => {
  useSyncExternalStore(
    subscribePicks,
    () => JSON.stringify(listPicks(company)),
    () => ""
  );
  const set = new Map(listPicks(company).map((p) => [p.key, p.in]));
  return {
    claim: (id: string) => set.get(claimKey(id)) ?? true,
    flag: (id: string) => getPick(company, `flag:${id}`),
  };
};

const verdictTone = (v: string) => {
  if (v === "looking_strong") {
    return "strong";
  }
  return v === "looking_weak" ? "weak" : "gap";
};

const ClaimDrill = ({
  room,
  id,
  company,
}: {
  room: Room;
  id: string;
  company?: string;
}) => {
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
        {company ? (
          <MemoToggle company={company} pickKey={claimKey(id)} />
        ) : null}
      </Row>
      <Body>{c.text}</Body>
      <Row>
        {c.sources.map((s) => (
          <RoomChip key={`${s.uri}${s.locator}`} source={s} />
        ))}
      </Row>
      {c.agree?.length ? <Note>Agrees:</Note> : null}
      <Row>
        {(c.agree ?? []).map((s) => (
          <RoomChip key={`a${s.uri}${s.locator}`} source={s} />
        ))}
      </Row>
      {c.disagree?.length ? <Note>Differs:</Note> : null}
      <Row>
        {(c.disagree ?? []).map((s) => (
          <RoomChip key={`d${s.uri}${s.locator}`} source={s} />
        ))}
      </Row>
    </View>
  );
};

export const MemoDocument = ({
  room = sazabiRoom,
  company = ROOM_SLUG,
  steerable = true,
  editable = false,
  focus,
}: {
  room?: Room;
  company?: string;
  steerable?: boolean;
  editable?: boolean;
  focus?: string | null;
}) => {
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const inMemo = useInMemo(company);
  const toggle = (id: string) => setOpen((o) => ({ ...o, [id]: !o[id] }));
  const flags = flagsForState(room, "full").filter((f) =>
    inMemo.flag(f.claim_id)
  );
  const toggleCompany = editable ? company : undefined;
  return (
    <View style={styles.doc}>
      <Heading style={styles.company}>{ROOM_COMPANY}</Heading>
      <Body>{room.memo_company}</Body>
      <Note>
        {room.synthetic_notice} Data as of {room.as_of}.
      </Note>

      <Heading>What stands out</Heading>
      <WeightedFlags company={toggleCompany} flags={flags} room={room} />

      <Heading>Each piece of the company</Heading>
      {room.pieces.map((p) => {
        const ids = editable ? p.claim_ids : p.claim_ids.filter(inMemo.claim);
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
                tone={verdictTone(p.verdict)}
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
              ? ids.map((id) => (
                  <ClaimDrill
                    company={toggleCompany}
                    id={id}
                    key={id}
                    room={room}
                  />
                ))
              : null}
            {steerable ? <SteerBar label={p.label} /> : null}
          </Card>
        );
      })}

      {room.reports.map((r) => (
        <View key={r.key}>
          <ReportSection drill={toggle} report={r} />
          {r.paras
            .flatMap((p) => p.refs)
            .filter(
              (ref, i, all) =>
                all.indexOf(ref) === i && open[ref] && inMemo.claim(ref)
            )
            .map((ref) => (
              <ClaimDrill id={ref} key={ref} room={room} />
            ))}
        </View>
      ))}
    </View>
  );
};

export const MemoScreen = ({
  room = sazabiRoom,
  company = ROOM_SLUG,
  onSend,
  embedded = false,
}: {
  room?: Room;
  company?: string;
  onSend?: () => void;
  embedded?: boolean;
}) => {
  const colors = useReadoutColors();
  const send = onSend ? (
    <Action onPress={onSend} primary title="Send to the partners" />
  ) : null;
  const body = (
    <>
      <Row>{send}</Row>
      <MemoDocument company={company} editable room={room} />
      <Row>{send}</Row>
    </>
  );
  if (embedded) {
    return <View style={styles.doc}>{body}</View>;
  }
  return (
    <ScrollView
      contentContainerStyle={styles.page}
      style={{ backgroundColor: colors.bg }}
    >
      {body}
    </ScrollView>
  );
};
