import type { CompanyEvidence } from "@tricorder/schema/company";
import { Fragment } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import type { StyleProp, TextStyle } from "react-native";

import { Body, useReadoutColors } from "../readout/ui";

const styles = StyleSheet.create({
  link: {
    alignItems: "center",
    justifyContent: "center",
    minHeight: 32,
    minWidth: 42,
    paddingHorizontal: 3,
  },
  number: { fontSize: 14, fontWeight: "700", lineHeight: 22 },
});

// Inline RN attachments keep citations in the paragraph; Expo UI Text accepts
// strings only. The visible link plus hitSlop gives a 44-point touch height.
export const CitedText = ({
  segments,
  evidence,
  onOpen,
  style,
}: {
  segments: { text: string; evidenceIds: string[] }[];
  evidence: Record<string, CompanyEvidence>;
  onOpen: (entry: CompanyEvidence) => void;
  style?: StyleProp<TextStyle>;
}) => {
  const colors = useReadoutColors();
  const sourceIds = [...new Set(segments.flatMap((part) => part.evidenceIds))];
  return (
    <Body
      accessibilityLabel={segments.map((part) => part.text).join("")}
      accessibilityHint="Use the source actions to open the evidence for this passage."
      accessibilityActions={sourceIds.flatMap((id) => {
        const entry = evidence[id];
        return entry
          ? [
              {
                label: `Source ${entry.number}: ${entry.sourceTitle}`,
                name: id,
              },
            ]
          : [];
      })}
      onAccessibilityAction={({ nativeEvent }) => {
        const entry = evidence[nativeEvent.actionName];
        if (entry && sourceIds.includes(entry.id)) {
          onOpen(entry);
        }
      }}
      style={style}
    >
      {segments.map((segment, index) => (
        <Fragment key={`${index}:${segment.text}`}>
          <Text accessible>{segment.text}</Text>
          {segment.evidenceIds.map((id) => {
            const entry = evidence[id];
            return entry ? (
              <Pressable
                key={id}
                nativeID={`source-citation:${entry.id}:${index}`}
                testID={`source-citation:${entry.id}:${index}`}
                accessibilityRole="link"
                accessibilityLabel={`Source ${entry.number}: ${entry.sourceTitle}. For: ${segment.text.trim()}`}
                accessibilityHint="Opens the saved evidence and original source link."
                hitSlop={{ bottom: 6, left: 4, right: 4, top: 6 }}
                onPress={() => onOpen(entry)}
                style={styles.link}
              >
                {({ pressed }) => (
                  <View
                    style={{
                      backgroundColor: colors.surface,
                      borderRadius: 8,
                      justifyContent: "center",
                      minHeight: 32,
                      paddingHorizontal: 8,
                    }}
                  >
                    <Text
                      style={[
                        styles.number,
                        { color: pressed ? colors.fg : colors.accent },
                      ]}
                    >
                      {`[${entry.number}]`}
                    </Text>
                  </View>
                )}
              </Pressable>
            ) : (
              <Text key={id} style={{ color: colors.muted }}>
                {" [source unavailable]"}
              </Text>
            );
          })}
        </Fragment>
      ))}
    </Body>
  );
};
