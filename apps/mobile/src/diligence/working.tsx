// The associate's working page: the company, what it does, What stands out, then the
// evidence sections in order (founders, comps, market signals, outside world). Each section
// shows a skeleton until its data arrives, then fills in whole.
import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { Linking, View } from "react-native";

import { Body, Card, Heading, Note, Row, useReadoutColors } from "../readout/ui";
import { EvRef, MARKS, Mark, MemoToggle, SourceButton, Skeleton, markTone } from "./diligence-bits";
import type { Claim, Research, Section } from "./diligence-data";
import { claimByNum, refNums } from "./diligence-data";

const PACE_MS = 650;

/** How many blocks have arrived: sections first, then insights, then the room box. */
export function useArrival(total: number, key: string) {
  const [arrived, setArrived] = useState(0);
  useEffect(() => {
    setArrived(0);
    const timers = Array.from({ length: total }, (_, i) =>
      setTimeout(() => setArrived(i + 1), 500 + i * PACE_MS),
    );
    return () => timers.forEach(clearTimeout);
  }, [total, key]);
  return arrived;
}

function EvidenceTable({ research, claims }: { research: Research; claims: Claim[] }) {
  const c = useReadoutColors();
  return (
    <View style={{ borderColor: c.line, borderTopWidth: 1 }}>
      <Row>
        <Note style={{ flex: 1, fontFamily: "PlexMono", fontSize: 11, textTransform: "uppercase" }}>What we found</Note>
        <Note style={{ fontFamily: "PlexMono", fontSize: 11, textTransform: "uppercase", width: 150 }}>Source</Note>
      </Row>
      {claims.map((cl, i) => (
        <View
          key={i}
          nativeID={cl.n ? `ev-${cl.n}` : undefined}
          style={{ borderColor: c.line, borderTopWidth: 1, flexDirection: "row", gap: 12, paddingVertical: 8 }}
        >
          <View style={{ flex: 1, flexDirection: "row", gap: 8 }}>
            {cl.n ? <Body style={{ color: c.accent, fontFamily: "PlexMono", fontSize: 13 }}>{cl.n}</Body> : null}
            <Body style={{ flex: 1, fontSize: 15, lineHeight: 22 }}>
              {cl.text}
              {cl.kind ? <Note style={{ fontSize: 12 }}>{`  ${cl.kind}`}</Note> : null}
            </Body>
          </View>
          <View style={{ gap: 4, width: 150 }}>
            {cl.placeholder ? (
              <Mark label="Placeholder" />
            ) : (
              <>
                <SourceButton research={research} sourceId={cl.source} url={cl.url} />
                {cl.n ? <MemoToggle company={research.slug} pickKey={`claim:${cl.n}`} /> : null}
              </>
            )}
          </View>
        </View>
      ))}
    </View>
  );
}

function SectionBody({ research, section }: { research: Research; section: Section }) {
  if (section.parts) {
    return (
      <View style={{ gap: 12 }}>
        {section.parts.map((p) => (
          <View key={p.label} style={{ gap: 6 }}>
            <Body style={{ fontFamily: "ArchivoBold" }}>{p.label}</Body>
            {p.claims.length ? <EvidenceTable research={research} claims={p.claims} /> : <Note>Nothing found.</Note>}
          </View>
        ))}
      </View>
    );
  }
  if (section.cards) {
    return (
      <View style={{ gap: 12 }}>
        {section.cards.map((card) => (
          <View key={card.name} style={{ gap: 6 }}>
            <Body style={{ fontFamily: "ArchivoBold", fontSize: 18 }}>{card.name}</Body>
            <Note>{card.role}</Note>
            <Row>
              {card.x ? <Note onPress={() => Linking.openURL(card.x!)} style={{ textDecorationLine: "underline" }}>X: linked, not read</Note> : null}
              {card.github ? <Note onPress={() => Linking.openURL(card.github!)} style={{ textDecorationLine: "underline" }}>GitHub</Note> : null}
            </Row>
            <EvidenceTable research={research} claims={card.claims} />
          </View>
        ))}
      </View>
    );
  }
  return <EvidenceTable research={research} claims={section.claims ?? []} />;
}

