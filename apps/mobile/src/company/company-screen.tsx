import * as Clipboard from "expo-clipboard";
import { router, useLocalSearchParams } from "expo-router";
import type { PropsWithChildren } from "react";
import { useState } from "react";
import {
  KeyboardAvoidingView,
  Linking,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  View,
} from "react-native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";

import {
  Action,
  Body,
  Card,
  Field,
  Heading,
  Note,
  Row,
  useReadoutColors,
} from "../readout/ui";
import { data } from "./data";
import {
  draftRequest,
  requestItems,
  resolveCompany,
  safeWebUrl,
} from "./model";
import type {
  Company,
  ResearchClaim,
  ResearchSection,
  SetupField,
  Stage,
} from "./model";

const styles = StyleSheet.create({
  brand: { fontFamily: "ArchivoDisplay", fontSize: 22, letterSpacing: -0.7 },
  check: { fontSize: 24, lineHeight: 28 },
  checkRow: {
    borderBottomWidth: 1,
    flexDirection: "row",
    gap: 12,
    paddingVertical: 16,
  },
  checkText: { flex: 1, gap: 4 },
  claim: { borderBottomWidth: 1, gap: 8, paddingVertical: 16 },
  content: {
    alignSelf: "center",
    gap: 24,
    maxWidth: 1264,
    padding: 16,
    paddingBottom: 48,
    width: "100%",
  },
  draft: {
    fontFamily: "PlexMono",
    fontSize: 14,
    lineHeight: 22,
    minHeight: 360,
  },
  emphasis: { fontFamily: "ArchivoBold" },
  group: { gap: 8 },
  hero: { gap: 16, paddingVertical: 16 },
  lede: { fontSize: 20, lineHeight: 29, maxWidth: 720 },
  masthead: {
    alignItems: "center",
    borderBottomWidth: 1,
    flexDirection: "row",
    gap: 16,
    justifyContent: "space-between",
    paddingHorizontal: 24,
    paddingVertical: 16,
  },
  mono: { fontFamily: "PlexMono", fontSize: 12, letterSpacing: 0.5 },
  screen: { flex: 1 },
  section: { borderTopWidth: 1, gap: 16, paddingTop: 24 },
  sectionTitle: {
    fontFamily: "ArchivoDisplay",
    fontSize: 28,
    letterSpacing: -0.6,
    lineHeight: 34,
  },
  sheetContent: {
    alignSelf: "center",
    gap: 16,
    maxWidth: 900,
    padding: 24,
    paddingBottom: 48,
    width: "100%",
  },
  sheetHeader: {
    alignItems: "center",
    borderBottomWidth: 1,
    flexDirection: "row",
    gap: 16,
    justifyContent: "space-between",
    padding: 16,
  },
  snapshot: { borderBottomWidth: 1, borderTopWidth: 1, paddingVertical: 16 },
  source: {
    borderRadius: 4,
    borderWidth: 1,
    flexShrink: 1,
    justifyContent: "center",
    minHeight: 44,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  start: {
    alignSelf: "center",
    gap: 24,
    maxWidth: 720,
    padding: 24,
    paddingTop: 64,
    width: "100%",
  },
  title: {
    fontFamily: "ArchivoDisplay",
    fontSize: 44,
    letterSpacing: -2,
    lineHeight: 46,
  },
});

const stages: {
  id: Stage;
  title: string;
}[] = [
  { id: "pre_seed", title: "Pre-seed" },
  { id: "seed", title: "Seed" },
  { id: "series_a", title: "Series A" },
];
const fieldLabels = {
  batch: "Batch",
  founders: "Founders",
  location: "Location",
  name: "Name",
  team_size: "Team size",
  website: "Website",
};
const Sheet = ({
  title,
  onClose,
  children,
}: PropsWithChildren<{
  title: string;
  onClose: () => void;
}>) => {
  const colors = useReadoutColors();
  return (
    <Modal
      visible
      animationType="slide"
      onRequestClose={onClose}
      presentationStyle="pageSheet"
    >
      <SafeAreaProvider>
        <SafeAreaView style={[styles.screen, { backgroundColor: colors.bg }]}>
          <View style={[styles.sheetHeader, { borderColor: colors.line }]}>
            <Heading>{title}</Heading>
            <Action title="Done" onPress={onClose} />
          </View>
          <KeyboardAvoidingView
            style={styles.screen}
            enabled={Platform.OS !== "web"}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
          >
            <ScrollView
              keyboardShouldPersistTaps="handled"
              contentContainerStyle={styles.sheetContent}
            >
              {children}
            </ScrollView>
          </KeyboardAvoidingView>
        </SafeAreaView>
      </SafeAreaProvider>
    </Modal>
  );
};
const SourceEvidence = ({
  claim,
  onClose,
}: {
  claim: ResearchClaim;
  onClose: () => void;
}) => {
  const [error, setError] = useState("");
  const source = claim.source ? data.sources[claim.source] : undefined;
  const url = safeWebUrl(claim.url ?? source?.url ?? "");
  const openSource = async () => {
    if (!url) {
      return;
    }
    try {
      await Linking.openURL(url);
    } catch {
      setError("Could not open this source. You can copy the URL below.");
    }
  };
  return (
    <Sheet title="Evidence" onClose={onClose}>
      <Note>PUBLIC SOURCE · SAVED SNAPSHOT</Note>
      <Heading>{source?.title ?? "Source unavailable"}</Heading>
      <Body>{claim.text}</Body>
      {claim.excerpt ? (
        <Card>
          <Note>{claim.excerpt.before}</Note>
          <Body style={styles.emphasis}>{claim.excerpt.match}</Body>
          <Note>{claim.excerpt.after}</Note>
        </Card>
      ) : null}
      {!claim.excerpt && claim.quote ? (
        <Card>
          <Body>{claim.quote}</Body>
        </Card>
      ) : null}
      {!claim.excerpt && !claim.quote && (
        <Note>No excerpt is included in this saved record.</Note>
      )}
      {url && (
        <>
          <Action title="Open original source ↗" onPress={openSource} />
          <Note>{url}</Note>
        </>
      )}
      {error ? <Body accessibilityRole="alert">{error}</Body> : null}
      <Note>Saved research: {data.built.replace("T", " ")}</Note>
      <Note>{source?.path}</Note>
    </Sheet>
  );
};
const ClaimLine = ({
  claim,
  number,
  onSource,
}: {
  claim: ResearchClaim;
  number: number;
  onSource: (claim: ResearchClaim) => void;
}) => {
  const colors = useReadoutColors();
  const source = claim.source && data.sources[claim.source];
  return (
    <View style={[styles.claim, { borderColor: colors.line }]}>
      <Body style={claim.placeholder ? { color: colors.muted } : undefined}>
        {claim.text}
      </Body>
      <Row>
        {claim.placeholder ? <Note>Not researched yet</Note> : null}
        {!claim.placeholder && claim.kind ? <Note>{claim.kind}</Note> : null}
        {source && (
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={`Evidence ${number}: ${source.title}`}
            onPress={() => onSource(claim)}
            style={({ pressed }) => [
              styles.source,
              { borderColor: colors.line, opacity: pressed ? 0.6 : 1 },
            ]}
          >
            <Note style={styles.mono}>
              [{number}] {source.title}
            </Note>
          </Pressable>
        )}
        {!source && !claim.placeholder && (
          <Note>Source unavailable in this snapshot</Note>
        )}
      </Row>
    </View>
  );
};
const Section = ({
  section,
  onSource,
}: {
  section: ResearchSection;
  onSource: (claim: ResearchClaim) => void;
}) => {
  const colors = useReadoutColors();
  const groups = section.parts?.map((part) => ({
    claims: part.claims,
    subtitle: "",
    title: part.label,
  })) ??
    section.cards?.map((card) => ({
      claims: card.claims,
      subtitle: card.role,
      title: card.name,
    })) ?? [{ claims: section.claims ?? [], subtitle: "", title: "" }];
  const claims = groups.flatMap((group) => group.claims);
  return (
    <View style={[styles.section, { borderColor: colors.line }]}>
      <Heading style={styles.sectionTitle}>{section.title}</Heading>
      {groups.map((group) => (
        <View key={group.title || section.key} style={styles.group}>
          {group.title ? (
            <Body style={styles.emphasis}>{group.title}</Body>
          ) : null}
          {group.subtitle ? <Note>{group.subtitle}</Note> : null}
          {group.claims.map((claim) => (
            <ClaimLine
              key={claim.text}
              claim={claim}
              number={claims.indexOf(claim) + 1}
              onSource={onSource}
            />
          ))}
        </View>
      ))}
      {section.gaps?.map((gap) => (
        <Card key={gap.text}>
          <Note>GAP</Note>
          <Body>{gap.text}</Body>
          <Note>{gap.why}</Note>
        </Card>
      ))}
    </View>
  );
};
const setupFor = (company: Company): Record<string, SetupField> => {
  const saved = data.research[company.slug]?.setup;
  if (saved) {
    return Object.fromEntries(
      Object.entries(saved).map(([key, value]) => [key, { ...value }])
    );
  }
  const founders = data.yc_founders[company.slug];
  return {
    batch: { source: data.list_source, value: company.batch },
    founders: {
      source: founders?.[0]?.source,
      value: founders?.map((founder) => founder.name).join(", ") ?? "",
    },
    location: { source: data.list_source, value: company.regions[0] ?? "" },
    name: { source: data.list_source, value: company.name },
    stage: {
      note: "Set by the associate; not confirmed by research",
      value: "seed",
    },
    team_size: { source: data.list_source, value: String(company.team_size) },
    website: { source: data.list_source, value: company.website },
  };
};
const fieldProvenance = (field: SetupField | undefined): string => {
  if (field?.edited) {
    return "Corrected by you";
  }
  if (field?.source) {
    return data.sources[field.source]?.title ?? "Source unavailable";
  }
  return "Not in the saved files";
};
const CompanyWorkspace = ({ company }: { company: Company }) => {
  const colors = useReadoutColors();
  const research = data.research[company.slug];
  const [fields, setFields] = useState(() => setupFor(company));
  const [setup, setSetup] = useState(false);
  const [request, setRequest] = useState(false);
  const [evidence, setEvidence] = useState<ResearchClaim | null>(null);
  const [stage, setStage] = useState<Stage>(() => {
    const value = research?.setup.stage?.value;
    if (value === "series_a" || value === "pre_seed") {
      return value;
    }
    return "seed";
  });
  const [items, setItems] = useState(() =>
    requestItems(data.checklist, stage, research)
  );
  const [custom, setCustom] = useState("");
  const [copyStatus, setCopyStatus] = useState("");
  const [editedDraft, setEditedDraft] = useState<string | null>(null);
  const generated = draftRequest(
    fields.name.value,
    fields.founders.value,
    items
  );
  const draft = editedDraft ?? generated;
  const selected = items.filter((item) => item.checked).length;
  const changeStage = (next: Stage) => {
    setStage(next);
    setFields((current) => ({
      ...current,
      stage: { ...current.stage, edited: true, value: next },
    }));
    setItems((current) => [
      ...requestItems(data.checklist, next, research).map((item) => ({
        ...item,
        checked:
          current.find((previous) => previous.id === item.id)?.checked ?? true,
      })),
      ...current.filter((item) => item.id.startsWith("custom-")),
    ]);
    setCopyStatus("");
  };
  const addItem = () => {
    const text = custom.trim();
    if (!text) {
      return;
    }
    setItems((current) => [
      ...current,
      {
        ask: text,
        checked: true,
        guidance: "",
        id: `custom-${Date.now()}-${current.length}`,
        reason: "Added by you",
        title: text,
      },
    ]);
    setCustom("");
    setCopyStatus("");
  };
  const copyDraft = async () => {
    try {
      setCopyStatus(
        (await Clipboard.setStringAsync(draft))
          ? "Copied. Nothing has been sent."
          : "Could not copy. Select the draft to copy it manually."
      );
    } catch {
      setCopyStatus("Could not copy. Select the draft to copy it manually.");
    }
  };
  return (
    <>
      <ScrollView
        keyboardShouldPersistTaps="handled"
        contentContainerStyle={styles.content}
      >
        <Row>
          <Action
            title="← Company URL"
            onPress={() => router.setParams({ company: "" })}
          />
          <Note style={styles.mono}>FIRST READOUT / BEFORE THE ROOM</Note>
        </Row>
        <View style={styles.hero}>
          <Heading style={styles.title}>
            {fields.name.value || company.name}
          </Heading>
          <Body style={styles.lede}>{company.one_liner}</Body>
          <Row>
            <Note>{fields.batch.value}</Note>
            <Note>· {fields.location.value}</Note>
            <Note>· {stages.find((entry) => entry.id === stage)?.title}</Note>
          </Row>
          <Row>
            <Action title="Company details" onPress={() => setSetup(true)} />
            <Action
              title="Draft the data-room request"
              primary
              onPress={() => setRequest(true)}
            />
          </Row>
        </View>
        <View style={[styles.snapshot, { borderColor: colors.line }]}>
          <Note>
            Saved public research · {data.built.slice(0, 10)}. This is a
            snapshot, not a live research run.
          </Note>
        </View>
        {research ? (
          research.sections.map((section) => (
            <Section
              key={section.key}
              section={section}
              onSource={setEvidence}
            />
          ))
        ) : (
          <Card>
            <Heading>No saved research yet</Heading>
            <Body>
              The company matched the YC directory, but its public research has
              not been collected in this snapshot.
            </Body>
            <Note>
              You can correct the company details and prepare a stage-based
              request.
            </Note>
          </Card>
        )}
        {research && (
          <View style={styles.section}>
            <Heading style={styles.sectionTitle}>
              What only a data room can answer
            </Heading>
            <Note>These gaps become the first items in your request.</Note>
            {research.room_gaps.map((gap) => (
              <Card key={gap.text}>
                <Body>{gap.text}</Body>
                <Note>{gap.why}</Note>
              </Card>
            ))}
          </View>
        )}
        <Card>
          <Heading>The next step</Heading>
          <Body>
            Review what you need from the founder, then copy the request into
            your own message.
          </Body>
          <Row>
            <Action
              primary
              title={`Review request · ${selected} items`}
              onPress={() => setRequest(true)}
            />
          </Row>
        </Card>
        <View style={styles.section}>
          <Note>
            The existing room analysis is available separately for the sample
            data rooms.
          </Note>
          <Action
            title="Open sample room analysis"
            onPress={() => router.push("/rooms")}
          />
        </View>
      </ScrollView>
      {setup && (
        <Sheet title="Company details" onClose={() => setSetup(false)}>
          <Note>
            Matched from the saved YC directory. Corrections apply to this
            readout and the request draft.
          </Note>
          {Object.entries(fieldLabels).map(([key, label]) => (
            <View key={key} style={styles.group}>
              <Field
                label={label}
                value={fields[key]?.value ?? ""}
                onChangeText={(value) =>
                  setFields((current) => ({
                    ...current,
                    [key]: { ...current[key], edited: true, value },
                  }))
                }
              />
              <Note>{fieldProvenance(fields[key])}</Note>
              {fields[key]?.source && (
                <Action
                  title={`Source for ${label.toLowerCase()}`}
                  onPress={() => {
                    setSetup(false);
                    setEvidence({
                      source: fields[key].source,
                      text: `${label} in the saved record: ${setupFor(company)[key].value}`,
                    });
                  }}
                />
              )}
            </View>
          ))}
          <Heading>Stage</Heading>
          <Row>
            {stages.map((entry) => (
              <Action
                key={entry.id}
                title={`${stage === entry.id ? "✓ " : ""}${entry.title}`}
                onPress={() => changeStage(entry.id)}
              />
            ))}
          </Row>
          <Note>
            {fields.stage.edited
              ? "Corrected by you"
              : (fields.stage.note ?? "From the saved research")}
          </Note>
        </Sheet>
      )}
      {request && (
        <Sheet title="Data-room request" onClose={() => setRequest(false)}>
          <Note>
            {fields.name.value} ·{" "}
            {stages.find((entry) => entry.id === stage)?.title} · {selected}{" "}
            selected
          </Note>
          <Body>
            Check what you need. Each item includes guidance for the founder.
          </Body>
          {items.map((item) => (
            <Pressable
              key={item.id}
              accessibilityRole="checkbox"
              accessibilityState={{ checked: item.checked }}
              accessibilityLabel={item.title}
              onPress={() => {
                setItems((current) =>
                  current.map((entry) =>
                    entry.id === item.id
                      ? { ...entry, checked: !entry.checked }
                      : entry
                  )
                );
                setCopyStatus("");
              }}
              style={({ pressed }) => [
                styles.checkRow,
                { borderColor: colors.line, opacity: pressed ? 0.6 : 1 },
              ]}
            >
              <Body
                style={[
                  styles.check,
                  { color: item.checked ? colors.accent : colors.muted },
                ]}
              >
                {item.checked ? "☑" : "□"}
              </Body>
              <View style={styles.checkText}>
                <Body style={styles.emphasis}>{item.title}</Body>
                <Note>{item.reason}</Note>
                {item.guidance ? <Note>{item.guidance}</Note> : null}
              </View>
            </Pressable>
          ))}
          <Field
            label="Add an item"
            value={custom}
            onChangeText={setCustom}
            onSubmitEditing={addItem}
            placeholder="What else do you need?"
          />
          <Action
            title="Add to request"
            disabled={!custom.trim()}
            onPress={addItem}
          />
          <Heading>Message to the founder</Heading>
          <Note>
            The draft updates with your selections until you edit it. Nothing is
            sent from this screen.
          </Note>
          {editedDraft !== null && (
            <Card>
              <Note>
                You edited this draft. Checklist changes are preserved, but will
                not overwrite your words.
              </Note>
              <Action
                title="Regenerate from selected items"
                onPress={() => {
                  setEditedDraft(null);
                  setCopyStatus("");
                }}
              />
            </Card>
          )}
          <Field
            label="Draft message"
            multiline
            value={draft}
            onChangeText={(value) => {
              setEditedDraft(value);
              setCopyStatus("");
            }}
            style={styles.draft}
          />
          <Action
            title="Copy request"
            primary
            disabled={!selected || !draft.trim()}
            onPress={copyDraft}
          />
          {copyStatus ? (
            <Note accessibilityLiveRegion="polite">{copyStatus}</Note>
          ) : null}
        </Sheet>
      )}
      {evidence && (
        <SourceEvidence claim={evidence} onClose={() => setEvidence(null)} />
      )}
    </>
  );
};
export const CompanyScreen = () => {
  const colors = useReadoutColors();
  const params = useLocalSearchParams<{
    company?: string | string[];
  }>();
  const parameter = Array.isArray(params.company)
    ? params.company[0]
    : params.company;
  const company = parameter ? resolveCompany(parameter, data.companies) : null;
  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const start = (value: string) => {
    if (!resolveCompany(value, data.companies)) {
      setError(
        "This URL does not match a company in the saved YC Spring 2026 directory. Try its website or exact YC company page."
      );
      return;
    }
    setError("");
    router.setParams({ company: value.trim() });
  };
  return (
    <SafeAreaView style={[styles.screen, { backgroundColor: colors.bg }]}>
      {Platform.OS !== "web" && (
        <View style={[styles.masthead, { borderColor: colors.line }]}>
          <Body style={styles.brand}>Tricorder</Body>
          <Note style={styles.mono}>EVERY CLAIM SOURCED</Note>
        </View>
      )}
      {company ? (
        <CompanyWorkspace key={company.slug} company={company} />
      ) : (
        <ScrollView
          keyboardShouldPersistTaps="handled"
          contentContainerStyle={styles.start}
        >
          <Note style={styles.mono}>01 / COMPANY URL</Note>
          <Heading style={styles.title}>Which company?</Heading>
          <Body style={styles.lede}>Point it at a startup, get a readout.</Body>
          <Note>
            Paste the company’s website or its YC company page. The saved
            research opens automatically.
          </Note>
          <Field
            label="Company URL"
            value={input}
            onChangeText={setInput}
            placeholder="https://ploy.ai"
            autoCapitalize="none"
            autoCorrect={false}
            keyboardType="url"
            returnKeyType="go"
            onSubmitEditing={() => start(input)}
          />
          <Action
            title="Start readout →"
            primary
            onPress={() => start(input)}
            disabled={!input.trim()}
          />
          {error || parameter ? (
            <Body accessibilityRole="alert" style={{ color: colors.red }}>
              {error || "No matching company found for the URL in this link."}
            </Body>
          ) : null}
          <Row>
            <Note>Try a saved readout</Note>
            <Action title="Ploy" onPress={() => start("https://ploy.ai")} />
            <Action
              title="Sazabi"
              onPress={() => start("https://www.sazabi.com")}
            />
          </Row>
          <Note>
            {data.companies.length} companies in the saved YC Spring 2026
            directory. Public research is available for Ploy and Sazabi.
          </Note>
          <Action
            title="Open sample room analysis"
            onPress={() => router.push("/rooms")}
          />
        </ScrollView>
      )}
    </SafeAreaView>
  );
};

export default CompanyScreen;
