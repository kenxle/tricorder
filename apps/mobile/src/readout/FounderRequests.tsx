import { Host, Switch } from "@expo/ui";
import type { PythonModels } from "@tricorder/schema/api";
import * as Clipboard from "expo-clipboard";
import * as DocumentPicker from "expo-document-picker";
import { File } from "expo-file-system";
import * as MailComposer from "expo-mail-composer";
import { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  KeyboardAvoidingView,
  Linking,
  Platform,
  ScrollView,
  StyleSheet,
  View,
} from "react-native";

import { AnnotationScope } from "../annotations/context";
import { apiRequest, roomPath } from "./api";
import { NativeSheet } from "./native-sheet";
import {
  Action,
  Body,
  Card,
  Field,
  Heading,
  Note,
  Row,
  renderReadoutScroll,
  useReadoutColors,
} from "./ui";

type Lines = PythonModels["FounderRequestList"];
type Item = PythonModels["Item"];
type Draft = PythonModels["Draft"];
interface Pending {
  asset: DocumentPicker.DocumentPickerAsset;
  answers: string[];
}
// This POST still has an opaque dictionary contract. Narrow its displayed fields here.
interface Receipt {
  room: string;
  files: { original_name: string; saved: string; note?: string }[];
  summary: string[];
}
let lastReceipt: Receipt | null = null;
let signoff = { fund: "", sender: "" };

const base = (room: string) => roomPath(room, "founder-requests");
const post = (body: unknown): RequestInit => ({
  body: JSON.stringify(body),
  headers: { "Content-Type": "application/json" },
  method: "POST",
});
const message = (error: unknown) =>
  error instanceof Error ? error.message : String(error);

function receiptOf(value: Record<string, unknown>): Receipt {
  if (
    typeof value.room !== "string" ||
    !Array.isArray(value.files) ||
    !Array.isArray(value.summary)
  ) {
    throw new TypeError(
      "The files were submitted, but the receipt could not be read. Refresh the readout before trying again."
    );
  }
  return {
    files: value.files.flatMap((file: unknown) => {
      if (
        !file ||
        typeof file !== "object" ||
        !("original_name" in file) ||
        !("saved" in file) ||
        typeof file.original_name !== "string" ||
        typeof file.saved !== "string"
      ) {
        return [];
      }
      return [
        {
          note:
            "note" in file && typeof file.note === "string"
              ? file.note
              : undefined,
          original_name: file.original_name,
          saved: file.saved,
        },
      ];
    }),
    room: value.room,
    summary: value.summary.filter(
      (line): line is string => typeof line === "string"
    ),
  };
}

function requestsOf(lines: Lines) {
  return lines.items.flatMap((item) =>
    (item.requests ?? []).flatMap((request) =>
      typeof request.checklist_id === "string" &&
      typeof request.name === "string"
        ? [
            {
              id: request.checklist_id,
              label:
                (item.requests?.length ?? 0) > 1
                  ? `${item.title}: ${request.name}`
                  : item.title,
            },
          ]
        : []
    )
  );
}

export function FounderRequests({
  room,
  onRebuilt,
}: {
  room: string;
  onRebuilt?: (room: string) => void;
}) {
  const [visible, setVisible] = useState(false);
  const [busy, setBusy] = useState(false);
  const [receipt, setReceipt] = useState<Receipt | null>(
    lastReceipt?.room === room ? lastReceipt : null
  );
  const colors = useReadoutColors();
  return (
    <Card>
      <Heading>Requests to the founder</Heading>
      <Note>
        Tick lines and draft one message, or draft one line on its own.
        Tricorder never sends it: copy it, or open it in your own mail app.
      </Note>
      <Action
        primary
        title="Manage requests and founder replies"
        onPress={() => setVisible(true)}
      />
      {receipt?.room === room && <ReceiptView receipt={receipt} />}
      <NativeSheet
        visible={visible}
        dismissalDisabled={busy}
        onClose={() => {
          if (!busy) {
            setVisible(false);
          }
        }}
      >
        <View style={[styles.fill, { backgroundColor: colors.bg }]}>
          {visible && (
            <RequestManager
              key={room}
              room={room}
              onBusy={setBusy}
              onClose={() => setVisible(false)}
              onDone={(next) => {
                lastReceipt = next;
                setReceipt(next);
                setVisible(false);
                onRebuilt?.(next.room);
              }}
            />
          )}
        </View>
      </NativeSheet>
    </Card>
  );
}

