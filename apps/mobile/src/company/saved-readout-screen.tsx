import type {
  CompanyEvidence,
  CompanyInsight,
  CompanyReadout,
  CompanySectionKey,
  CompanySectionResponse,
} from "@tricorder/schema/company";
import { router, useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import { Linking, Platform, ScrollView, StyleSheet, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { AnnotationToolbar } from "../annotations/annotation-panel";
import { AnnotationItem, AnnotationScope } from "../annotations/context";
import { NativeSheet } from "../readout/native-sheet";
import {
  Action,
  Body,
  Card,
  Heading,
  Note,
  useReadoutColors,
} from "../readout/ui";
import { getCompanyReadout, getCompanySection } from "./api";
import { CitedText } from "./cited-text";
import { CompanyCarousel } from "./company-carousel";
import { safeWebUrl } from "./model";
import { CompanyRoomArrivals } from "./room-arrival";
import { SavedRequest } from "./saved-request";

const styles = StyleSheet.create({
  content: {
    alignSelf: "center",
    gap: 28,
    maxWidth: 1000,
    padding: 20,
    paddingBottom: 60,
    width: "100%",
  },
  evidenceRow: {
    alignItems: "flex-start",
    borderBottomWidth: 1,
    gap: 16,
    paddingVertical: 16,
  },
  evidenceText: { gap: 8 },
  group: { gap: 12 },
  heading: { fontFamily: "ArchivoDisplay", fontSize: 34, lineHeight: 41 },
  lede: { fontSize: 19, lineHeight: 29 },
  screen: { flex: 1 },
  section: { borderTopWidth: 1, gap: 20, paddingTop: 24 },
  skeleton: { borderRadius: 4, height: 18 },
});

const Skeleton = ({ title }: { title: string }) => {
  const colors = useReadoutColors();
  return (
    <View
      accessibilityLabel={`Loading ${title}`}
      accessibilityState={{ busy: true }}
      style={styles.group}
    >
      <Heading>{title}</Heading>
      <View style={[styles.skeleton, { backgroundColor: colors.line }]} />
      <View
        style={[
          styles.skeleton,
          { backgroundColor: colors.line, width: "80%" },
        ]}
      />
      <Note>Loading saved evidence…</Note>
    </View>
  );
};

const EvidenceSheet = ({
  evidence,
  snapshotAt,
  company,
  onClose,
}: {
  evidence: CompanyEvidence;
  snapshotAt: string;
  company: CompanyReadout["company"];
  onClose: () => void;
}) => {
  const [error, setError] = useState("");
  const [source] = evidence.claim.sources;
  const url = source && source.kind !== "file" ? safeWebUrl(source.uri) : null;
  const openOriginal = async () => {
    if (!url) {
      return;
    }
    try {
      await Linking.openURL(url);
    } catch {
      setError(
        "Could not open the original. The saved passage remains available below."
      );
    }
  };
  return (
    <AnnotationScope
      id={`company:${company.slug}/evidence:${evidence.id}`}
      label={`${company.name} · ${evidence.sourceTitle}`}
    >
      <NativeSheet visible onClose={onClose}>
        <View style={{ gap: 12, padding: 16 }}>
          <Heading>Evidence [{evidence.number}]</Heading>
          <Action compact title="Done" onPress={onClose} />
        </View>
        <ScrollView contentContainerStyle={styles.content}>
          <Note>Saved public research · {snapshotAt.replace("T", " ")}</Note>
          <Heading>{evidence.sourceTitle}</Heading>
          <Body>{evidence.claim.text}</Body>
          {evidence.qualification ? (
            <Note>{evidence.qualification}</Note>
          ) : null}
          <Card>
            <Heading>Saved passage</Heading>
            {evidence.excerpt?.before ? (
              <Note>{evidence.excerpt.before}</Note>
            ) : null}
            <Body>
              {source?.quote ||
                "No source passage is available in this snapshot."}
            </Body>
            {evidence.excerpt?.after ? (
              <Note>{evidence.excerpt.after}</Note>
            ) : null}
          </Card>
          {source ? <Note>{source.locator}</Note> : null}
          {url ? (
            <>
              <Action title="Open original source" onPress={openOriginal} />
              <Body>{url}</Body>
            </>
          ) : (
            <Note>This source is retained as a saved research record.</Note>
          )}
          {error ? <Body accessibilityRole="alert">{error}</Body> : null}
        </ScrollView>
      </NativeSheet>
    </AnnotationScope>
  );
};

const insightMarks = {
  mixed: "Mixed",
  strong: "Looking strong",
  thin: "Not enough yet",
  weak: "Looking weak",
};
const Insight = ({
  insight,
  readout,
  onOpen,
}: {
  insight: CompanyInsight;
  readout: CompanyReadout;
  onOpen: (entry: CompanyEvidence) => void;
}) => {
  const colors = useReadoutColors();
  const markColors = {
    mixed: colors.amber,
    strong: colors.green,
    thin: colors.amber,
    weak: colors.red,
  };
  const color = markColors[insight.mark];
  return (
    <AnnotationScope
      id={`company:${readout.company.slug}/insight:${insight.id}`}
      label={`${readout.company.name} · ${insight.piece}`}
    >
      <Card>
        <Note style={{ color }}>{insightMarks[insight.mark]}</Note>
        <Heading>{insight.piece}</Heading>
        <Body style={{ fontFamily: "ArchivoBold" }}>{insight.title}</Body>
        <CitedText
          segments={insight.segments ?? [insight]}
          evidence={readout.evidence}
          onOpen={onOpen}
        />
      </Card>
    </AnnotationScope>
  );
};

const LoadedSection = ({
  response,
  onOpen,
}: {
  response: CompanySectionResponse;
  onOpen: (entry: CompanyEvidence) => void;
}) => {
  const colors = useReadoutColors();
  const { section, evidence } = response;
  const empty =
    section.groups.every(
      (group) =>
        group.evidenceIds.length === 0 && group.unavailable.length === 0
    ) && section.gaps.length === 0;
  return (
    <AnnotationScope
      id={`company:${response.company.slug}/section:${section.key}`}
      label={`${response.company.name} · ${section.title}`}
    >
      <View style={styles.group}>
        <Heading>{section.title}</Heading>
        {empty ? <Note>No saved evidence for this section.</Note> : null}
        {section.groups.map((group) => (
          <AnnotationItem
            key={group.id}
            id={`group:${group.id}`}
            label={group.title || section.title}
          >
            <View style={styles.group}>
              {group.title ? <Heading>{group.title}</Heading> : null}
              {group.subtitle ? <Note>{group.subtitle}</Note> : null}
              {group.evidenceIds.map((id) => {
                const entry = evidence[id];
                return entry ? (
                  <AnnotationItem
                    key={id}
                    id={`evidence:${id}`}
                    label={entry.sourceTitle}
                  >
                    <View
                      style={[styles.evidenceRow, { borderColor: colors.line }]}
                    >
                      <View style={styles.evidenceText}>
                        <CitedText
                          segments={[
                            { evidenceIds: [id], text: entry.claim.text },
                          ]}
                          evidence={evidence}
                          onOpen={onOpen}
                        />
                        {entry.qualification ? (
                          <Note>{entry.qualification}</Note>
                        ) : null}
                      </View>
                    </View>
                  </AnnotationItem>
                ) : (
                  <Note key={id}>Evidence unavailable</Note>
                );
              })}
              {group.unavailable.map((text) => (
                <AnnotationItem
                  key={text}
                  id={`unavailable:${text}`}
                  label={text}
                >
                  <Card>
                    <Note>Not researched yet</Note>
                    <Body>{text}</Body>
                  </Card>
                </AnnotationItem>
              ))}
            </View>
          </AnnotationItem>
        ))}
        {section.gaps.map((gap) => (
          <AnnotationItem
            key={gap.text}
            id={`gap:${gap.text}`}
            label={gap.text}
          >
            <Card>
              <Note>Unknown</Note>
              <Body>{gap.text}</Body>
              <Note>{gap.why}</Note>
            </Card>
          </AnnotationItem>
        ))}
      </View>
    </AnnotationScope>
  );
};

const SectionFetch = ({
  readout,
  sectionKey,
  title,
  onOpen,
  onRetry,
}: {
  readout: CompanyReadout;
  sectionKey: CompanySectionKey;
  title: string;
  onOpen: (entry: CompanyEvidence) => void;
  onRetry: () => void;
}) => {
  const [response, setResponse] = useState<CompanySectionResponse | null>(null);
  const [error, setError] = useState("");
  const company = readout.company.slug;
  const snapshot = readout.snapshotAt;
  useEffect(() => {
    const abort = new AbortController();
    const load = async () => {
      try {
        const next = await getCompanySection(company, sectionKey, abort.signal);
        if (
          next.company.slug !== company ||
          next.snapshotAt !== snapshot ||
          next.section.key !== sectionKey
        ) {
          if (!abort.signal.aborted) {
            setError(
              "The saved section does not belong to this readout. Reopen the company to refresh its snapshot."
            );
          }
          return;
        }
        if (!abort.signal.aborted) {
          setResponse(next);
        }
      } catch (error_) {
        if (!abort.signal.aborted) {
          setError(
            error_ instanceof Error
              ? error_.message
              : "This section could not be loaded."
          );
        }
      }
    };
    void load();
    return () => abort.abort();
  }, [company, sectionKey, snapshot]);
  if (error) {
    return (
      <Card>
        <Heading>{title}</Heading>
        <Body accessibilityRole="alert">{error}</Body>
        <Action title={`Retry ${title}`} onPress={onRetry} />
      </Card>
    );
  }
  return response ? (
    <LoadedSection response={response} onOpen={onOpen} />
  ) : (
    <Skeleton title={title} />
  );
};

const IndependentSection = ({
  readout,
  sectionKey,
  title,
  onOpen,
}: {
  readout: CompanyReadout;
  sectionKey: CompanySectionKey;
  title: string;
  onOpen: (entry: CompanyEvidence) => void;
}) => {
  const [attempt, setAttempt] = useState(0);
  const colors = useReadoutColors();
  return (
    <View style={[styles.section, { borderColor: colors.line }]}>
      <SectionFetch
        key={attempt}
        readout={readout}
        sectionKey={sectionKey}
        title={title}
        onOpen={onOpen}
        onRetry={() => setAttempt((value) => value + 1)}
      />
    </View>
  );
};

const WorkingPage = ({ readout }: { readout: CompanyReadout }) => {
  const [evidence, setEvidence] = useState<CompanyEvidence | null>(null);
  const [requestOpen, setRequestOpen] = useState(false);
  return (
    <AnnotationScope
      id={`company:${readout.company.slug}`}
      label={`${readout.company.name} · Company report`}
    >
      <View style={styles.group}>
        <Heading style={styles.heading}>{readout.company.name}</Heading>
        <CitedText
          style={styles.lede}
          segments={readout.summary.segments ?? [readout.summary]}
          evidence={readout.evidence}
          onOpen={setEvidence}
        />
        <Note>Saved public research · {readout.snapshotAt.slice(0, 10)}</Note>
      </View>
      <View style={styles.group}>
        <Heading>What stands out</Heading>
        <Note>Team-authored readings of the saved sources.</Note>
        {readout.insights.map((insight) => (
          <Insight
            key={insight.id}
            insight={insight}
            readout={readout}
            onOpen={setEvidence}
          />
        ))}
      </View>
      <CompanyRoomArrivals
        key={readout.company.slug}
        company={readout.company}
      />
      {readout.sections.map((section) => (
        <IndependentSection
          key={section.key}
          readout={readout}
          sectionKey={section.key}
          title={section.title}
          onOpen={setEvidence}
        />
      ))}
      <Card>
        <Heading>Up Next: Data Room Requests</Heading>
        {readout.roomGaps.map((gap) => (
          <View key={gap.text} style={styles.group}>
            <Body>{gap.text}</Body>
            <Note>{gap.why}</Note>
          </View>
        ))}
        <Action
          title="Draft the data-room request"
          primary
          onPress={() => setRequestOpen(true)}
        />
      </Card>
      {evidence ? (
        <EvidenceSheet
          key={evidence.id}
          evidence={evidence}
          company={readout.company}
          snapshotAt={readout.snapshotAt}
          onClose={() => setEvidence(null)}
        />
      ) : null}
      <SavedRequest
        readout={readout}
        visible={requestOpen}
        onClose={() => setRequestOpen(false)}
      />
    </AnnotationScope>
  );
};

const ReadoutFetch = ({
  url,
  onRetry,
}: {
  url: string;
  onRetry: () => void;
}) => {
  const [readout, setReadout] = useState<CompanyReadout | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    const abort = new AbortController();
    const load = async () => {
      try {
        const result = await getCompanyReadout(url, abort.signal);
        if (!abort.signal.aborted) {
          setReadout(result);
        }
      } catch (error_) {
        if (!abort.signal.aborted) {
          setError(
            error_ instanceof Error
              ? error_.message
              : "The saved readout is unavailable."
          );
        }
      }
    };
    void load();
    return () => abort.abort();
  }, [url]);
  if (error) {
    return (
      <Card>
        <Heading>Saved readout unavailable</Heading>
        <Body accessibilityRole="alert">{error}</Body>
        <Action title="Retry readout" onPress={onRetry} />
      </Card>
    );
  }
  return readout ? (
    <WorkingPage readout={readout} />
  ) : (
    <Skeleton title="Company readout" />
  );
};

