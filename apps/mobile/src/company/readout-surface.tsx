import { Column, Host, RNHostView } from "@expo/ui";
import type { CompanyInsight } from "@tricorder/schema/company";
import type { PropsWithChildren } from "react";
import { useColorScheme, View } from "react-native";

import { Note, useReadoutColors } from "../readout/ui";
import { CardGradient } from "./card-gradient";

// Reuse the carousel’s native gradient surface. Let RN measure rich prose
// directly so callouts and annotation controls expand with their content.
export const ReadoutSurface = ({ children }: PropsWithChildren) => {
  const colors = useReadoutColors();
  const dark = useColorScheme() === "dark";
  return (
    <View
      style={{
        backgroundColor: colors.surface,
        borderColor: colors.line,
        borderRadius: 32,
        borderWidth: 1,
        boxShadow: [
          {
            blurRadius: 24,
            color: dark ? "rgba(0, 0, 0, 0.28)" : "rgba(52, 41, 28, 0.14)",
            offsetX: 0,
            offsetY: 10,
            spreadDistance: -6,
          },
          {
            blurRadius: 6,
            color: dark ? "rgba(0, 0, 0, 0.18)" : "rgba(52, 41, 28, 0.06)",
            offsetX: 0,
            offsetY: 2,
            spreadDistance: -2,
          },
        ],
      }}
    >
      <View
        pointerEvents="none"
        style={{
          borderRadius: 31,
          bottom: 0,
          left: 0,
          overflow: "hidden",
          position: "absolute",
          right: 0,
          top: 0,
        }}
      >
        <CardGradient
          colors={
            dark
              ? ["#343027", "#1a1916", "#24211b"]
              : ["#f7f2e6", "#e5d7bc", "#fbfaf7"]
          }
        />
      </View>
      <View style={{ gap: 16, padding: 24 }}>{children}</View>
    </View>
  );
};

const marks = {
  mixed: {
    dark: ["#93b2e6", "#292b2f"],
    label: "Mixed",
    light: ["#2d5c9c", "#eef2f7"],
  },
  strong: {
    dark: ["#7dc4a0", "#262e27"],
    label: "Looking strong",
    light: ["#1e7550", "#edf4f1"],
  },
  thin: {
    dark: ["#aaa498", "#282723"],
    label: "Not enough yet",
    light: ["#6b675e", "#f3f3f2"],
  },
  weak: {
    dark: ["#f08c78", "#342722"],
    label: "Looking weak",
    light: ["#b3402e", "#f9f0ee"],
  },
} as const;

export const InsightMark = ({ mark }: { mark: CompanyInsight["mark"] }) => {
  const scheme = useColorScheme();
  const entry = marks[mark];
  const [color, backgroundColor] = entry[scheme === "dark" ? "dark" : "light"];
  return (
    <Host matchContents style={{ alignSelf: "flex-start", maxWidth: "100%" }}>
      <Column
        style={{
          backgroundColor,
          borderRadius: 14,
          paddingHorizontal: 12,
          paddingVertical: 6,
        }}
      >
        <RNHostView matchContents>
          <Note
            style={{
              color,
              fontFamily: undefined,
              fontSize: 14,
              fontWeight: "600",
              lineHeight: 20,
            }}
          >
            {entry.label}
          </Note>
        </RNHostView>
      </Column>
    </Host>
  );
};
