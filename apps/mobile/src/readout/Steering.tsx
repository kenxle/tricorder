import type {
  Claim,
  Panel,
  Piece,
  PieceRevision,
  Readout,
} from "@tricorder/schema";
import type { PythonAPI } from "@tricorder/schema/api";
import { useEffect, useRef, useState } from "react";
import {
  FlatList,
  KeyboardAvoidingView,
  Modal,
  Platform,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";

import { apiRequest, roomPath } from "./api";
import { SourceChip } from "./SourceChip";
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

export const PIECE_LABEL: Record<Piece["name"], string> = {
  burn_and_runway: "Burn and runway",
  comps: "Comps",
  customers: "Customers",
  market: "Market",
  retention: "Retention",
  team: "Team",
  the_pitch_itself: "The pitch itself",
  traction_and_revenue: "Traction and revenue",
  unit_economics: "Unit economics",
};
export const VERDICT_LABEL: Record<Piece["verdict"], string> = {
  looking_strong: "Looking strong",
  looking_weak: "Looking weak",
  mixed: "Mixed",
  not_enough_in_the_room: "Not enough in the room",
};

interface Revision {
  rev: PieceRevision;
  n: number;
  panel?: Panel;
  typedOn: string;
}
type Line =
  | { kind: "claim"; claim: Claim }
  | { kind: "diff"; revision: Revision };
const cell = (panel: Panel | undefined, change: string, col: number) =>
  panel?.rows.find((row) => row[0] === change)?.[col] ?? null;

function who(rev: PieceRevision) {
  const date = new Date(rev.steer.at);
  const at = Number.isNaN(date.getTime())
    ? rev.steer.at
    : date.toLocaleString([], {
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        month: "short",
      });
  return `${rev.steer.author ? `${rev.steer.author}'s` : "The operator's"} steer, ${at}`;
}

function said(rev: PieceRevision, headline: string) {
  let rest = (rev.note ?? "").trim();
  if (headline && rest.startsWith(headline)) {
    rest = rest.slice(headline.length).trim();
  }
  rest = rest
    .replace(/^[^"]*? instruction: ".*?"\.\s*/, "")
    .replace(/^Every piece now reads [^.]*\.\s*/, "")
    .replace(/^\d+ new claims?, marked new( \([^)]*\))?\.\s*/, "");
  const cut = rest.indexOf("Read as ");
  return (cut === -1 ? rest : rest.slice(0, cut)).trim();
}

export function SteerableOverview({
  readout,
  onReadout,
  selectedPiece,
  onClosePiece,
}: {
  readout: Readout;
  onReadout: (readout: Readout) => void;
  selectedPiece?: string | null;
  onClosePiece?: () => void;
}) {
  const colors = useReadoutColors();
  const [localDetail, setDetail] = useState<string | null>(null);
  const detail = selectedPiece ?? localDetail;
  const [order, setOrder] = useState(readout.pieces.map((piece) => piece.name));
  const [target, setTarget] = useState<{
    piece: string;
    claimId: string | null;
  } | null>(null);
  const [sentence, setSentence] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [panel, setPanel] = useState<Panel | null>(null);
  const request = useRef(false);
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);

  const claims = new Map(
    [...readout.claims, ...readout.unverified].map((claim) => [claim.id, claim])
  );
  const revisions: Revision[] = readout.revisions.map((rev, index) => {
    const panel = readout.panels.find(
      (candidate) => candidate.name === `steer ${index + 1}: what changed`
    );
    return {
      n: index + 1,
      panel,
      rev,
      typedOn: cell(panel, "typed on", 3) ?? rev.steer.piece,
    };
  });
  const replaced = new Set(
    revisions.flatMap((revision) =>
      (revision.panel?.rows ?? [])
        .filter((row) => row[0] === "replaced")
        .map((row) => row[1])
    )
  );
  const addedBy = new Map(
    revisions.flatMap((revision) =>
      revision.rev.claims_added.map((id) => [id, revision] as const)
    )
  );
  const piece = readout.pieces.find((candidate) => candidate.name === detail);
  const switched = revisions.find((revision) =>
    cell(revision.panel, "source", 3)
  );

  // A line replaced by a scenario stays in its revision's before view. Scenario
  // lines appear beside the place the instruction was typed, once each.
  const under = (revision: Revision) =>
    revision.typedOn === "overview"
      ? []
      : revision.rev.claims_added.filter(
          (id) =>
            readout.pieces
              .find((candidate) => candidate.name === revision.typedOn)
              ?.claim_ids.includes(id) && claims.get(id)?.scan === "steering"
        );
  const underASteer = new Set(revisions.flatMap(under));
  const steersOn = (name: string, id: string | null) =>
    revisions.filter((revision) => {
      const original = revision.rev.steer.claim_id;
      return (
        revision.typedOn === name &&
        (original && !replaced.has(original) ? original : null) === id
      );
    });
  const data: Line[] = [];
  const shown = new Set<string>();
  const addClaim = (id: string) => {
    const claim = claims.get(id);
    if (!claim || shown.has(id)) {
      return;
    }
    shown.add(id);
    data.push({ claim, kind: "claim" });
    for (const revision of steersOn(detail ?? "", id)) {
      under(revision).forEach(addClaim);
      data.push({ kind: "diff", revision });
    }
  };
  for (const revision of steersOn(detail ?? "", null)) {
    under(revision).forEach(addClaim);
    data.push({ kind: "diff", revision });
  }
  for (const id of piece?.claim_ids ?? []) {
    if (!underASteer.has(id) && !replaced.has(id)) {
      addClaim(id);
    }
  }

  const open = (name: string, claimId?: string | null) => {
    setDetail(name);
    setPanel(null);
    setError("");
    if (claimId === undefined) {
      setTarget(null);
    } else {
      setTarget({ claimId, piece: name });
      setSentence("");
    }
  };
  const close = () => {
    if (busy) {
      return;
    }
    if (panel) {
      setPanel(null);
      return;
    }
    setDetail(null);
    setTarget(null);
    setError("");
    onClosePiece?.();
  };
  const send = async () => {
    if (!target || !sentence.trim() || request.current) {
      return;
    }
    request.current = true;
    setBusy(true);
    setError("");
    try {
      const response = await apiRequest<
        PythonAPI["POST /api/rooms/{room}/steer"]["output"]
      >(roomPath(readout.room, "steer"), {
        body: JSON.stringify({
          claim_id: target.claimId,
          piece: target.piece,
          sentence: sentence.trim(),
        }),
        headers: { "Content-Type": "application/json" },
        method: "POST",
      });
      if (mounted.current) {
        onReadout(response.readout);
        setTarget(null);
        setSentence("");
      }
    } catch (error_) {
      if (mounted.current) {
        setError(error_ instanceof Error ? error_.message : String(error_));
      }
    } finally {
      request.current = false;
      if (mounted.current) {
        setBusy(false);
      }
    }
  };
  const move = (index: number, by: number) =>
    setOrder((current) => {
      const next = [...current];
      const [item] = next.splice(index, 1);
      next.splice(Math.max(0, Math.min(next.length, index + by)), 0, item);
      return next;
    });
  const heading =
    detail === "overview"
      ? "Overview"
      : piece
        ? PIECE_LABEL[piece.name]
        : "Overview";

  return (
    <View style={styles.stack}>
      <Heading>Overview</Heading>
      <Action
        title="Steer the overview"
        onPress={() => open("overview", null)}
      />
      {switched && (
        <Card>
          <Body>
            Every piece reads {cell(switched.panel, "source", 3)}, the full
            room, instead of {cell(switched.panel, "source", 2)}.
          </Body>
          <Note>
            {who(switched.rev)}: “{switched.rev.steer.instruction}”.
          </Note>
        </Card>
      )}
      {steersOn("overview", null).length > 0 && (
        <Action
          title="What changed in the overview"
          onPress={() => open("overview")}
        />
      )}
      {order.map((name, index) => {
        const current = readout.pieces.find(
          (candidate) => candidate.name === name
        );
        if (!current) {
          return null;
        }
        return (
          <Card key={name}>
            <Action
              title={`${PIECE_LABEL[name]} · ${current.status === "waiting_on_input" && current.claim_ids.length === 0 ? "Not assessed yet" : VERDICT_LABEL[current.verdict]}`}
              onPress={() => open(name)}
            />
            <Note>
              Source links: {current.corroborating_sources} agree ·{" "}
              {current.contradicting_sources} disagree
            </Note>
            <Body>{current.reason}</Body>
            <Row>
              <Action
                title="Steer this piece"
                onPress={() => open(name, null)}
              />
              <Action
                title={`Move ${PIECE_LABEL[name]} up`}
                disabled={index === 0}
                onPress={() => move(index, -1)}
              />
              <Action
                title={`Move ${PIECE_LABEL[name]} down`}
                disabled={index === order.length - 1}
                onPress={() => move(index, 1)}
              />
            </Row>
          </Card>
        );
      })}
      <Modal
        visible={detail !== null}
        animationType="slide"
        onRequestClose={close}
      >
        <SafeAreaProvider>
          <SafeAreaView style={[styles.fill, { backgroundColor: colors.bg }]}>
            <KeyboardAvoidingView
              style={styles.fill}
              behavior={Platform.OS === "ios" ? "padding" : "height"}
            >
              <View style={styles.header}>
                <Action
                  title={panel ? "Back to piece" : "Close overview detail"}
                  onPress={close}
                  disabled={busy}
                />
                <Heading>{panel?.name ?? heading}</Heading>
                {readout.synthetic_notice && (
                  <Note>{readout.synthetic_notice}</Note>
                )}
                {error ? (
                  <Text accessibilityRole="alert" style={{ color: colors.red }}>
                    {error}
                  </Text>
                ) : null}
                {!panel && target && (
                  <View style={styles.stack}>
                    <Field
                      label="Steer in one sentence"
                      value={sentence}
                      onChangeText={setSentence}
                      editable={!busy}
                      autoFocus
                      placeholder={
                        detail === "overview"
                          ? "On the overview, ask to read more: read the full room"
                          : readout.revisions.length === 0
                            ? "For example: treat the pilot as non-recurring"
                            : "Say what is wrong, in one sentence."
                      }
                      returnKeyType="send"
                      onSubmitEditing={() => void send()}
                    />
                    <Row>
                      <Action
                        title={busy ? "Steering" : "Apply steer"}
                        disabled={busy || !sentence.trim()}
                        onPress={() => void send()}
                      />
                      <Action
                        title="Cancel steer"
                        disabled={busy}
                        onPress={() => setTarget(null)}
                      />
                    </Row>
                  </View>
                )}
              </View>
              {panel ? (
                <FlatList
                  renderScrollComponent={renderReadoutScroll}
                  data={panel.rows}
                  keyExtractor={(_, index) => String(index)}
                  contentContainerStyle={styles.content}
                  renderItem={({ item }) => (
                    <Card>
                      {item.map((value, index) => (
                        <View key={index}>
                          <Note>
                            {panel.columns[index] ?? String(index + 1)}
                          </Note>
                          <Body>{value}</Body>
                        </View>
                      ))}
                    </Card>
                  )}
                />
              ) : (
                <FlatList
                  renderScrollComponent={renderReadoutScroll}
                  data={data}
                  keyExtractor={(item) =>
                    item.kind === "claim"
                      ? `claim:${item.claim.id}`
                      : `revision:${item.revision.n}`
                  }
                  keyboardShouldPersistTaps="handled"
                  contentContainerStyle={styles.content}
                  ListHeaderComponent={
                    <View style={styles.stack}>
                      {piece && (
                        <>
                          <Body>{piece.reason}</Body>
                          <Note>
                            Source links: {piece.corroborating_sources} agree ·{" "}
                            {piece.contradicting_sources} disagree
                          </Note>
                        </>
                      )}
                      {!target && (
                        <Action
                          title={
                            detail === "overview"
                              ? "Steer the overview"
                              : "Steer this piece"
                          }
                          onPress={() => {
                            setTarget({
                              claimId: null,
                              piece: detail ?? "overview",
                            });
                            setSentence("");
                          }}
                        />
                      )}
                    </View>
                  }
                  ListEmptyComponent={<Note>No claims in this piece yet.</Note>}
                  renderItem={({ item }) =>
                    item.kind === "claim" ? (
                      <ClaimLine
                        claim={item.claim}
                        readout={readout}
                        addedBy={addedBy.get(item.claim.id)}
                        onPanel={setPanel}
                        onSteer={() => {
                          setTarget({
                            claimId: item.claim.id,
                            piece: detail ?? "overview",
                          });
                          setSentence("");
                        }}
                      />
                    ) : (
                      <Diff
                        revision={item.revision}
                        readout={readout}
                        claims={claims}
                        onPanel={setPanel}
                      />
                    )
                  }
                />
              )}
            </KeyboardAvoidingView>
          </SafeAreaView>
        </SafeAreaProvider>
      </Modal>
    </View>
  );
}

function ClaimLine({
  claim,
  readout,
  addedBy,
  onSteer,
  onPanel,
}: {
  claim: Claim;
  readout: Readout;
  addedBy?: Revision;
  onSteer?: () => void;
  onPanel: (panel: Panel) => void;
}) {
  const colors = useReadoutColors();
  const panel = readout.panels.find(
    (candidate) =>
      !candidate.name.startsWith("steer ") &&
      claim.text.includes(`'${candidate.name}'`)
  );
  return (
    <Card>
      {addedBy && (
        <Note>
          {claim.scan === "steering"
            ? who(addedBy.rev)
            : `new, ${who(addedBy.rev)}`}
        </Note>
      )}
      {claim.scan === "steering" && <Note>Operator scenario</Note>}
      <View
        style={[
          styles.claim,
          {
            borderLeftColor:
              claim.scan === "steering"
                ? colors.amber
                : claim.severity === "flag"
                  ? colors.red
                  : "transparent",
          },
        ]}
      >
        <Body>{claim.text}</Body>
      </View>
      {claim.sources.map((source, index) => (
        <SourceChip
          key={index}
          room={readout.room}
          source={source}
          n={index + 1}
          claimId={claim.id}
          revision={`${readout.built_at}:${readout.revisions.length}`}
        />
      ))}
      {panel && (
        <Action
          title={`Show the rows it sums (${panel.rows.length} lines)`}
          onPress={() => onPanel(panel)}
        />
      )}
      {onSteer && <Action title="Steer this line" onPress={onSteer} />}
    </Card>
  );
}

function Diff({
  revision,
  readout,
  claims,
  onPanel,
}: {
  revision: Revision;
  readout: Readout;
  claims: Map<string, Claim>;
  onPanel: (panel: Panel) => void;
}) {
  const { rev, panel, n } = revision;
  const headline =
    cell(panel, "headline", 3) ??
    (rev.steer.kind === "more_info" ? "More info" : "Rewritten");
  return (
    <Card>
      <Note>Steer {n}</Note>
      <Heading>{headline}</Heading>
      <Body>
        {who(rev)}: “{rev.steer.instruction}”
      </Body>
      {(panel?.rows ?? [])
        .filter((row) => row[0] === "replaced")
        .map((row, index) => (
          <View key={`before:${index}`}>
            <Note>Before, the check&apos;s line (kept):</Note>
            {claims.get(row[1]) ? (
              <ClaimLine
                claim={claims.get(row[1])!}
                readout={readout}
                onPanel={onPanel}
              />
            ) : (
              <Body>{row[2]}</Body>
            )}
          </View>
        ))}
      {(panel?.rows ?? [])
        .filter((row) => row[0] === "dropped")
        .map((row, index) => (
          <Body key={`dropped:${index}`}>Dropped: {row[2]}</Body>
        ))}
      {(panel?.rows ?? [])
        .filter((row) => row[0] === "wording")
        .map((row, index) => (
          <View key={`wording:${index}`}>
            <Note>Reworded, before:</Note>
            <Body>{row[2]}</Body>
            <Note>After:</Note>
            <Body>{row[3]}</Body>
          </View>
        ))}
      {rev.steer.kind === "more_info" && rev.claims_added.length > 0 && (
        <Body>
          {rev.claims_added.length} new lines, marked new in their pieces. New
          sources:{" "}
          {[
            ...new Set(
              rev.sources_added.map((source) => source.split(", ")[0])
            ),
          ].join("; ")}
        </Body>
      )}
      {said(rev, headline) ? <Body>{said(rev, headline)}</Body> : null}
    </Card>
  );
}

const styles = StyleSheet.create({
  claim: {
    borderLeftColor: "transparent",
    borderLeftWidth: 3,
    paddingLeft: 10,
  },
  content: {
    alignSelf: "center",
    gap: 12,
    maxWidth: 960,
    padding: 16,
    width: "100%",
  },
  fill: { flex: 1 },
  header: { gap: 12, padding: 16 },
  stack: { gap: 12 },
});
