import { Host } from "@expo/ui";
import { Rectangle } from "@expo/ui/swift-ui";
import { foregroundStyle } from "@expo/ui/swift-ui/modifiers";
import { StyleSheet, View } from "react-native";

export const CardGradient = ({ colors }: { colors: string[] }) => (
  <View pointerEvents="none" accessible={false} style={StyleSheet.absoluteFill}>
    <Host style={StyleSheet.absoluteFill}>
      <Rectangle
        modifiers={[
          foregroundStyle({
            colors,
            endPoint: { x: 1, y: 1 },
            startPoint: { x: 0, y: 0 },
            type: "linearGradient",
          }),
        ]}
      />
    </Host>
  </View>
);