function RequestManager({
  room,
  onClose,
  onDone,
  onBusy,
}: {
  room: string;
  onClose: () => void;
  onDone: (receipt: Receipt) => void;
  onBusy: (busy: boolean) => void;
}) {
  const [lines, setLines] = useState<Lines | null>(null);
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [pending, setPending] = useState<Pending[]>([]);
  const [tab, setTab] = useState<"requests" | "draft" | "reply">("requests");
  const [draft, setDraft] = useState<Draft | null>(null);
  const [numbers, setNumbers] = useState<number[]>([]);
  const [to, setTo] = useState("");
  const [sender, setSender] = useState(signoff.sender);
  const [fund, setFund] = useState(signoff.fund);
  const [by, setBy] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [retry, setRetry] = useState(0);
  const active = useRef(false);
  const working = useRef(false);

  useEffect(() => {
    active.current = true;
    const controller = new AbortController();
    apiRequest<Lines>(base(room), { signal: controller.signal })
      .then((next) => {
        if (!active.current || controller.signal.aborted) {
          return;
        }
        setLines(next);
        setSelected(new Set(next.default));
        setBy(next.by);
        setError("");
        setSender((value) => value || next.sender);
        setFund((value) => value || next.fund);
      })
      .catch((error_: unknown) => {
        if (!controller.signal.aborted) {
          setError(message(error_));
        }
      });
    return () => {
      active.current = false;
      controller.abort();
    };
  }, [room, retry]);

  const run = async (job: () => Promise<void>) => {
    if (working.current) {
      return;
    }
    working.current = true;
    onBusy(true);
    setBusy(true);
    setError("");
    setStatus("");
    try {
      await job();
    } catch (error_) {
      if (active.current) {
        setError(message(error_));
      }
    } finally {
      working.current = false;
      onBusy(false);
      if (active.current) {
        setBusy(false);
      }
    }
  };
  const makeDraft = (wanted: number[]) =>
    run(async () => {
      const next = await apiRequest<Draft>(
        `${base(room)}/draft`,
        post({
          by: by || null,
          fund,
          numbers: wanted,
          sender,
          to,
        } satisfies PythonModels["DraftAsk"])
      );
      if (!active.current) {
        return;
      }
      signoff = { fund, sender };
      setDraft(next);
      setNumbers(wanted);
      setSubject(next.subject);
      setBody(next.body);
      setTab("draft");
    });
  const pick = (kind: "top" | "need" | "all" | "none") => {
    setSelected(
      new Set(
        (lines?.items ?? [])
          .filter(
            (item) =>
              kind === "all" ||
              (kind === "top" && item.top) ||
              (kind === "need" &&
                !item.if_you_have_it &&
                item.ask_stage === "before_second_meeting")
          )
          .map((item) => item.number)
      )
    );
  };
  const toggle = (number: number) =>
    setSelected((current) => {
      const next = new Set(current);
      if (next.has(number)) {
        next.delete(number);
      } else {
        next.add(number);
      }
      return next;
    });
  const mailto = `mailto:${encodeURIComponent(to).replace("%40", "@")}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body.replaceAll(/\r?\n/g, "\r\n"))}`;
  const openMail = () =>
    run(async () => {
      if (Platform.OS !== "web" && (await MailComposer.isAvailableAsync())) {
        await MailComposer.composeAsync({
          body,
          isHtml: false,
          recipients: to.trim() ? [to.trim()] : [],
          subject,
        });
      } else {
        if (mailto.length > (lines?.mailto_max ?? 1800)) {
          throw new Error(
            "This message is too long for a mail link. Copy the text instead."
          );
        }
        await Linking.openURL(mailto);
      }
    });

  return (
    <KeyboardAvoidingView
      style={styles.fill}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      <View style={styles.header}>
        <Heading>Requests to the founder</Heading>
        <Row>
          <Action
            compact
            title="Requests"
            disabled={busy}
            onPress={() => setTab("requests")}
          />
          <Action
            compact
            title="Draft"
            disabled={busy || !draft}
            onPress={() => setTab("draft")}
          />
          <Action
            compact
            title="Add reply"
            disabled={busy || !lines}
            onPress={() => setTab("reply")}
          />
          <Action compact title="Close" disabled={busy} onPress={onClose} />
        </Row>
        {busy && <ActivityIndicator accessibilityLabel="Working" />}
        {!!error && <Body accessibilityRole="alert">{error}</Body>}
        {!!status && <Note accessibilityLiveRegion="polite">{status}</Note>}
        {!lines && !error && <Note>Loading requests.</Note>}
        {!lines && !!error && (
          <Action
            title="Retry"
            onPress={() => setRetry((value) => value + 1)}
          />
        )}
      </View>
      {tab === "requests" && lines && (
        <FlatList
          renderScrollComponent={renderReadoutScroll}
          contentContainerStyle={styles.content}
          data={lines.items}
          extraData={selected}
          keyExtractor={(item) => String(item.number)}
          ListHeaderComponent={
            <View style={styles.gap}>
              <Note>
                Tricorder never sends this. Choose the lines you want to ask
                for.
              </Note>
              <Row>
                {(["top", "need", "all", "none"] as const).map(
                  (kind, index) => (
                    <Action
                      key={kind}
                      compact
                      title={["Top five", "All required", "All", "None"][index]}
                      disabled={busy}
                      onPress={() => pick(kind)}
                    />
                  )
                )}
              </Row>
              <Action
                title={`Draft request for ${selected.size} selected`}
                disabled={busy || !selected.size}
                onPress={() =>
                  makeDraft(
                    lines.items
                      .filter((item) => selected.has(item.number))
                      .map((item) => item.number)
                  )
                }
              />
            </View>
          }
          renderItem={({ item }) => (
            <AnnotationScope
              id={`room:${room}/request:${item.number}`}
              label={`${room} · Founder request · ${item.title}`}
            >
              <RequestItem
                item={item}
                selected={selected.has(item.number)}
                disabled={busy}
                onToggle={() => toggle(item.number)}
                onDraft={() => makeDraft([item.number])}
              />
            </AnnotationScope>
          )}
          ListFooterComponent={
            lines.held.length ? (
              <Card>
                <Heading>Not asked for: the room already holds these</Heading>
                {lines.held.map((item) => (
                  <AnnotationScope
                    key={item.number}
                    id={`room:${room}/held:${item.number}`}
                    label={`${room} · Evidence already held · ${item.title}`}
                  >
                    <Note>
                      {item.title}: {item.files.join(", ")}
                    </Note>
                  </AnnotationScope>
                ))}
              </Card>
            ) : undefined
          }
        />
      )}
      {tab === "draft" && draft && lines && (
        <ScrollView
          keyboardShouldPersistTaps="handled"
          contentContainerStyle={styles.content}
        >
          <Heading>Draft to the founder</Heading>
          <Note>
            Tricorder never sends this. Copy it, or open it in your own mail app
            and send it from there.
          </Note>
          <Field
            label="To"
            value={to}
            onChangeText={setTo}
            autoCapitalize="none"
            keyboardType="email-address"
            editable={!busy}
          />
          <Field
            label="Ask for it by (YYYY-MM-DD)"
            value={by}
            onChangeText={setBy}
            editable={!busy}
          />
          <Field
            label="Your name"
            value={sender}
            onChangeText={setSender}
            editable={!busy}
          />
          <Field
            label="Fund"
            value={fund}
            onChangeText={setFund}
            editable={!busy}
          />
          <Note>
            Redo the draft to apply a new date or sign-off. This replaces your
            edits to the subject and message.
          </Note>
          <Action
            title="Redo the draft with these"
            disabled={busy}
            onPress={() => makeDraft(numbers)}
          />
          <Field
            label="Subject"
            value={subject}
            onChangeText={setSubject}
            editable={!busy}
          />
          <Field
            label="Message (edit freely)"
            value={body}
            onChangeText={setBody}
            multiline
            editable={!busy}
            style={styles.message}
          />
          <Row>
            <Action
              compact
              title="Copy text"
              disabled={busy}
              onPress={() =>
                run(async () => {
                  const copied = await Clipboard.setStringAsync(
                    `Subject: ${subject}\n\n${body}`
                  );
                  if (!copied) {
                    throw new Error("Could not copy the draft.");
                  }
                  if (active.current) {
                    setStatus("Copied.");
                  }
                })
              }
            />
            <Action
              compact
              title="Open in mail app"
              disabled={busy}
              onPress={openMail}
            />
          </Row>
          {mailto.length > lines.mailto_max && (
            <Note>
              This message is long for a mail link. If your mail app cuts it
              short, copy the text instead.
            </Note>
          )}
          <Heading>Where the guidance comes from</Heading>
          {[
            ...new Set(
              (draft.items ?? []).flatMap((item) =>
                typeof item.guidance?.path === "string"
                  ? [item.guidance.path]
                  : []
              )
            ),
          ].map((path) => (
            <Note key={path}>{path}</Note>
          ))}
          {draft.read_from && (
            <Note>Greeting and company read from {draft.read_from}</Note>
          )}
        </ScrollView>
      )}
      {tab === "reply" && lines && (
        <AddReply
          room={room}
          lines={lines}
          busy={busy}
          run={run}
          isActive={() => active.current}
          onDone={onDone}
          pending={pending}
          setPending={setPending}
        />
      )}
    </KeyboardAvoidingView>
  );
}

