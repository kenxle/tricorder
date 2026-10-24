import { usePathname } from "expo-router";
import type { TabTriggerSlotProps } from "expo-router/ui";
import { Tabs, TabList, TabTrigger, TabSlot } from "expo-router/ui";
import type { ComponentProps } from "react";
import { Pressable, View, StyleSheet } from "react-native";

import { Body, useReadoutColors } from "../readout/ui";

export default function AppTabs() {
  const colors = useReadoutColors();
  const pathname = usePathname();
  return (
    <Tabs style={{ backgroundColor: colors.bg, flex: 1 }}>
      <TabList asChild>
        <View
          style={StyleSheet.flatten([
            styles.navigation,
            styles.bar,
            { borderBottomColor: colors.line },
          ])}
        >
          <Body style={styles.brand}>Tricorder</Body>
          <TabTrigger name="diligence" href="/diligence" asChild>
            <TabButton isFocused={pathname === "/diligence"}>Diligence</TabButton>
          </TabTrigger>
          <TabTrigger name="diligence-flow" href="/diligence-flow" asChild>
            <TabButton isFocused={pathname.startsWith("/diligence-")}>Diligence (native)</TabButton>
          </TabTrigger>
          <TabTrigger name="diligence-room" href="/diligence-room" style={{ display: "none" }} />
          <TabTrigger name="diligence-memo" href="/diligence-memo" style={{ display: "none" }} />
          <TabTrigger name="home" href="/" asChild>
            <TabButton isFocused={pathname === "/"}>Company</TabButton>
          </TabTrigger>
          <TabTrigger name="rooms" href="/rooms" asChild>
            <TabButton isFocused={pathname === "/rooms"}>Rooms</TabButton>
          </TabTrigger>
          <TabTrigger name="flow" href="/flow" asChild>
            <TabButton isFocused={pathname === "/flow"}>UX Flow</TabButton>
          </TabTrigger>
        </View>
      </TabList>
      <TabSlot style={{ flex: 1 }} />
    </Tabs>
  );
}

type TabButtonProps = Omit<TabTriggerSlotProps, "ref"> &
  Pick<ComponentProps<typeof Pressable>, "ref">;

export function TabButton({ children, isFocused, ...props }: TabButtonProps) {
  const colors = useReadoutColors();
  return (
    <Pressable
      {...props}
      accessibilityRole="tab"
      aria-selected={isFocused}
      accessibilityState={{ selected: isFocused }}
      style={({ pressed }) => [
        styles.tab,
        {
          borderBottomColor: isFocused ? colors.accent : "transparent",
          opacity: pressed ? 0.65 : 1,
        },
      ]}
    >
      <Body
        style={{
          color: isFocused ? colors.fg : colors.muted,
          fontFamily: isFocused ? "ArchivoBold" : "Archivo",
          fontSize: 14,
        }}
      >
        {children}
      </Body>
    </Pressable>
  );
}
const styles = StyleSheet.create({
  bar: {
    alignItems: "center",
    alignSelf: "center",
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 16,
    justifyContent: "space-between",
    maxWidth: 1200,
    width: "100%",
  },
  brand: {
    fontFamily: "ArchivoDisplay",
    fontSize: 20,
    letterSpacing: -0.6,
    marginRight: "auto",
  },
  navigation: { borderBottomWidth: 1, paddingHorizontal: 16 },
  tab: { borderBottomWidth: 2, justifyContent: "center", minHeight: 56 },
});
