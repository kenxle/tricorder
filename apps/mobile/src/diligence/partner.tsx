// The partner reviewing the memo the associate sent, with a chat that helps them navigate it.
// The chat answers by pointing at statements in the memo. It searches the memo on the page;
// Benjamin's chat endpoint can replace answerFromMemo when it lands.
import { useState } from "react";
import { ScrollView, StyleSheet, TextInput, View } from "react-native";

import {
  Action,
  Body,
  Card,
  Heading,
  Note,
  useReadoutColors,
} from "../readout/ui";
import { MemoDocument } from "./memo";
import type { Room } from "./room-data";
import { ROOM_COMPANY, ROOM_SLUG, sazabiRoom } from "./room-data";

const styles = StyleSheet.create({
  hit: { borderRadius: 8, borderWidth: 1, gap: 4, padding: 10 },
  input: {
    borderRadius: 8,
    borderWidth: 1,
    fontFamily: "Archivo",
    fontSize: 15,
    minHeight: 44,
    padding: 10,
  },
  page: {
    alignSelf: "center",
    gap: 12,
    maxWidth: 880,
    padding: 16,
    width: "100%",
  },
  q: { fontFamily: "ArchivoBold" },
  stack: { gap: 12 },
  title: { fontFamily: "ArchivoBold", fontSize: 20, lineHeight: 26 },
  turn: { gap: 6 },
  where: { fontFamily: "PlexMono", fontSize: 12, textTransform: "uppercase" },
});

interface Answer {
  question: string;
  hits: { piece: string; label: string; text: string }[];
}

const WORD = /[a-z0-9$%.]+/gu;
const MIN_WORD = 4;
const MAX_HITS = 3;

export const answerFromMemo = (room: Room, question: string): Answer => {
  const words = (question.toLowerCase().match(WORD) ?? []).filter(
    (w) => w.length >= MIN_WORD
  );
  const statements = [
    ...room.pieces.map((p) => ({
      label: p.label,
      piece: p.name,
      text: p.reason,
    })),
    ...room.reports.flatMap((r) =>
      r.paras.map((p) => ({
        label: r.title,
        piece: r.key,
        text: `${p.lead} ${p.body}`,
      }))
    ),
  ];
  const hits = statements
    .map((s) => {
      const hay = `${s.label} ${s.text}`.toLowerCase();
      return { s, score: words.filter((w) => hay.includes(w)).length };
    })
    .filter((x) => x.score > 0)
    .toSorted((a, b) => b.score - a.score)
    .slice(0, MAX_HITS)
    .map((x) => x.s);
  return { hits, question };
};

export const PartnerChat = ({
  room,
  onFocus,
}: {
  room: Room;
  onFocus: (piece: string) => void;
}) => {
  const colors = useReadoutColors();
  const [q, setQ] = useState("");
  const [answers, setAnswers] = useState<Answer[]>([]);
  const ask = () => {
    if (q.trim() === "") {
      return;
    }
    setAnswers((a) => [...a, answerFromMemo(room, q)]);
    setQ("");
  };
  return (
    <Card>
      <Body style={styles.title}>Ask about the memo</Body>
      {answers.map((a, i) => (
        <View key={`${String(i)}-${a.question}`} style={styles.turn}>
          <Body style={styles.q}>{a.question}</Body>
          {a.hits.length === 0 ? (
            <Note>The memo does not cover that yet.</Note>
          ) : null}
          {a.hits.map((h) => (
            <View
              key={`${h.piece}${h.text}`}
              style={[styles.hit, { borderColor: colors.line }]}
            >
              <Note style={styles.where}>{h.label}</Note>
              <Body>{h.text}</Body>
              <Action
                onPress={() => onFocus(h.piece)}
                title="Go to it in the memo"
              />
            </View>
          ))}
        </View>
      ))}
      <TextInput
        accessibilityLabel="Ask about the memo"
        onChangeText={setQ}
        onSubmitEditing={ask}
        placeholder="How much of the seed is signed?"
        placeholderTextColor={colors.muted}
        style={[styles.input, { borderColor: colors.line, color: colors.fg }]}
        value={q}
      />
      <Action disabled={q.trim() === ""} onPress={ask} primary title="Ask" />
    </Card>
  );
};

export const PartnerScreen = ({
  room = sazabiRoom,
  company = ROOM_SLUG,
  embedded = false,
}: {
  room?: Room;
  company?: string;
  embedded?: boolean;
}) => {
  const colors = useReadoutColors();
  const [focus, setFocus] = useState<string | null>(null);
  const body = (
    <>
      <Heading>Memo from the associate: {ROOM_COMPANY}</Heading>
      <PartnerChat onFocus={setFocus} room={room} />
      <MemoDocument company={company} focus={focus} room={room} />
    </>
  );
  if (embedded) {
    return <View style={styles.stack}>{body}</View>;
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