function RequestItem({
  item,
  selected,
  disabled,
  onToggle,
  onDraft,
}: {
  item: Item;
  selected: boolean;
  disabled: boolean;
  onToggle: () => void;
  onDraft: () => void;
}) {
  return (
    <Card>
      <Host matchContents={{ vertical: true }}>
        <Switch
          value={selected}
          onValueChange={onToggle}
          disabled={disabled}
          label={item.title}
        />
      </Host>
      <Body>{item.text}</Body>
      <Note>{item.piece.replaceAll("_", " ")}</Note>
      {!!item.top && <Note>Top {item.top}</Note>}
      {item.rests_on_flag && <Note>A red flag rests on it</Note>}
      {item.if_you_have_it && <Note>If you have it</Note>}
      {item.ask_stage === "after_term_sheet" && (
        <Note>After the term sheet</Note>
      )}
      {item.in_room.length > 0 && (
        <Note>
          Already in the room: {item.in_room.join(", ")}. The line asks only for
          the rest.
        </Note>
      )}
      <Note>For you, not sent: {item.operator_why}</Note>
      <Action
        title={`Draft request for ${item.title}`}
        disabled={disabled}
        onPress={onDraft}
      />
    </Card>
  );
}

async function assetBase64(
  asset: DocumentPicker.DocumentPickerAsset
): Promise<string> {
  if (Platform.OS !== "web") {
    return new File(asset.uri).base64();
  }
  // DocumentPicker supplies a data URL on web; native reads its cached file asynchronously.
  const encoded = asset.base64 ?? asset.uri;
  const match = /^data:[^,]*;base64,(.*)$/s.exec(encoded);
  if (match) {
    return match[1];
  }
  if (asset.base64 && !asset.base64.startsWith("data:")) {
    return asset.base64;
  }
  throw new Error(`Could not read ${asset.name}. Choose the file again.`);
}

