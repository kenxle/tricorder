import { BottomSheet, Host, RNHostView } from "@expo/ui";
import { interactiveDismissDisabled } from "@expo/ui/swift-ui/modifiers";
import type { PropsWithChildren } from "react";
import { View } from "react-native";

import { useReadoutColors } from "./colors";

// Keep RN virtualized lists and keyboard-aware forms inside a native presentation.
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
    <Host style={{ position: "absolute" }} seedColor={colors.accent}>
      <BottomSheet
        isPresented={visible}
        onDismiss={() => {
          if (!dismissalDisabled) {
            onClose();
          }
        }}
        snapPoints={["full"]}
        contentPadding={{ top: 12 }}
        containerColor={colors.bg}
        shouldDismissOnBackPress={!dismissalDisabled}
        shouldDismissOnClickOutside={!dismissalDisabled}
        modifiers={[interactiveDismissDisabled(dismissalDisabled)]}
      >
        <RNHostView style={{ height: "100%", width: "100%" }}>
          <View style={{ backgroundColor: colors.bg, flex: 1 }}>
            {children}
          </View>
        </RNHostView>
      </BottomSheet>
    </Host>
  );
};
