import { semantics } from "@expo/ui/jetpack-compose/modifiers";

export const actionModifiers = () => [];
export const fieldModifiers = (label: string) => [
  semantics({ contentDescription: label }),
];
