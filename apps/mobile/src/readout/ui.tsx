import {
  Button,
  Column,
  Host,
  Text as NativeText,
  TextInput as NativeTextInput,
  useNativeState,
} from "@expo/ui";
import type { TextInputProps as NativeTextInputProps } from "@expo/ui";
import { useEffect, useRef } from "react";
import type { PropsWithChildren } from "react";
import {
  Platform,
  TextInput as RNTextInput,
  ScrollView,
  StyleSheet,
  View,
} from "react-native";
import type {
  StyleProp,
  TextStyle,
  TextProps,
  ScrollViewProps,
} from "react-native";

import { AnnotatableText } from "../annotations/annotatable-text";
import { useReadoutColors } from "./colors";
import { actionModifiers, fieldModifiers } from "./native-modifiers";

export { useReadoutColors } from "./colors";

export function Body({ style, ...props }: TextProps) {
  const colors = useReadoutColors();
  return (
    <AnnotatableText
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
  compact = false,
}: {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  primary?: boolean;
  compact?: boolean;
}) {
  const colors = useReadoutColors();
  return (
    <Host
      matchContents={compact ? true : { vertical: true }}
      seedColor={colors.accent}
      style={{
        flexShrink: 1,
        minHeight: 44,
        width: compact ? undefined : "100%",
      }}
    >
      <Button
        modifiers={actionModifiers()}
        label={title}
        testID={title}
        disabled={disabled}
        onPress={onPress}
        variant={primary ? "filled" : "outlined"}
        style={{
          paddingHorizontal: 4,
          paddingVertical: 8,
          width: compact ? undefined : "100%",
        }}
      />
    </Host>
  );
}
type FieldProps = Omit<NativeTextInputProps, "value" | "style"> & {
  label: string;
  value?: string;
  style?: StyleProp<TextStyle>;
};

export function Field({
  label,
  value,
  defaultValue,
  onChangeText,
  style,
  ...props
}: FieldProps) {
  const colors = useReadoutColors();
  const text = useNativeState(value ?? defaultValue ?? "");
  const lastEdit = useRef(value ?? defaultValue ?? "");
  // Native typing owns its buffer. Only external resets/regeneration write back;
  // an echoed React update must not replace newer text or move the cursor.
  useEffect(() => {
    if (value !== undefined && value !== lastEdit.current) {
      lastEdit.current = value;
      text.set(value);
    }
  }, [text, value]);
  const inputStyle = StyleSheet.flatten(style);
  // SDK 58 universal web TextInput does not forward an accessible label.
  if (Platform.OS === "web") {
    return (
      <View style={{ gap: 8 }}>
        <Body style={{ fontSize: 15, fontWeight: "600" }}>{label}</Body>
        <RNTextInput
          accessibilityLabel={label}
          testID={props.testID ?? label}
          value={value}
          defaultValue={defaultValue}
          onChangeText={onChangeText}
          placeholder={props.placeholder}
          placeholderTextColor={colors.muted}
          multiline={props.multiline}
          numberOfLines={props.numberOfLines ?? (props.multiline ? 6 : 1)}
          maxLength={props.maxLength}
          editable={props.editable}
          autoFocus={props.autoFocus}
          autoCapitalize={props.autoCapitalize}
          autoCorrect={props.autoCorrect}
          keyboardType={props.keyboardType}
          returnKeyType={props.returnKeyType}
          onSubmitEditing={(event) =>
            props.onSubmitEditing?.(event.nativeEvent.text)
          }
          style={[
            {
              backgroundColor: colors.surface,
              borderColor: colors.line,
              borderRadius: 8,
              borderWidth: 1,
              color: colors.fg,
              fontSize: 17,
              minHeight: 48,
              padding: 12,
            },
            props.multiline && { minHeight: 144, textAlignVertical: "top" },
            style,
          ]}
        />
      </View>
    );
  }
  return (
    <Host matchContents={{ vertical: true }} seedColor={colors.accent}>
      <Column spacing={8} alignment="start" style={{ width: "100%" }}>
        <NativeText
          textStyle={{ color: colors.muted, fontSize: 15, fontWeight: "600" }}
        >
          {label}
        </NativeText>
        <NativeTextInput
          {...props}
          modifiers={[...(props.modifiers ?? []), ...fieldModifiers(label)]}
          testID={props.testID ?? label}
          value={text}
          placeholder={props.placeholder ?? label}
          placeholderTextColor={colors.muted}
          onChangeText={(next) => {
            lastEdit.current = next;
            onChangeText?.(next);
          }}
          numberOfLines={props.numberOfLines ?? (props.multiline ? 6 : 1)}
          style={{
            backgroundColor: colors.surface,
            borderRadius: 8,
            padding: 12,
            width: "100%",
          }}
          textStyle={{
            color: colors.fg,
            fontFamily: inputStyle?.fontFamily,
            fontSize: inputStyle?.fontSize ?? 17,
          }}
        />
      </Column>
    </Host>
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
  body: { flexShrink: 1, fontSize: 17, lineHeight: 24 },
  card: {
    borderRadius: 14,
    gap: 12,
    marginVertical: 8,
    padding: 20,
  },
  heading: {
    fontSize: 24,
    fontWeight: "700",
    letterSpacing: -0.4,
    lineHeight: 30,
    marginVertical: 8,
  },
  row: { alignItems: "center", flexDirection: "row", flexWrap: "wrap", gap: 8 },
});
