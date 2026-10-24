import { Host } from "@expo/ui";
import { BottomSheet } from "@expo/ui/community/bottom-sheet";
import type { PropsWithChildren } from "react";
import { View } from "react-native";

import { useReadoutColors } from "./colors";

// The universal web sheet cannot disable dismissal; the Expo compatibility
// layer forwards this guard to its dialog, including drag, backdrop and Escape.
export const NativeSheet = ({
  visible,
  onClose,
  dismissalDisabled = false,
  children,
}: PropsWithChildren<{
  visible: boolean;
  onClose: () => void;
  dismissalDisabled?: boolean;
}>) => {
  const colors = useReadoutColors();
  return (
    <Host>
      <BottomSheet
        index={visible ? 0 : -1}
        snapPoints={["100%"]}
        enablePanDownToClose={!dismissalDisabled}
        backgroundStyle={{ backgroundColor: colors.bg }}
        onClose={() => {
          if (visible && !dismissalDisabled) {
            onClose();
          }
        }}
      >
        <View style={{ backgroundColor: colors.bg, flex: 1, height: "100%" }}>
          {children}
        </View>
      </BottomSheet>
    </Host>
  );
};
