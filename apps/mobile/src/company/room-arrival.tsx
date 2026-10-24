import type { Claim } from "@tricorder/schema";
import type { CompanyIdentity } from "@tricorder/schema/company";
import type { CompanyRoomArrival } from "@tricorder/schema/company-room";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ScrollView, StyleSheet, View } from "react-native";
import { createMMKV } from "react-native-mmkv";

import { NativeSheet } from "../readout/native-sheet";
import {
  Action,
  Body,
  Card,
  Heading,
  Note,
  useReadoutColors,
} from "../readout/ui";
import { getCompanyRoom } from "./api";
import {
  emptyRoomState,
  openRoomArrival,
  receiveRoomArrival,
  restoreRoomState,
  roomStorageKey,
  stageForSequence,
  validateRoomArrival,
} from "./room-arrival-state";
import type { RoomArrivalState, RoomStage } from "./room-arrival-state";

const storage = createMMKV({ id: "tricorder.demo-room-arrivals" });
const readSaved = (company: string, snapshotAt: string) => {
  try {
    return {
      state: restoreRoomState(
        company,
        snapshotAt,
        storage.getString(roomStorageKey(company, snapshotAt))
      ),
      warning: "",
    };
  } catch {
    return {
      state: emptyRoomState(company, snapshotAt),
      warning: "Saved room progress could not be restored on this device.",
    };
  }
};
const styles = StyleSheet.create({
  group: { gap: 12 },
  sheet: { gap: 20, padding: 20, paddingBottom: 48 },
  source: { borderTopWidth: 1, gap: 8, paddingTop: 16 },
});
const categories = [
  { key: "strength", label: "Real strengths in the synthetic room" },
  { key: "red_flag", label: "Major red flags" },
  { key: "corroboration", label: "Small corroborations" },
] as const;

const RoomEvidence = ({
  claim,
  arrival,
  onClose,
}: {
  claim: Claim;
  arrival: CompanyRoomArrival;
  onClose: () => void;
}) => {
  const colors = useReadoutColors();
  return (
    <NativeSheet visible onClose={onClose}>
      <View style={{ gap: 12, padding: 16 }}>
        <Heading>Synthetic room evidence</Heading>
        <Action compact title="Done" onPress={onClose} />
      </View>
      <ScrollView contentContainerStyle={styles.sheet}>
        <Note>{arrival.syntheticNotice}</Note>
        <Note>Saved replay · {arrival.snapshotAt.replace("T", " ")}</Note>
        <Body>{claim.text}</Body>
        <Note>
          Authored demo finding. Replaying it does not run an analysis.
        </Note>
        {claim.sources.map((source) => (
          <View
            key={`${source.kind}:${source.uri}:${source.locator}:${source.quote}`}
            style={[styles.source, { borderColor: colors.line }]}
          >
            <Heading>
              {source.kind === "file"
                ? "Synthetic file excerpt"
                : "Saved public source"}
            </Heading>
            <Body>{source.uri}</Body>
            <Note>{source.locator}</Note>
            <Body>{source.quote}</Body>
          </View>
        ))}
      </ScrollView>
    </NativeSheet>
  );
};

const RoomFindings = ({ arrival }: { arrival: CompanyRoomArrival }) => {
  const [evidence, setEvidence] = useState<Claim | null>(null);
  const colors = useReadoutColors();
  const files = new Map(
    [...arrival.files, ...arrival.missingFiles].map((file) => [
      file.id,
      file.path,
    ])
  );
  return (
    <View style={styles.group}>
      <Heading>
        {arrival.stage === "partial" ? "Room partly in" : "Full saved room"}
      </Heading>
      <Note>{arrival.syntheticNotice}</Note>
      <Note>Saved replay · {arrival.snapshotAt.replace("T", " ")}</Note>
      {categories.map((category) => {
        const flags = arrival.flags.filter(
          (flag) => flag.category === category.key
        );
        return flags.length > 0 ? (
          <View key={category.key} style={styles.group}>
            <Heading>{category.label}</Heading>
            {flags.map((flag) => (
              <Card key={flag.id}>
                <Heading>{flag.piece}</Heading>
                <Body
                  style={{
                    color: category.key === "red_flag" ? colors.red : colors.fg,
                  }}
                >
                  {flag.title}
                </Body>
                {flag.why ? <Body>{flag.why}</Body> : null}
                {flag.claimIds.map((id) => {
                  const claim = arrival.claims[id];
                  return claim ? (
                    <View key={id} style={styles.group}>
                      <Body>{claim.text}</Body>
                      <Action
                        title={`Inspect ${flag.piece.toLowerCase()} evidence`}
                        onPress={() => setEvidence(claim)}
                      />
                    </View>
                  ) : null;
                })}
              </Card>
            ))}
          </View>
        ) : null;
      })}
      {arrival.waiting.length > 0 ? (
        <Card>
          <Heading>Waiting on files</Heading>
          {arrival.waiting.map((waiting) => (
            <View
              key={`${waiting.piece}:${waiting.fileIds.join(",")}`}
              style={styles.group}
            >
              <Body>{waiting.piece}</Body>
              {waiting.fileIds.map((id) => (
                <Note key={id}>{files.get(id) ?? id}</Note>
              ))}
            </View>
          ))}
        </Card>
      ) : null}
      {arrival.gaps.length > 0 ? (
        <Card>
          <Heading>Remaining evidence gaps</Heading>
          {arrival.gaps.map((gap) => (
            <Body key={gap}>{gap}</Body>
          ))}
        </Card>
      ) : null}
      <Card>
        <Heading>Files in this saved arrival ({arrival.files.length})</Heading>
        <Note>
          These are saved synthetic file references and excerpts, not uploaded
          documents.
        </Note>
        {arrival.files.map((file) => (
          <Note key={file.id}>{file.path}</Note>
        ))}
      </Card>
      {evidence ? (
        <RoomEvidence
          claim={evidence}
          arrival={arrival}
          onClose={() => setEvidence(null)}
        />
      ) : null}
    </View>
  );
};

