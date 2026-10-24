// Steering on one statement: agree, disagree, ask or what-if. Kept on the page for now;
// the readout API's steering endpoint (readout/Steering.tsx) is not wired to room claims yet.
import { useState } from "react";
import { StyleSheet, TextInput, View } from "react-native";

import { Action, Note, Row, useReadoutColors } from "../readout/ui";

const styles = StyleSheet.create({
  input: {
    borderRadius: 8,
    borderWidth: 1,
    fontFamily: "Archivo",
    fontSize: 15,
    minHeight: 44,
    padding: 10,
  },
  wrap: { gap: 8 },
});

const MOVES = ["Agree", "Disagree", "Ask", "What if"] as const;
type Move = (typeof MOVES)[number];

export const SteerBar = ({ label }: { label: string }) => {
  const colors = useReadoutColors();
  const [move, setMove] = useState<Move | null>(null);
  const [text, setText] = useState("");
  const [saved, setSaved] = useState<string | null>(null);
  const needsText = move === "Ask" || move === "What if" || move === "Disagree";
  return (
    <View style={styles.wrap}>
      <Row>
        {MOVES.map((m) => (
          <Action
            key={m}
            onPress={() => {
              setMove(m);
              setSaved(m === "Agree" ? "You agreed." : null);
            }}
            primary={move === m}
            title={m}
          />
        ))}
      </Row>
      {needsText && !saved ? (
        <View style={styles.wrap}>
          <TextInput
            accessibilityLabel={`${move} on ${label}`}
            onChangeText={setText}
            placeholder={
              move === "What if"
                ? "What if the unsigned $2.75M never comes in?"
                : "Say why"
            }
            placeholderTextColor={colors.muted}
            style={[
              styles.input,
              { borderColor: colors.line, color: colors.fg },
            ]}
            value={text}
          />
          <Action
            disabled={text.trim() === ""}
            onPress={() => setSaved(`${move}: ${text.trim()}`)}
            title="Save"
          />
        </View>
      ) : null}
      {saved ? <Note>{saved}</Note> : null}
    </View>
  );
};
