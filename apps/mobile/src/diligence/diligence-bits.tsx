// Small shared pieces of the diligence screens: marks, the source button, evidence numbers,
// the "In memo" toggle and the loading skeleton. Built on the readout ui.tsx primitives.
import { Linking, Pressable, View } from "react-native";

import { Body, Note, useReadoutColors } from "../readout/ui";
import type { Research } from "./diligence-data";
import { useMemoPick } from "./memo-picks";

export const MARKS: Record<string, string> = {
  strong: "Looking strong",
  weak: "Looking weak",
  mixed: "Mixed",
  thin: "Not enough yet",
};

export function Mark({ label, tone }: { label: string; tone?: "green" | "red" | "amber" | "plain" }) {
  const c = useReadoutColors();
  const color =
    tone === "green" ? c.green : tone === "red" ? c.red : tone === "amber" ? c.amber : c.muted;
  return (
    <View style={{ borderColor: color, borderWidth: 1, borderRadius: 4, paddingHorizontal: 6, paddingVertical: 1 }}>
      <Body selectable={false} style={{ color, fontFamily: "PlexMono", fontSize: 11, letterSpacing: 0.6, lineHeight: 18, textTransform: "uppercase" }}>
        {label}
      </Body>
    </View>
  );
}

export function markTone(mark: string) {
  return mark === "strong" ? "green" : mark === "weak" ? "red" : mark === "mixed" ? "amber" : "plain";
}

export function SourceButton({ research, sourceId, url }: { research: Research; sourceId?: string; url?: string }) {
  const c = useReadoutColors();
  const src = sourceId ? research.sources[sourceId] : undefined;
  const href = url || src?.url || undefined;
  const label = src?.title || sourceId || "Source";
  return (
    <Pressable
      accessibilityRole="link"
      accessibilityLabel={`Source: ${label}`}
      disabled={!href}
      onPress={() => href && Linking.openURL(href)}
      style={({ pressed }) => ({
        alignSelf: "flex-start",
        borderColor: c.line,
        borderRadius: 6,
        borderWidth: 1,
        opacity: pressed ? 0.6 : 1,
        paddingHorizontal: 8,
        paddingVertical: 3,
      })}
    >
      <Body selectable={false} numberOfLines={2} style={{ fontSize: 12, lineHeight: 18, fontFamily: "ArchivoBold" }}>
        {label}
      </Body>
    </Pressable>
  );
}

export function EvRef({ n, onPress }: { n: number; onPress: (n: number) => void }) {
  const c = useReadoutColors();
  return (
    <Pressable accessibilityRole="button" accessibilityLabel={`Evidence ${n}`} onPress={() => onPress(n)}>
      <Body selectable={false} style={{ color: c.accent, fontFamily: "PlexMono", fontSize: 13, textDecorationLine: "underline" }}>
        {n}
      </Body>
    </Pressable>
  );
}

export function MemoToggle({ company, pickKey }: { company: string; pickKey: string }) {
  const c = useReadoutColors();
  const [on, toggle] = useMemoPick(company, pickKey);
  return (
    <Pressable
      accessibilityRole="checkbox"
      accessibilityState={{ checked: on }}
      accessibilityLabel="In memo"
      onPress={toggle}
      style={{ alignItems: "center", flexDirection: "row", gap: 6, minHeight: 32 }}
    >
      <View
        style={{
          alignItems: "center",
          backgroundColor: on ? c.buttonBg : "transparent",
          borderColor: on ? c.buttonBg : c.line,
          borderRadius: 3,
          borderWidth: 1,
          height: 16,
          justifyContent: "center",
          width: 16,
        }}
      >
        {on ? <Body selectable={false} style={{ color: c.buttonFg, fontSize: 11, lineHeight: 14 }}>✓</Body> : null}
      </View>
      <Note selectable={false} style={{ fontSize: 12 }}>In memo</Note>
    </Pressable>
  );
}

export function Skeleton() {
  const c = useReadoutColors();
  return (
    <View accessibilityElementsHidden importantForAccessibility="no-hide-descendants" style={{ gap: 8, paddingVertical: 6 }}>
      {[92, 78, 64].map((w) => (
        <View key={w} style={{ backgroundColor: c.line, borderRadius: 4, height: 12, opacity: 0.5, width: `${w}%` }} />
      ))}
    </View>
  );
}