const CompanyJourney = ({ parameter }: { parameter: string }) => {
  const colors = useReadoutColors();
  const [attempt, setAttempt] = useState(0);
  if (!parameter) {
    return (
      <CompanyCarousel onSelect={(url) => router.setParams({ company: url })} />
    );
  }
  return (
    <ScrollView
      keyboardShouldPersistTaps="handled"
      contentContainerStyle={styles.content}
      style={{ backgroundColor: colors.bg }}
    >
      {Platform.OS === "web" ? null : <Heading>Tricorder</Heading>}
      <Action
        title="← Companies"
        onPress={() => router.setParams({ company: "" })}
      />
      <ReadoutFetch
        key={`${parameter}:${attempt}`}
        url={parameter}
        onRetry={() => setAttempt((value) => value + 1)}
      />
    </ScrollView>
  );
};

const SavedReadoutScreen = () => {
  const colors = useReadoutColors();
  const { company } = useLocalSearchParams<{ company?: string | string[] }>();
  const parameter = (Array.isArray(company) ? company[0] : company) ?? "";
  return (
    <SafeAreaView style={[styles.screen, { backgroundColor: colors.bg }]}>
      <View style={{ paddingHorizontal: 20 }}>
        <AnnotationToolbar />
      </View>
      <CompanyJourney key={parameter} parameter={parameter} />
    </SafeAreaView>
  );
};
export default SavedReadoutScreen;
