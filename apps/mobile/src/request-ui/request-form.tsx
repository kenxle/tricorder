import { Checkbox, Host } from "@expo/ui";
import type { Spec } from "@json-render/core";
import {
  JSONUIProvider,
  Renderer,
  defineRegistry,
  useBoundProp,
} from "@json-render/react-native";
import {
  createRequestSpec,
  requestCatalog,
  requestItemSchema,
} from "@tricorder/request-ui/catalog";
import type { RequestItem, Stage } from "@tricorder/request-ui/model";
import { readRequestStream } from "@tricorder/request-ui/stream";
import { fetch } from "expo/fetch";
import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { StyleSheet, View } from "react-native";

import { serverOrigin } from "../readout/api";
import { Action, Field, Note, useReadoutColors } from "../readout/ui";
import type { RequestSession } from "./session";

const styles = StyleSheet.create({
  column: { gap: 16 },
  draft: {
    fontFamily: "PlexMono",
    fontSize: 14,
    lineHeight: 22,
    minHeight: 360,
  },
  toggle: {
    borderBottomWidth: 1,
    gap: 6,
    paddingVertical: 16,
  },
});

const SessionContext = createContext<RequestSession | null>(null);
const useSession = () => {
  const session = useContext(SessionContext);
  if (!session) {
    throw new Error("Request controls require a request session.");
  }
  return session;
};

const Toggle = ({
  item,
  checked,
  onChange,
}: {
  item: RequestItem;
  checked: boolean;
  onChange: () => void;
}) => {
  const colors = useReadoutColors();
  return (
    <View style={[styles.toggle, { borderColor: colors.line }]}>
      <Host matchContents={{ vertical: true }} seedColor={colors.accent}>
        <Checkbox label={item.title} value={checked} onValueChange={onChange} />
      </Host>
      <Note>{item.reason}</Note>
      {item.guidance ? <Note>{item.guidance}</Note> : null}
    </View>
  );
};

const { registry } = defineRegistry(requestCatalog, {
  components: {
    RequestButton: function RequestButton({ props }) {
      const session = useSession();
      const disabled =
        (props.kind === "add" &&
          (!session.form.custom.trim() ||
            session.form.customItems.length >= 50)) ||
        (props.kind === "copy" &&
          (!session.items.some((item) => item.checked) ||
            !session.draft.trim()));
      return (
        <Action
          title={props.label}
          disabled={disabled}
          onPress={() => {
            void session.act(props.kind);
          }}
        />
      );
    },
    RequestColumn: ({ children }) => (
      <View style={styles.column}>{children}</View>
    ),
    RequestCustomItems: function RequestCustomItems() {
      const { form, store } = useSession();
      return (
        <View>
          {form.customItems.map((item) => {
            const checked = form.selected[item.id] ?? item.checked;
            return (
              <Toggle
                key={item.id}
                item={item}
                checked={checked}
                onChange={() => store.set(`/selected/${item.id}`, !checked)}
              />
            );
          })}
        </View>
      );
    },
    RequestInput: function RequestInput({ props, bindings }) {
      const session = useSession();
      const [value, setValue] = useBoundProp(props.value, bindings?.value);
      const isDraft = props.field === "draft";
      return (
        <Field
          label={props.label}
          value={value ?? (isDraft ? session.generated : "")}
          onChangeText={setValue}
          multiline={isDraft}
          maxLength={isDraft ? 20_000 : 2000}
          style={isDraft ? styles.draft : undefined}
        />
      );
    },
    RequestNote: ({ props }) => <Note>{props.text}</Note>,
    RequestStatus: function RequestStatus() {
      const { status, form } = useSession();
      return (
        <View>
          {typeof form.editedDraft === "string" && (
            <Note>
              Your edited message is kept until you regenerate it from the
              selected items.
            </Note>
          )}
          <Note accessibilityLiveRegion="polite">{status}</Note>
        </View>
      );
    },
    RequestToggle: function RequestToggle({ props, bindings }) {
      const [value, setValue] = useBoundProp(props.checked, bindings?.checked);
      const checked = value ?? props.item.checked;
      return (
        <Toggle
          item={props.item}
          checked={checked}
          onChange={() => setValue(!checked)}
        />
      );
    },
  },
});

interface RequestFormProps {
  company: string;
  stage: Stage;
  items: RequestItem[];
  session: RequestSession;
  onItems: (items: RequestItem[]) => void;
}

const fetchLayout = async (
  company: string,
  stage: Stage,
  signal: AbortSignal,
  onSpec: (spec: Spec) => void
) => {
  const response = await fetch(
    `${serverOrigin()}/api/ui/request?${new URLSearchParams({ company, stage })}`,
    { signal }
  );
  if (
    !response.ok ||
    !response.body ||
    response.headers.get("X-Tricorder-UI-Version") !== "1" ||
    !response.headers.get("Content-Type")?.includes("application/x-ndjson")
  ) {
    throw new Error("Request layout unavailable.");
  }
  return readRequestStream(response.body, onSpec, signal);
};

const layoutItems = (spec: Spec) =>
  (spec.elements.request.children ?? []).flatMap((id) => {
    const element = spec.elements[id];
    return element.type === "RequestToggle"
      ? [requestItemSchema.parse(element.props.item)]
      : [];
  });

const RequestLayout = ({
  company,
  stage,
  items,
  session,
  onItems,
  onRefresh,
}: RequestFormProps & { onRefresh: () => void }) => {
  const [spec, setSpec] = useState<Spec | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const fallback = useMemo(() => createRequestSpec(items), [items]);
  useEffect(() => {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15_000);
    let mounted = true;
    void fetchLayout(company, stage, controller.signal, (next) => {
      if (mounted) {
        setSpec(next);
      }
    })
      .then((complete) => {
        if (mounted) {
          onItems(layoutItems(complete));
        }
        return complete;
      })
      .catch(() => {
        controller.abort();
        if (mounted) {
          setSpec(fallback);
          onItems(layoutItems(fallback));
          setError(
            "Using the saved checklist. Live layout is unavailable; your edits are kept."
          );
        }
      })
      .finally(() => {
        clearTimeout(timeout);
        if (mounted) {
          setLoading(false);
        }
      });
    return () => {
      mounted = false;
      clearTimeout(timeout);
      controller.abort();
    };
  }, [company, stage, fallback, onItems]);
  return (
    <SessionContext.Provider value={session}>
      <Note accessibilityLiveRegion="polite">
        {loading ? "Loading request…" : error}
      </Note>
      <Action
        title={error ? "Retry live layout" : "Refresh request layout"}
        disabled={loading}
        onPress={onRefresh}
      />
      <JSONUIProvider registry={registry} store={session.store}>
        <Renderer spec={spec} registry={registry} includeStandard={false} />
      </JSONUIProvider>
    </SessionContext.Provider>
  );
};

export const RequestForm = (props: RequestFormProps) => {
  const [attempt, setAttempt] = useState(0);
  return (
    <RequestLayout
      key={`${props.company}:${props.stage}:${attempt}`}
      {...props}
      onRefresh={() => setAttempt((value) => value + 1)}
    />
  );
};