type ArrivalCache = Partial<Record<1 | 2, CompanyRoomArrival>>;
interface RoomSessionProps {
  company: CompanyIdentity;
  snapshotAt: string;
}

const RoomSession = ({ company, snapshotAt }: RoomSessionProps) => {
  const initial = useMemo(
    () => readSaved(company.slug, snapshotAt),
    [company.slug, snapshotAt]
  );
  const [progress, setProgress] = useState(initial.state);
  const progressRef = useRef(progress);
  const [cache, setCache] = useState<ArrivalCache>({});
  const [warning, setWarning] = useState(initial.warning);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(initial.state.received > 0);
  const [retryStage, setRetryStage] = useState<RoomStage | null>(null);
  const active = useRef<AbortController | null>(null);

  const restore = useCallback(async () => {
    active.current?.abort();
    const controller = new AbortController();
    active.current = controller;
    const saved = progressRef.current;
    if (saved.received === 0) {
      return;
    }
    setBusy(true);
    setError("");
    setRetryStage(null);
    const sequences = new Set([saved.opened, saved.received]);
    const results = await Promise.allSettled(
      [...sequences]
        .filter((sequence) => sequence !== 0)
        .map(async (sequence) => {
          const stage = stageForSequence(sequence as 1 | 2);
          const result = await getCompanyRoom(
            company.slug,
            stage,
            controller.signal
          );
          validateRoomArrival(saved, result, stage);
          if (!controller.signal.aborted) {
            setCache((previous) => ({
              ...previous,
              [result.sequence]: result,
            }));
          }
        })
    );
    if (!controller.signal.aborted) {
      const failed = results.find((result) => result.status === "rejected");
      if (failed?.status === "rejected") {
        setError(
          failed.reason instanceof Error
            ? failed.reason.message
            : "The saved room could not be restored."
        );
      }
      setBusy(false);
    }
  }, [company.slug]);
  useEffect(() => {
    void restore();
    return () => active.current?.abort();
  }, [restore]);

  const retain = (next: RoomArrivalState) => {
    try {
      storage.set(
        roomStorageKey(company.slug, snapshotAt),
        JSON.stringify(next)
      );
      setWarning("");
    } catch {
      setWarning(
        "Room progress is visible now but could not be saved on this device."
      );
    }
    progressRef.current = next;
    setProgress(next);
  };
  const replay = async (stage: RoomStage) => {
    active.current?.abort();
    const controller = new AbortController();
    active.current = controller;
    setBusy(true);
    setError("");
    setRetryStage(stage);
    try {
      const result = await getCompanyRoom(
        company.slug,
        stage,
        controller.signal
      );
      if (controller.signal.aborted) {
        return;
      }
      validateRoomArrival(progressRef.current, result, stage);
      const next = receiveRoomArrival(progressRef.current, result);
      setCache((previous) => ({ ...previous, [result.sequence]: result }));
      retain(next);
    } catch (error_) {
      if (!controller.signal.aborted) {
        setError(
          error_ instanceof Error
            ? error_.message
            : "The arrival could not be loaded. Please retry."
        );
      }
    }
    if (!controller.signal.aborted) {
      setBusy(false);
    }
  };
  const pending =
    progress.received > progress.opened && progress.received !== 0
      ? cache[progress.received]
      : undefined;
  const opened = progress.opened === 0 ? undefined : cache[progress.opened];
  return (
    <View style={styles.group}>
      <Card>
        <Heading>Synthetic room arrivals</Heading>
        <Note>
          Replay the saved demo results. No founder is sending files and no
          analysis runs.
        </Note>
        <Action
          title="Replay partial arrival"
          disabled={busy}
          onPress={() => {
            void replay("partial");
          }}
        />
        <Action
          title="Replay full arrival"
          disabled={busy}
          onPress={() => {
            void replay("full");
          }}
        />
        {busy ? (
          <Note accessibilityRole="status">Loading saved arrival…</Note>
        ) : null}
        {warning ? <Body accessibilityRole="alert">{warning}</Body> : null}
        {error ? (
          <>
            <Body accessibilityRole="alert">{error}</Body>
            <Action
              title="Retry room arrival"
              disabled={busy}
              onPress={() => {
                if (retryStage) {
                  void replay(retryStage);
                } else {
                  void restore();
                }
              }}
            />
          </>
        ) : null}
        {pending ? (
          <View style={styles.group}>
            <Body accessibilityRole="status">
              {company.name}: {pending.stage} synthetic arrival ready ·{" "}
              {pending.files.length} file references
            </Body>
            <Action
              title={`Open ${pending.stage} arrival`}
              primary
              onPress={() =>
                retain(openRoomArrival(progressRef.current, pending))
              }
            />
          </View>
        ) : null}
        {!busy && progress.received === 0 ? (
          <Note>No synthetic arrivals replayed yet.</Note>
        ) : null}
        {progress.received > 0 && progress.received === progress.opened ? (
          <Note>
            Latest received arrival is open. Replaying an earlier arrival will
            not replace it.
          </Note>
        ) : null}
      </Card>
      {opened ? <RoomFindings key={opened.arrivalId} arrival={opened} /> : null}
    </View>
  );
};

export const CompanyRoomArrivals = ({
  company,
  snapshotAt,
}: RoomSessionProps) => (
  <RoomSession
    key={roomStorageKey(company.slug, snapshotAt)}
    company={company}
    snapshotAt={snapshotAt}
  />
);
