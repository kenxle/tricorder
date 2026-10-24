import { accessibilityLabel, controlSize } from "@expo/ui/swift-ui/modifiers";

export const actionModifiers = () => [controlSize("large")];
export const fieldModifiers = (label: string) => [accessibilityLabel(label)];
