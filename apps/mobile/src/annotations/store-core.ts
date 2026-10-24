import { createStore } from "zustand/vanilla";

import {
  annotationInputSchema,
  personas,
  savedAnnotationsSchema,
} from "./model.ts";
import type { Annotation, AnnotationInput } from "./model.ts";

export interface AnnotationStorage {
  getItem: (name: string) => string | null;
  setItem: (name: string, value: string) => void;
}

export interface AnnotationState {
  personaId: string;
  annotations: Annotation[];
  storageError: string | null;
  selectingText: boolean;
  setSelectingText: (selecting: boolean) => void;
  setPersona: (id: string) => void;
  addAnnotation: (input: AnnotationInput) => boolean;
}

export const annotationStorageKey = "annotations:v1";

const restore = (storage: AnnotationStorage) => {
  try {
    const serialized = storage.getItem(annotationStorageKey);
    if (serialized !== null) {
      return {
        ...savedAnnotationsSchema.parse(JSON.parse(serialized)),
        storageError: null,
      };
    }
  } catch {
    return {
      annotations: [],
      personaId: personas[0].id,
      storageError: "Saved annotations could not be restored on this device.",
    };
  }
  return { annotations: [], personaId: personas[0].id, storageError: null };
};

export const createAnnotationStore = (storage: AnnotationStorage) =>
  createStore<AnnotationState>()((set, get) => {
    const save = (personaId: string, annotations: Annotation[]): boolean => {
      try {
        storage.setItem(
          annotationStorageKey,
          JSON.stringify({ annotations, personaId, version: 1 })
        );
        set({ annotations, personaId, storageError: null });
        return true;
      } catch {
        set({
          storageError:
            "Could not save on this device. Your annotation has not been saved. Try again.",
        });
        return false;
      }
    };
    return {
      ...restore(storage),
      addAnnotation: (input) => {
        const { personaId, annotations } = get();
        if (
          !personas.some(
            (persona) =>
              persona.id === personaId && persona.role === "associate"
          )
        ) {
          return false;
        }
        const parsed = annotationInputSchema.safeParse(input);
        if (!parsed.success) {
          return false;
        }
        const { target, start, end, comment } = parsed.data;
        const createdAt = new Date().toISOString();
        return save(personaId, [
          ...annotations,
          {
            authorId: personaId,
            comment,
            createdAt,
            end,
            id: `annotation:${createdAt}:${annotations.length}`,
            quote: target.text.slice(start, end),
            start,
            target,
          },
        ]);
      },
      selectingText: false,
      setPersona: (id) => {
        if (
          personas.some((persona) => persona.id === id) &&
          save(id, get().annotations)
        ) {
          set({ selectingText: false });
        }
      },
      setSelectingText: (selecting) => {
        const associate = personas.some(
          (persona) =>
            persona.id === get().personaId && persona.role === "associate"
        );
        set({ selectingText: selecting && associate });
      },
    };
  });
