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
        amber: "#f0b44c",
        bg: "#111317",
        fg: "#e8eaed",
        green: "#5cc48d",
        line: "#424854",
        muted: "#9aa1ab",
        red: "#ff8a80",
      }
    : {
        amber: "#8a5a00",
        bg: "#ffffff",
        fg: "#16181d",
        green: "#1f7a4d",
        line: "#d1d5db",
        muted: "#5d6470",
        red: "#b3261e",
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
}: {
  title: string;
  onPress: () => void;
  disabled?: boolean;
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
          borderColor: colors.line,
          opacity: disabled ? 0.45 : pressed ? 0.65 : 1,
        },
      ]}
    >
      <Body selectable={false}>{title}</Body>
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
      <Body>{label}</Body>
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
    <View style={[styles.card, { borderColor: colors.line }]}>{children}</View>
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
  body: { flexShrink: 1, fontSize: 16, lineHeight: 24 },
  card: {
    borderRadius: 8,
    borderWidth: 1,
    gap: 10,
    marginVertical: 6,
    padding: 12,
  },
  field: { gap: 6 },
  heading: {
    fontSize: 20,
    fontWeight: "600",
    lineHeight: 28,
    marginVertical: 8,
  },
  input: {
    borderRadius: 8,
    borderWidth: 1,
    fontSize: 16,
    minHeight: 48,
    padding: 12,
  },
  row: { alignItems: "center", flexDirection: "row", flexWrap: "wrap", gap: 8 },
});
