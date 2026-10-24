import type { PropsWithChildren } from "react";
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  useColorScheme,
} from "react-native";
import type { TextInputProps, TextProps, ScrollViewProps } from "react-native";

export function useReadoutColors() {
  return useColorScheme() === "dark"
    ? {
        accent: "#d3bf8e",
        amber: "#d3bf8e",
        bg: "#131210",
        buttonBg: "#d3bf8e",
        buttonFg: "#16140f",
        fg: "#eeebe4",
        green: "#7dc4a0",
        line: "#45413a",
        muted: "#bdb7ab",
        red: "#f08c78",
        surface: "#1a1916",
      }
    : {
        accent: "#85692f",
        amber: "#85692f",
        bg: "#ffffff",
        buttonBg: "#1c1b18",
        buttonFg: "#eadbb4",
        fg: "#1c1b18",
        green: "#1e7550",
        line: "#cdc7ba",
        muted: "#47443d",
        red: "#b3402e",
        surface: "#ffffff",
      };
}
export function Body({ style, ...props }: TextProps) {
  const colors = useReadoutColors();
  return (
    <Text
      selectable
      {...props}
      style={[styles.body, { color: colors.fg }, style]}
    />
  );
}
export function Note({ style, ...props }: TextProps) {
  const colors = useReadoutColors();
  return (
    <Body {...props} style={[{ color: colors.muted, fontSize: 14 }, style]} />
  );
}
export function Heading({ style, ...props }: TextProps) {
  return (
    <Body
      accessibilityRole="header"
      {...props}
      style={[styles.heading, style]}
    />
  );
}
export function Action({
  title,
  onPress,
  disabled = false,
  primary = false,
}: {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  primary?: boolean;
}) {
  const colors = useReadoutColors();
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.action,
        {
          backgroundColor: primary ? colors.buttonBg : colors.surface,
          borderColor: colors.line,
          opacity: disabled ? 0.45 : pressed ? 0.65 : 1,
        },
      ]}
    >
      <Body
        selectable={false}
        style={{
          color: primary ? colors.buttonFg : colors.fg,
          fontFamily: "ArchivoBold",
          fontSize: 15,
        }}
      >
        {title}
      </Body>
    </Pressable>
  );
}
export function Field({
  label,
  style,
  ...props
}: TextInputProps & { label: string }) {
  const colors = useReadoutColors();
  return (
    <View style={styles.field}>
      <Body style={styles.label}>{label}</Body>
      <TextInput
        accessibilityLabel={label}
        placeholderTextColor={colors.muted}
        {...props}
        style={[
          styles.input,
          { borderColor: colors.line, color: colors.fg },
          props.multiline && { minHeight: 120, textAlignVertical: "top" },
          style,
        ]}
      />
    </View>
  );
}
export function Card({ children }: PropsWithChildren) {
  const colors = useReadoutColors();
  return (
    <View
      style={[
        styles.card,
        { backgroundColor: colors.surface, borderColor: colors.line },
      ]}
    >
      {children}
    </View>
  );
}
// Explicitly use the app ScrollView. The default FlatList renderer painted blank
// in this SDK 58 native development client; this preserves list virtualization.
export function renderReadoutScroll(props: ScrollViewProps) {
  return <ScrollView {...props} />;
}
export function Row({ children }: PropsWithChildren) {
  return <View style={styles.row}>{children}</View>;
}
const styles = StyleSheet.create({
  action: {
    alignSelf: "flex-start",
    borderRadius: 8,
    borderWidth: 1,
    justifyContent: "center",
    minHeight: 44,
    paddingHorizontal: 12,
    paddingVertical: 9,
  },
  body: { flexShrink: 1, fontFamily: "Archivo", fontSize: 16, lineHeight: 24 },
  card: {
    borderRadius: 14,
    borderWidth: 1,
    gap: 12,
    marginVertical: 8,
    padding: 24,
  },
  field: { gap: 6 },
  heading: {
    fontFamily: "ArchivoBold",
    fontSize: 24,
    letterSpacing: -0.4,
    lineHeight: 30,
    marginVertical: 8,
  },
  input: {
    borderRadius: 8,
    borderWidth: 1,
    fontFamily: "Archivo",
    fontSize: 16,
    minHeight: 48,
    padding: 12,
  },
  label: {
    fontFamily: "PlexMono",
    fontSize: 12,
    letterSpacing: 1,
    textTransform: "uppercase",
  },
  row: { alignItems: "center", flexDirection: "row", flexWrap: "wrap", gap: 8 },
});
