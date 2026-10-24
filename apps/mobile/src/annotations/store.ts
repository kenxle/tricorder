import { createMMKV } from "react-native-mmkv";
import { useStore } from "zustand";

import { createAnnotationStore } from "./store-core";
import type { AnnotationState } from "./store-core";

const storage = createMMKV({ id: "tricorder.demo-annotations" });

export const annotationStore = createAnnotationStore({
  getItem: (name) => storage.getString(name) ?? null,
  setItem: (name, value) => storage.set(name, value),
});

export const useAnnotations = <T>(selector: (state: AnnotationState) => T): T =>
  useStore(annotationStore, selector);