function AddReply({
  lines,
  room,
  busy,
  run,
  isActive,
  onDone,
  pending,
  setPending,
}: {
  lines: Lines;
  room: string;
  busy: boolean;
  run: (job: () => Promise<void>) => Promise<void>;
  isActive: () => boolean;
  onDone: (receipt: Receipt) => void;
  pending: Pending[];
  setPending: React.Dispatch<React.SetStateAction<Pending[]>>;
}) {
  const requests = requestsOf(lines);
  const update = (
    index: number,
    change: (current: Pending) => Pending | null
  ) =>
    setPending((current) =>
      current.flatMap((item, n) =>
        n === index
          ? [change(item)].filter((next): next is Pending => next !== null)
          : [item]
      )
    );
  const choose = () =>
    run(async () => {
      const result = await DocumentPicker.getDocumentAsync({
        base64: true,
        copyToCacheDirectory: true,
        multiple: true,
      });
      if (result.canceled || !isActive()) {
        return;
      }
      const { assets } = result;
      for (const asset of assets) {
        const extension = asset.name
          .slice(asset.name.lastIndexOf("."))
          .toLowerCase();
        if (!lines.accepted.includes(extension)) {
          throw new Error(
            `${asset.name}: choose one of ${lines.accepted.join(", ")}.`
          );
        }
        if (asset.size !== undefined && asset.size > lines.upload_max_bytes) {
          throw new Error(`${asset.name} is larger than the file size limit.`);
        }
      }
      setPending((current) => [
        ...current,
        ...assets.map((asset) => ({ answers: [], asset })),
      ]);
    });
  const ready =
    pending.length > 0 && pending.every((item) => item.answers.length > 0);
  const add = () =>
    run(async () => {
      if (!ready) {
        return;
      }
      let total = 0;
      const files = [];
      // Read sequentially so several large files do not allocate their base64 strings at once.
      for (const item of pending) {
        const data = await assetBase64(item.asset);
        const size =
          Math.floor((data.length * 3) / 4) -
          (data.endsWith("==") ? 2 : data.endsWith("=") ? 1 : 0);
        total += size;
        if (
          size > lines.upload_max_bytes ||
          total > lines.upload_max_bytes * 4
        ) {
          throw new Error(
            "The selected files exceed the upload size limit. Remove some files and try again."
          );
        }
        files.push({
          answers: item.answers.join(","),
          data,
          name: item.asset.name,
        });
      }
      if (!isActive()) {
        return;
      }
      let target = lines.synthetic ? lines.working_copy : room;
      if (!target) {
        const copied = await apiRequest<Record<string, unknown>>(
          `${base(room)}/copy`,
          post({})
        );
        if (typeof copied.room !== "string") {
          throw new TypeError(
            "Could not find the working copy. Refresh the room before adding files."
          );
        }
        target = copied.room;
      }
      const receipt = receiptOf(
        await apiRequest<Record<string, unknown>>(
          `${base(target)}/batch`,
          post({ files })
        )
      );
      lastReceipt = receipt;
      if (isActive()) {
        setPending([]);
        onDone(receipt);
      }
    });
  return (
    <FlatList
      renderScrollComponent={renderReadoutScroll}
      contentContainerStyle={styles.content}
      data={pending}
      keyExtractor={(item, index) => `${item.asset.uri}:${index}`}
      ListHeaderComponent={
        <View style={styles.gap}>
          <Heading>Add the founder&apos;s reply</Heading>
          {lines.synthetic && (
            <Note>
              This is a sample room, so the files go into a working copy of it.
            </Note>
          )}
          <Note>
            Up to {Math.round(lines.upload_max_bytes / 1_048_576)} MB a file.
            Accepted: {lines.accepted.join(", ")}.
          </Note>
          <Action
            title="Choose files from the reply"
            disabled={busy}
            onPress={choose}
          />
        </View>
      }
      renderItem={({ item, index }) => (
        <Card>
          <Heading>{item.asset.name}</Heading>
          <Action
            title={`Remove ${item.asset.name}`}
            disabled={busy}
            onPress={() => update(index, () => null)}
          />
          <Note>It answers:</Note>
          {requests.map((request) => (
            <Host key={request.id} matchContents={{ vertical: true }}>
              <Switch
                label={request.label}
                disabled={busy}
                value={item.answers.includes(request.id)}
                onValueChange={() =>
                  update(index, (current) => ({
                    ...current,
                    answers: current.answers.includes(request.id)
                      ? current.answers.filter((id) => id !== request.id)
                      : [...current.answers, request.id],
                  }))
                }
              />
            </Host>
          ))}
        </Card>
      )}
      ListFooterComponent={
        <Action
          title={
            busy
              ? "Adding and rerunning"
              : `Add ${pending.length || ""} ${pending.length === 1 ? "file" : "files"} to the room`
          }
          disabled={busy || !ready}
          onPress={add}
        />
      }
    />
  );
}

function ReceiptView({ receipt }: { receipt: Receipt }) {
  return (
    <AnnotationScope
      id={`room:${receipt.room}/receipt:${receipt.files.map((file) => file.saved).join(",")}`}
      label={`${receipt.room} · Founder reply receipt`}
    >
      <View style={styles.gap} accessibilityLiveRegion="polite">
        <Heading>What changed</Heading>
        {receipt.files.map((file) => (
          <Body key={file.saved}>
            {file.original_name} is saved as {file.saved}.
            {file.note ? ` ${file.note}` : ""}
          </Body>
        ))}
        {receipt.summary.map((line, index) => (
          <Body key={index}>{line}</Body>
        ))}
      </View>
    </AnnotationScope>
  );
}

const styles = StyleSheet.create({
  content: { gap: 16, padding: 16, paddingBottom: 32 },
  fill: { flex: 1 },
  gap: { gap: 10 },
  header: { gap: 10, padding: 16 },
  message: { minHeight: 260, textAlignVertical: "top" },
});
