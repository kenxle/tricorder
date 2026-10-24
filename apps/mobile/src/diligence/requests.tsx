// The data-room request: a dialog over the working page (checklist, add an item, guidance
// per document, the live draft). After "Mark as sent" the working page lists each item as
// Open; the room arrives as a notification, and opening it marks the items it holds Answered.
import { useMemo, useState } from "react";
import { Modal, Pressable, ScrollView, View } from "react-native";

import { Action, Body, Card, Field, Heading, Note, Row, useReadoutColors } from "../readout/ui";
import { Mark } from "./diligence-bits";
import type { Research } from "./diligence-data";

export type RequestItem = {
  key: string;
  id?: string;
  title: string;
  ask: string;
  includes?: string;
  guidance?: { what: string; form: string; good: string[]; path: string };
  fromReadout: boolean;
  firstTier: boolean;
  custom?: boolean;
  reasons: string[];
  checked: boolean;
  askedAt?: Date;
};

export type RoomState = "none" | "shared" | "partial" | "more" | "full";

export function buildItems(r: Research): RequestItem[] {
  const byId = Object.fromEntries(r.checklist.map((c) => [c.id, c]));
  const items: RequestItem[] = [];
  for (const g of r.roomGaps) {
    for (const id of g.ids) {
      const c = byId[id];
      if (!c) continue;
      const have = items.find((x) => x.id === id);
      if (have) {
        have.reasons.push(g.text);
        continue;
      }
      items.push({ key: id, id, title: c.title, ask: c.ask, includes: c.includes, guidance: c.guidance,
        fromReadout: true, firstTier: c.stages.seed === "yes", reasons: [g.text], checked: true });
    }
  }
  for (const c of r.checklist) {
    if (c.kind !== "document" || c.stages.seed !== "yes") continue;
    const have = items.find((x) => x.id === c.id);
    if (have) {
      have.firstTier = true;
      continue;
    }
    items.push({ key: c.id, id: c.id, title: c.title, ask: c.ask, includes: c.includes, guidance: c.guidance,
      fromReadout: false, firstTier: true, reasons: [], checked: true });
  }
  return items;
}

function whenText(d: Date) {
  return d.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
}

export function draftText(r: Research, items: RequestItem[], by: Date) {
  const first = r.founder.split(",")[0].trim().split(/\s+/)[0] || "";
  const chosen = items.filter((i) => i.checked);
  const lines = [first ? `Hi ${first},` : "Hello,", "",
    `Thanks for talking with us about ${r.name}. Before our next meeting, could you set up a data room with the ${chosen.length === 1 ? "item" : "items"} below by ${whenText(by)}? A rough version is fine, and if something does not exist yet, just say so.`, ""];
  chosen.forEach((it, n) => {
    lines.push(`${n + 1}. ${it.ask}`);
    if (it.includes) lines.push(`   Ideally it includes ${it.includes}.`);
  });
  lines.push("", "Thanks,");
  return { subject: `${r.name}: a few things for a data room`, body: lines.join("\n") };
}

function ItemRow({ it, onToggle }: { it: RequestItem; onToggle: () => void }) {
  const c = useReadoutColors();
  const [open, setOpen] = useState(false);
  return (
    <View style={{ borderColor: c.line, borderTopWidth: 1, flexDirection: "row", gap: 12, paddingVertical: 10 }}>
      <Pressable
        accessibilityRole="checkbox"
        accessibilityState={{ checked: it.checked }}
        accessibilityLabel={`Ask for ${it.title}`}
        onPress={onToggle}
        style={{ alignItems: "center", borderColor: c.line, borderRadius: 4, borderWidth: 1, height: 24, justifyContent: "center", width: 24,
          backgroundColor: it.checked ? c.buttonBg : "transparent" }}
      >
        {it.checked ? <Body selectable={false} style={{ color: c.buttonFg, fontSize: 13 }}>✓</Body> : null}
      </Pressable>
      <View style={{ flex: 1, gap: 4 }}>
        <Body style={{ fontFamily: "ArchivoBold" }}>{it.title}</Body>
        <Body style={{ fontSize: 15 }}>{it.ask}</Body>
        <Row>
          {it.fromReadout ? <Mark label="From the readout" tone="amber" /> : null}
          {it.firstTier ? <Mark label="First tier at seed" /> : null}
          {it.custom ? <Mark label="Added by you" /> : null}
        </Row>
        {it.reasons.length ? <Note style={{ fontSize: 13 }}>{`For you, not sent: ${it.reasons.join(" ")}`}</Note> : null}
        {it.guidance ? (
          <>
            <Note onPress={() => setOpen(!open)} style={{ fontSize: 13, textDecorationLine: "underline" }}>
              {open ? "Hide guidance" : "Guidance for this document"}
            </Note>
            {open ? (
              <View style={{ gap: 4 }}>
                <Body style={{ fontSize: 14 }}><Body style={{ fontFamily: "ArchivoBold", fontSize: 14 }}>What it is. </Body>{it.guidance.what}</Body>
                <Body style={{ fontSize: 14 }}><Body style={{ fontFamily: "ArchivoBold", fontSize: 14 }}>Best form. </Body>{it.guidance.form}</Body>
                <Body style={{ fontFamily: "ArchivoBold", fontSize: 14 }}>A good one shows:</Body>
                {it.guidance.good.map((g) => <Body key={g} style={{ fontSize: 14 }}>{`· ${g}`}</Body>)}
              </View>
            ) : null}
          </>
        ) : null}
      </View>
    </View>
  );
}

