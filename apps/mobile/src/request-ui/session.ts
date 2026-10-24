import { createStateStore } from "@json-render/core";
import { requestFormSchema } from "@tricorder/request-ui/catalog";
import { draftRequest } from "@tricorder/request-ui/model";
import type { RequestItem, Stage } from "@tricorder/request-ui/model";
import * as Clipboard from "expo-clipboard";
import { useMemo, useState, useSyncExternalStore } from "react";
import { createMMKV } from "react-native-mmkv";

import { savedDraftSchema, snapshotDraft } from "./draft";

// Saved public-demo requests only; separate from application preferences.
const drafts = createMMKV({ id: "tricorder.demo-requests" });
const emptyForm = () => ({
  custom: "",
  customItems: [],
  editedDraft: null,
  selected: {},
});

const loadDraft = (company: string) => {
  try {
    const saved = drafts.getString(`v1:${company}`);
    return {
      form: saved
        ? savedDraftSchema.parse(JSON.parse(saved)).form
        : emptyForm(),
      stage: saved
        ? savedDraftSchema.parse(JSON.parse(saved)).stage
        : undefined,
      status: saved ? "Saved draft restored from this device." : "",
    };
  } catch {
    return {
      form: emptyForm(),
      status: "The saved draft could not be restored. Starting a new draft.",
    };
  }
};

export const useRequestSession = (
  company: string,
  name: string,
  founder: string,
  stage: Stage,
  baseItems: RequestItem[]
) => {
  const initial = useMemo(() => loadDraft(company), [company]);
  const store = useMemo(() => createStateStore(initial.form), [initial]);
  const snapshot = useSyncExternalStore(
    store.subscribe,
    store.getSnapshot,
    store.getSnapshot
  );
  const form = requestFormSchema.parse(snapshot);
  const items = [...baseItems, ...form.customItems].map((item) => ({
    ...item,
    checked: form.selected[item.id] ?? item.checked,
  }));
  const generated = draftRequest(name, founder, items);
  const draft = form.editedDraft ?? generated;
  const [notice, setNotice] = useState({
    draft,
    snapshot,
    stage,
    text: initial.status,
  });
  const status =
    notice.snapshot === snapshot &&
    notice.draft === draft &&
    notice.stage === stage
      ? notice.text
      : "";
  const setStatus = (text: string) =>
    setNotice({ draft, snapshot, stage, text });

  const act = async (kind: "add" | "regenerate" | "copy" | "save") => {
    setStatus("");
    if (kind === "add") {
      const text = form.custom.trim();
      if (!text || form.customItems.length >= 50) {
        return;
      }
      store.update({
        "/custom": "",
        "/customItems": [
          ...form.customItems,
          {
            ask: text,
            checked: true,
            guidance: "",
            id: `custom-${Date.now()}-${form.customItems.length}`,
            reason: "Added by you",
            title: text,
          },
        ],
      });
    } else if (kind === "regenerate") {
      store.set("/editedDraft", null);
    } else if (kind === "save") {
      try {
        drafts.set(
          `v1:${company}`,
          JSON.stringify(snapshotDraft(store.getSnapshot(), stage, draft))
        );
        setStatus("Saved on this device. Nothing has been sent.");
      } catch {
        setStatus(
          "Could not save this draft. Copy it to keep a separate copy."
        );
      }
    } else {
      try {
        setStatus(
          (await Clipboard.setStringAsync(draft))
            ? "Copied. Nothing has been sent."
            : "Could not copy. Select the draft to copy it manually."
        );
      } catch {
        setStatus("Could not copy. Select the draft to copy it manually.");
      }
    }
  };
  return { act, draft, form, generated, items, status, store };
};

export const savedRequestStage = (company: string) => loadDraft(company).stage;

export type RequestSession = ReturnType<typeof useRequestSession>;
