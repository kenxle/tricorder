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
  Row,
  useReadoutColors,
} from "../readout/ui";
import type { MemoPicks } from "./memo";
import { MemoDocument } from "./memo";
import type { Room } from "./room-data";
import { ROOM_COMPANY, sazabiRoom } from "./room-data";

interface Answer {
  question: string;
  hits: { piece: string; label: string; text: string }[];
}

const WORD = /[a-z0-9$%.]+/g;

export function answerFromMemo(room: Room, question: string): Answer {
  const words = (question.toLowerCase().match(WORD) ?? []).filter(
    (w) => w.length > 3
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
  const scored = statements
    .map((s) => {
      const hay = `${s.label} ${s.text}`.toLowerCase();
      return { s, score: words.filter((w) => hay.includes(w)).length };
    })
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map((x) => x.s);
  return { hits: scored, question };
}

export function PartnerChat({
  room,
  onFocus,
}: {
  room: Room;
  onFocus: (piece: string) => void;
}) {
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
        <View key={`${i}-${a.question}`} style={styles.turn}>
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
}

export function PartnerScreen({
  room = sazabiRoom,
  picks,
}: {
  room?: Room;
  picks?: MemoPicks;
}) {
  const colors = useReadoutColors();
  const [focus, setFocus] = useState<string | null>(null);
  return (
    <ScrollView
      contentContainerStyle={styles.page}
      style={{ backgroundColor: colors.bg }}
    >
      <Row>
        <Heading>Memo from the associate: {ROOM_COMPANY}</Heading>
      </Row>
      <PartnerChat onFocus={setFocus} room={room} />
      <MemoDocument focus={focus} picks={picks} room={room} />
    </ScrollView>
  );
}

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
  title: { fontFamily: "ArchivoBold", fontSize: 20, lineHeight: 26 },
  turn: { gap: 6 },
  where: { fontFamily: "PlexMono", fontSize: 12, textTransform: "uppercase" },
});