export function RequestDialog({
  research,
  visible,
  items,
  setItems,
  onClose,
  onSent,
}: {
  research: Research;
  visible: boolean;
  items: RequestItem[];
  setItems: (items: RequestItem[]) => void;
  onClose: () => void;
  onSent: () => void;
}) {
  const c = useReadoutColors();
  const [extra, setExtra] = useState("");
  const by = useMemo(() => {
    const d = new Date();
    d.setDate(d.getDate() + 7);
    return d;
  }, []);
  const draft = draftText(research, items, by);
  const fromReadout = items.filter((i) => i.fromReadout).length;
  return (
    <Modal visible={visible} animationType="fade" transparent onRequestClose={onClose}>
      <View style={{ backgroundColor: "rgba(0,0,0,0.45)", flex: 1, padding: 16 }}>
        <View accessibilityViewIsModal style={{ alignSelf: "center", backgroundColor: c.bg, borderRadius: 14, flex: 1, maxWidth: 900, width: "100%" }}>
          <ScrollView contentContainerStyle={{ gap: 12, padding: 24 }}>
            <Row>
              <Heading style={{ flex: 1 }}>{`Data-room request for ${research.name}`}</Heading>
              <Action title="Close" onPress={onClose} />
            </Row>
            <Note>{`${items.filter((i) => i.checked).length} items selected · ${fromReadout} from the readout`}</Note>
            {items.map((it) => (
              <ItemRow key={it.key} it={it} onToggle={() => setItems(items.map((x) => (x.key === it.key ? { ...x, checked: !x.checked } : x)))} />
            ))}
            <Field label="Add an item" value={extra} onChangeText={setExtra} placeholder="Anything else to ask for" />
            <Action
              title="Add"
              disabled={!extra.trim()}
              onPress={() => {
                const t = extra.trim();
                setItems([...items, { key: `custom-${items.length}`, title: t, ask: t, fromReadout: false, firstTier: false, custom: true, reasons: [], checked: true }]);
                setExtra("");
              }}
            />
            <Card>
              <Note style={{ fontFamily: "PlexMono", fontSize: 11, textTransform: "uppercase" }}>Draft</Note>
              <Body style={{ fontFamily: "ArchivoBold" }}>{draft.subject}</Body>
              <Body style={{ fontSize: 15 }}>{draft.body}</Body>
            </Card>
            <Action title="Mark as sent" primary onPress={onSent} />
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
}

export function UpNextBox({ research, onDraft }: { research: Research; onDraft: () => void }) {
  return (
    <Card>
      <Heading>Up Next: Data Room Requests</Heading>
      {research.roomGaps.map((g) => (
        <Body key={g.text} style={{ fontSize: 15 }}>
          <Body style={{ fontFamily: "ArchivoBold", fontSize: 15 }}>{g.text} </Body>
          <Note style={{ fontSize: 14 }}>{g.why}</Note>
        </Body>
      ))}
      <Action title="Draft the data-room request" primary onPress={onDraft} />
    </Card>
  );
}

function answeredIds(r: Research, room: RoomState): string[] {
  if (room === "partial" || room === "more") return r.room.partial.answered;
  if (room === "full") return r.room.full.answered;
  return [];
}

export function RequestsBox({ research, items, room }: { research: Research; items: RequestItem[]; room: RoomState }) {
  const asked = items.filter((i) => i.checked);
  const answered = new Set(answeredIds(research, room));
  const openCount = asked.filter((i) => !(i.id && answered.has(i.id))).length;
  return (
    <Card>
      <Heading>Data room requests</Heading>
      <Note>
        {`${asked.length} items asked for, ${openCount} open. Request sent to ${research.founder}`}
        {room === "none" || room === "shared" ? ` · waiting for ${research.name}'s data room` : ""}
      </Note>
      {asked.map((it) => {
        const done = !!(it.id && answered.has(it.id));
        const files = done && it.id ? research.room.holds[it.id] ?? [] : [];
        return (
          <Row key={it.key}>
            <Mark label={done ? "Answered" : "Open"} tone={done ? "green" : "plain"} />
            <View style={{ flex: 1 }}>
              <Body style={{ fontFamily: "ArchivoBold", fontSize: 15 }}>{it.title}</Body>
              <Note style={{ fontSize: 13 }}>
                {done ? files.join(", ") : `Asked ${it.askedAt ? it.askedAt.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) : ""}`}
              </Note>
            </View>
          </Row>
        );
      })}
    </Card>
  );
}

export function RoomNotice({ title, onOpen }: { title: string; onOpen: () => void }) {
  return (
    <Card>
      <Row>
        <Body style={{ flex: 1, fontFamily: "ArchivoBold" }}>{`${title} · just now`}</Body>
        <Action title="Open the data room" primary onPress={onOpen} />
      </Row>
    </Card>
  );
}