function Block({ title, ready, children }: { title: string; ready: boolean; children: ReactNode }) {
  return (
    <View accessibilityLabel={title} style={{ gap: 8, marginTop: 24 }}>
      <Heading>{title}</Heading>
      {ready ? children : <Skeleton />}
    </View>
  );
}

export function WorkingPage({
  research,
  notice,
  roomBox,
}: {
  research: Research;
  notice?: ReactNode;
  roomBox: ReactNode;
}) {
  const c = useReadoutColors();
  const total = research.sections.length + 2;
  const arrived = useArrival(total, research.slug);
  const [focus, setFocus] = useState<number | null>(null);
  const focused = focus ? claimByNum(research, focus) : undefined;
  const sectionsReady = (i: number) => arrived > i;
  const insightsReady = arrived > research.sections.length;
  const roomReady = arrived > research.sections.length + 1;
  const aboutNums = refNums(research, research.about.refs);

  return (
    <View style={{ gap: 4 }}>
      {notice}
      <Heading style={{ fontSize: 34, lineHeight: 40 }}>{research.name}</Heading>
      <Body>{research.about.text}</Body>
      <Row>
        {aboutNums.map((n) => <EvRef key={n} n={n} onPress={setFocus} />)}
      </Row>
      {focused ? (
        <Card>
          <Row>
            <Body style={{ color: c.accent, fontFamily: "PlexMono" }}>{focused.n}</Body>
            <Body style={{ flex: 1 }}>{focused.text}</Body>
          </Row>
          <Row>
            <SourceButton research={research} sourceId={focused.source} url={focused.url} />
            <Note onPress={() => setFocus(null)} style={{ textDecorationLine: "underline" }}>Close</Note>
          </Row>
        </Card>
      ) : null}
      {!roomReady ? <Note accessibilityRole="text">Researching</Note> : null}

      <Block title="What stands out" ready={insightsReady}>
        <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 12 }}>
          {research.insights.map((ins, idx) => (
            <View key={idx} style={{ flexBasis: 300, flexGrow: 1 }}>
              <Card>
                <Row>
                  <Mark label={MARKS[ins.mark] ?? MARKS.thin} tone={markTone(ins.mark)} />
                  <Note style={{ fontSize: 13 }}>{ins.piece}</Note>
                </Row>
                <Body style={{ fontFamily: "ArchivoBold", fontSize: 18, lineHeight: 24 }}>{ins.title}</Body>
                <Body style={{ fontSize: 15, lineHeight: 22 }}>{ins.text}</Body>
                <Row>
                  <Note style={{ fontSize: 13 }}>Based on</Note>
                  {refNums(research, ins.refs).map((n) => <EvRef key={n} n={n} onPress={setFocus} />)}
                  <View style={{ flexGrow: 1 }} />
                  <MemoToggle company={research.slug} pickKey={`insight:${idx}`} />
                </Row>
              </Card>
            </View>
          ))}
        </View>
      </Block>

      {research.sections.map((s, i) => (
        <Block key={s.key} title={s.title} ready={sectionsReady(i)}>
          <SectionBody research={research} section={s} />
          {(s.gaps ?? []).map((g) => (
            <Body key={g.text} style={{ fontSize: 14 }}>
              <Body style={{ fontFamily: "ArchivoBold", fontSize: 14 }}>Gap: </Body>
              {g.text} <Note style={{ fontSize: 13 }}>{g.why}</Note>
            </Body>
          ))}
        </Block>
      ))}

      <View style={{ marginTop: 24 }}>{roomReady ? roomBox : <Skeleton />}</View>
    </View>
  );
}
