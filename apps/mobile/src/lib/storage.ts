import { createMMKV } from "react-native-mmkv";

/** Shared storage for non-sensitive app preferences. */
export const storage = createMMKV({ id: "tricorder.preferences" });
