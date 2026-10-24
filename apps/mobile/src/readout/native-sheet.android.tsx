import { Host, RNHostView } from "@expo/ui";
import { Column, ModalBottomSheet } from "@expo/ui/jetpack-compose";
import type { ModalBottomSheetRef } from "@expo/ui/jetpack-compose";
import { fillMaxSize, padding } from "@expo/ui/jetpack-compose/modifiers";
import type { PropsWithChildren } from "react";
import { useEffect, useRef, useState } from "react";
import { View } from "react-native";

import { useReadoutColors } from "./ui";

// The universal sheet does not expose Compose's swipe-dismiss guard.
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
  const sheet = useRef<ModalBottomSheetRef>(null);
  const [mounted, setMounted] = useState(visible);

  if (visible && !mounted) {
    setMounted(true);
  }

  useEffect(() => {
    if (visible) {
      // A quick reopen can arrive before the previous hide animation finishes.
      void sheet.current?.expand().catch(() => {
        // Closing or unmounting can cancel the native expansion animation.
      });
      return;
    }
    let cancelled = false;
    const finish = () => {
      if (!cancelled) {
        setMounted(false);
      }
    };
    if (sheet.current) {
      void sheet.current.hide().then(finish, finish);
    }
    return () => {
      cancelled = true;
    };
  }, [visible]);

  if (!mounted) {
    return null;
  }

  return (
    <Host style={{ position: "absolute" }} seedColor={colors.accent}>
      <ModalBottomSheet
        ref={sheet}
        onDismissRequest={() => {
          if (!dismissalDisabled) {
            onClose();
          }
        }}
        skipPartiallyExpanded
        sheetGesturesEnabled={!dismissalDisabled}
        properties={{
          shouldDismissOnBackPress: !dismissalDisabled,
          shouldDismissOnClickOutside: !dismissalDisabled,
        }}
        containerColor={colors.bg}
        contentColor={colors.fg}
      >
        <Column modifiers={[fillMaxSize(), padding(0, 12, 0, 0)]}>
          <RNHostView modifiers={[fillMaxSize()]}>
            <View style={{ backgroundColor: colors.bg, flex: 1 }}>
              {children}
            </View>
          </RNHostView>
        </Column>
      </ModalBottomSheet>
    </Host>
  );
};
