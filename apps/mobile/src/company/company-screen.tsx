import { router, useLocalSearchParams } from "expo-router";
import type { PropsWithChildren } from "react";
import { useCallback, useMemo, useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { NativeSheet } from "../readout/native-sheet";
import {
  Action,
  Body,
  Card,
  Heading,
  Note,
  Row,
  useReadoutColors,
} from "../readout/ui";
import { RequestForm } from "../request-ui/request-form";
import { useRequestSession } from "../request-ui/session";
import { CompanyCarousel } from "./company-carousel";
import { stages, useCompanyState } from "./company-state";
import { data } from "./data";
import { EvidenceContent } from "./evidence-content";
import { requestItems, resolveCompany } from "./model";
import type {
  Company,
  RequestItem,
  ResearchClaim,
  ResearchSection,
  Stage,
} from "./model";

const styles = StyleSheet.create({
  brand: { fontFamily: "ArchivoDisplay", fontSize: 22, letterSpacing: -0.7 },
  claim: { gap: 4, paddingVertical: 4 },
  content: {
    alignSelf: "center",
    gap: 24,
    maxWidth: 1264,
    padding: 16,
    paddingBottom: 48,
    width: "100%",
  },
  emphasis: { fontWeight: "600" },
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
    fontSize: 24,
    fontWeight: "700",
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
    flexDirection: "row",
    gap: 16,
    justifyContent: "space-between",
    padding: 16,
  },
  snapshot: { borderBottomWidth: 1, borderTopWidth: 1, paddingVertical: 16 },
  title: {
    fontSize: 34,
    fontWeight: "700",
    letterSpacing: -0.7,
    lineHeight: 41,
  },
});

const Sheet = ({
  title,
  onClose,
  children,
}: PropsWithChildren<{
  title: string;
  onClose: () => void;
}>) => (
  <NativeSheet visible onClose={onClose}>
    <View style={styles.sheetHeader}>
      <Heading>{title}</Heading>
      <Action compact title="Done" onPress={onClose} />
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
  </NativeSheet>
);
const SourceEvidence = ({
  claim,
  onClose,
}: {
  claim: ResearchClaim;
  onClose: () => void;
}) => (
  <Sheet title="Evidence" onClose={onClose}>
    <EvidenceContent claim={claim} />
  </Sheet>
);
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
      <Body
        accessibilityRole={source ? "link" : undefined}
        accessibilityLabel={
          source
            ? `${claim.text}. Evidence ${number}: ${source.title}`
            : undefined
        }
        onPress={source ? () => onSource(claim) : undefined}
        style={[
          { minHeight: source ? 44 : undefined },
          claim.placeholder ? { color: colors.muted } : undefined,
        ]}
      >
        {claim.text}
        {/* Universal Text accepts only a string; RN Text preserves selectable prose and inline links. */}
        {source && (
          <Text
            style={{ color: colors.accent, textDecorationLine: "underline" }}
          >
            {` [${number}]`}
          </Text>
        )}
      </Body>
      {claim.placeholder ? <Note>Not researched yet</Note> : null}
      {!claim.placeholder && claim.kind ? <Note>{claim.kind}</Note> : null}
      {!source && !claim.placeholder && (
        <Note>Source unavailable in this snapshot</Note>
      )}
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
const CompanyWorkspace = ({ company }: { company: Company }) => {
  const colors = useReadoutColors();
  const research = data.research[company.slug];
  const { fields, stage } = useCompanyState(company);
  const [request, setRequest] = useState(false);
  const [evidence, setEvidence] = useState<ResearchClaim | null>(null);
  const bundledItems = useMemo(
    () => requestItems(data.checklist, stage, research),
    [stage, research]
  );
  const [layoutItems, setLayoutItems] = useState<{
    stage: Stage;
    items: RequestItem[];
  } | null>(null);
  const receiveItems = useCallback(
    (items: RequestItem[]) => setLayoutItems({ items, stage }),
    [stage]
  );
  const session = useRequestSession(
    company.slug,
    fields.name.value,
    fields.founders.value,
    stage,
    layoutItems?.stage === stage ? layoutItems.items : bundledItems
  );
  const selected = session.items.filter((item) => item.checked).length;
  return (
    <>
      <ScrollView
        keyboardShouldPersistTaps="handled"
        contentContainerStyle={styles.content}
      >
        <Row>
          <Action
            title="← Companies"
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
            <Action
              title="Company details"
              onPress={() =>
                router.push({
                  params: { company: company.website },
                  pathname: "/company-sheet",
                })
              }
            />
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
      {request && (
        <Sheet title="Data-room request" onClose={() => setRequest(false)}>
          <Note>
            {fields.name.value} ·{" "}
            {stages.find((entry) => entry.id === stage)?.title} · {selected}{" "}
            selected
          </Note>
          <RequestForm
            company={company.slug}
            stage={stage}
            items={bundledItems}
            session={session}
            onItems={receiveItems}
          />
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
  return (
    <SafeAreaView style={[styles.screen, { backgroundColor: colors.bg }]}>
      {company && Platform.OS !== "web" && (
        <View style={[styles.masthead, { borderColor: colors.line }]}>
          <Body style={styles.brand}>Tricorder</Body>
          <Note style={styles.mono}>EVERY CLAIM SOURCED</Note>
        </View>
      )}
      {company ? (
        <CompanyWorkspace key={company.slug} company={company} />
      ) : (
        <CompanyCarousel
          onSelect={(url) => router.setParams({ company: url })}
        />
      )}
    </SafeAreaView>
  );
};

export default CompanyScreen;
