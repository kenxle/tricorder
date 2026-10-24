import { useRef, useState, useEffect } from "react";
import type { ComponentRef } from "react";
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const screens = [
  "Start",
  "Research",
  "First readout",
  "Request evidence",
  "Room received",
  "Updated readout",
  "Finding & source",
  "Steer & revisions",
  "Prepare memo",
  "Reader memo",
] as const;
const initialRequests = [
  "Revenue by customer",
  "Retention cohorts",
  "Signed customer contracts",
];
const receivedItems = new Set([initialRequests[0], initialRequests[2]]);
const evidence = [
  {
    finding: "Voice software for support teams",
    passage: "Hollis builds voice software for customer support teams.",
    title: "Company website · synthetic fixture",
  },
  {
    finding: "Customer commitments need a closer look",
    passage:
      "The sample agreements include a termination-for-convenience clause.",
    title: "Customer contracts · synthetic fixture",
  },
];

export default function FlowScreen() {
  const [step, setStep] = useState(0);
  const [url, setUrl] = useState("https://hollis.example");
  const [requests, setRequests] = useState(initialRequests);
  const [selected, setSelected] = useState(initialRequests);
  const [extra, setExtra] = useState("");
  const [note, setNote] = useState(
    "Could you share the items below so we can understand the business better?"
  );
  const [received, setReceived] = useState(false);
  const [source, setSource] = useState<number | null>(null);
  const [steer, setSteer] = useState(
    "Keep the contract uncertainty prominent."
  );
  const [revisions, setRevisions] = useState<string[]>([]);
  const [judgment, setJudgment] = useState(
    "Discuss renewal risk with the founders before making a recommendation."
  );
  const [map, setMap] = useState(false);
  const scroll = useRef<ComponentRef<typeof ScrollView>>(null);
  useEffect(() => {
    scroll.current?.scrollTo({ animated: false, y: 0 });
  }, [step]);
  const outstanding = selected.filter(
    (item) => !received || !receivedItems.has(item)
  );
  function go(next: number) {
    if (next >= 4) {
      setReceived(true);
    }
    setStep(next);
    setSource(null);
    setMap(false);
  }
  function toggle(item: string) {
    setSelected((items) =>
      items.includes(item) ? items.filter((x) => x !== item) : [...items, item]
    );
  }
  function addRequest() {
    const item = extra.trim();
    if (item && !requests.includes(item)) {
      setRequests([...requests, item]);
      setSelected([...selected, item]);
    }
    setExtra("");
  }
  const button = (title: string, onPress: () => void, primary = false) => (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={({ pressed }) => [
        s.button,
        primary && s.primary,
        pressed && { opacity: 0.7 },
      ]}
    >
      <Text style={[s.buttonText, primary && { color: "#16140f" }]}>
        {title}
      </Text>
    </Pressable>
  );
  const body = (text: string) => <Text style={s.body}>{text}</Text>;
  const card = (title: string, text: string, action?: React.ReactNode) => (
    <View style={s.card}>
      <Text style={s.cardTitle}>{title}</Text>
      {body(text)}
      {action}
    </View>
  );
  const field = (
    label: string,
    value: string,
    change: (v: string) => void,
    multiline = false
  ) => (
    <View style={s.field}>
      <Text style={s.label}>{label}</Text>
      <TextInput
        accessibilityLabel={label}
        value={value}
        onChangeText={change}
        multiline={multiline}
        style={[
          s.input,
          multiline && { minHeight: 100, textAlignVertical: "top" },
        ]}
        placeholderTextColor="#9a9488"
      />
    </View>
  );
  const sourceButton = (index: number) =>
    button("Inspect source", () => setSource(index));
  return (
    <SafeAreaView style={s.screen} edges={["top", "left", "right"]}>
      <View style={s.top}>
        <Text style={s.brand}>Tricorder</Text>
        {button(map ? "Close screen index" : "Screen index", () =>
          setMap(!map)
        )}
      </View>
      <ScrollView
        ref={scroll}
        contentContainerStyle={s.content}
        keyboardShouldPersistTaps="handled"
      >
        <Text style={s.eyebrow}>UX PROTOTYPE · SYNTHETIC CONTENT</Text>
        {body(
          "A clickable sketch. Research, uploads and steering are simulated; nothing is sent or saved to the server."
        )}
        {map && (
          <View style={s.card}>
            {screens.map((name, index) => (
              <View key={name}>
                {button(`${index + 1}. ${name}`, () => go(index))}
              </View>
            ))}
          </View>
        )}
        <Text style={s.label}>
          {step + 1} / {screens.length} · {screens[step]}
        </Text>
        <Text accessibilityRole="header" style={s.title}>
          {
            [
              "Understand a company.",
              "Research taking shape.",
              "What we know. What we need.",
              "Ask for the evidence.",
              "Close the loop.",
              "What changed?",
              "Show the work.",
              "Refine the interpretation.",
              "Make the memo yours.",
              "A memo you can question.",
            ][step]
          }
        </Text>
        {step === 0 && (
          <>
            {body(
              "Start with a company URL. Get a sourced first readout and the questions worth asking next."
            )}
            {field("Company URL (demo only)", url, setUrl)}
            {button("Start demo research", () => go(1), true)}
            {body(
              "This walkthrough always uses the fictional Hollis fixture, whatever URL you enter."
            )}
          </>
        )}
        {step === 1 && (
          <>
            {card(
              "Hollis · company resolved",
              `Demo input: ${url || "No URL entered"}. Voice software for support teams.`,
              sourceButton(0)
            )}
            {card(
              "Outside world · available",
              evidence[0].finding,
              sourceButton(0)
            )}
            {card(
              "Founders · pending",
              "Founder background is still being researched in this simulated state."
            )}
            {card(
              "Market signals · unavailable",
              "No reliable traffic source available. Keep this as an explicit gap."
            )}
            {button("View first readout", () => go(2), true)}
          </>
        )}
        {step === 2 && (
          <>
            {card(
              "Hollis · company summary",
              evidence[0].finding,
              sourceButton(0)
            )}
            {card(
              "Important unknowns",
              "Revenue quality, retention and customer commitments need evidence from the founder."
            )}
            {card(
              "Public research",
              "Outside world has a source. Founder background and market signals remain incomplete."
            )}
            {button("Review evidence request", () => go(3), true)}
          </>
        )}
        {step === 3 && (
          <>
            {body(
              "Missing items begin checked. Keep, remove or add requests before reviewing your message."
            )}
            {requests.map((item) => (
              <Pressable
                key={item}
                accessibilityRole="checkbox"
                accessibilityState={{
                  checked: selected.includes(item),
                  disabled: received && receivedItems.has(item),
                }}
                disabled={received && receivedItems.has(item)}
                onPress={() => toggle(item)}
                style={s.card}
              >
                <Text style={s.cardTitle}>
                  {received && receivedItems.has(item)
                    ? "Received"
                    : selected.includes(item)
                      ? "☑"
                      : "☐"}{" "}
                  · {item}
                </Text>
                {body(
                  item === initialRequests[0]
                    ? "Understand revenue quality and customer concentration."
                    : item === initialRequests[1]
                      ? "Understand whether customers stay over time."
                      : item === initialRequests[2]
                        ? "Check commitments against contract terms."
                        : "Additional operator request."
                )}
              </Pressable>
            ))}
            {field("Add a request", extra, setExtra)}
            {button("Add item", addRequest)}
            {field("Message introduction", note, setNote, true)}
            {card(
              "Draft for your own email",
              `${note}\n\n${outstanding.map((item) => `• ${item}`).join("\n") || "No outstanding items selected."}`
            )}
            {body(
              "Tricorder never sends. In this prototype, continue to simulate a founder reply."
            )}
            {button(
              "Simulate room received",
              () => {
                setReceived(true);
                go(4);
              },
              true
            )}
          </>
        )}
        {step === 4 && (
          <>
            {card(
              "Received · revenue and signed contracts",
              "Demo files received. Coverage has been rechecked."
            )}
            {card(
              "Still needed",
              outstanding.join("\n") ||
                "No selected requests remain outstanding."
            )}
            {button("Review remaining requests", () => go(3))}
            {button("Open updated readout", () => go(5), true)}
          </>
        )}
        {step === 5 && (
          <>
            {card(
              "New evidence in the room",
              "The sample revenue file is available for analysis. Retention evidence is still missing."
            )}
            {card(
              "Looking weak · customer commitments",
              evidence[1].finding,
              button("Open finding", () => go(6))
            )}
            {card(
              "Not enough in the room · retention",
              "No cohort evidence has arrived. No retention conclusion is supported."
            )}
            {button("Request more evidence", () => go(3))}
            {button("Prepare memo", () => go(8), true)}
          </>
        )}
        {step === 6 && (
          <>
            {card(
              "Company statement",
              "Customer commitments are durable. This is a synthetic statement for the walkthrough."
            )}
            {card(
              "Evidence · contract qualification",
              evidence[1].passage,
              sourceButton(1)
            )}
            {card(
              "Interpretation · looking weak",
              "The statement needs qualification. Contract terms alone do not establish realized retention."
            )}
            {button("Steer this finding", () => go(7), true)}
          </>
        )}
        {step === 7 && (
          <>
            {field("Your instruction", steer, setSteer, true)}
            {button(
              "Apply demo steer",
              () => {
                if (steer.trim()) {
                  setRevisions([...revisions, steer.trim()]);
                }
              },
              true
            )}
            {card(
              "Original finding · retained",
              "Customer commitments need a closer look. Source passages and computed figures stay unchanged."
            )}
            {revisions.map((revision, i) => (
              <View key={i}>
                {card(`Revision ${i + 1} · operator instruction`, revision)}
              </View>
            ))}
            {body(
              "Demo behavior: applying a steer records your instruction as a revision. It does not run an analysis model."
            )}
            {button("Return to readout", () => go(5))}
            {button("Prepare memo", () => go(8), true)}
          </>
        )}
        {step === 8 && (
          <>
            {card("Sourced summary", evidence[0].finding, sourceButton(0))}
            {card(
              "Risk to carry forward",
              evidence[1].finding,
              sourceButton(1)
            )}
            {field("Operator-authored judgment", judgment, setJudgment, true)}
            {card(
              "Open questions",
              "Retention remains unsupported. Keep missing evidence visible in the memo."
            )}
            {button("Preview reader memo", () => go(9), true)}
          </>
        )}
        {step === 9 && (
          <>
            {card(
              "Hollis · diligence memo",
              evidence[0].finding,
              sourceButton(0)
            )}
            {card(
              "Customer commitments",
              evidence[1].finding,
              button("Memo line → claim → source", () => go(6))
            )}
            {card(
              "Operator-authored judgment",
              judgment || "No operator judgment added."
            )}
            {card("Evidence gaps", "Retention cohorts remain missing.")}
            {card(
              "Planned · reader copies and scenarios",
              "A future personal workspace for what-if questions. Not interactive in this prototype."
            )}
            {button("Edit memo", () => go(8))}
            {button("Back to beginning", () => go(0))}
          </>
        )}
        {source !== null && (
          <View accessibilityRole="summary" style={s.source}>
            <Text style={s.eyebrow}>SOURCE INSPECTOR</Text>
            <Text style={s.cardTitle}>{evidence[source].title}</Text>
            {body(evidence[source].passage)}
            {body(
              "Synthetic excerpt authored for this UX sketch; not a verified company claim."
            )}
            {button("Close source", () => setSource(null))}
          </View>
        )}
        <View style={s.footer}>
          {step > 0 && button("Previous screen", () => go(step - 1))}
          {step < screens.length - 1 &&
            button("Next screen", () => go(step + 1))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
const s = StyleSheet.create({
  body: { color: "#bdb7ab", fontSize: 16, lineHeight: 25 },
  brand: { color: "#eeebe4", fontSize: 22, fontWeight: "800" },
  button: {
    alignSelf: "flex-start",
    borderColor: "#d3bf8e",
    borderRadius: 6,
    borderWidth: 1,
    justifyContent: "center",
    minHeight: 44,
    padding: 12,
  },
  buttonText: { color: "#d3bf8e", fontSize: 15, fontWeight: "600" },
  card: {
    backgroundColor: "#1a1916",
    borderColor: "#45413a",
    borderRadius: 8,
    borderWidth: 1,
    gap: 12,
    padding: 20,
  },
  cardTitle: { color: "#eeebe4", fontSize: 20, fontWeight: "600" },
  content: {
    alignSelf: "center",
    gap: 16,
    maxWidth: 820,
    padding: 24,
    paddingBottom: 100,
    width: "100%",
  },
  eyebrow: { color: "#d3bf8e", fontSize: 12, letterSpacing: 1.5 },
  field: { gap: 8 },
  footer: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginTop: 16 },
  input: {
    backgroundColor: "#1a1916",
    borderColor: "#9a9488",
    borderRadius: 6,
    borderWidth: 1,
    color: "#eeebe4",
    fontSize: 16,
    minHeight: 48,
    padding: 12,
  },
  label: { color: "#bdb7ab", fontSize: 14 },
  primary: { backgroundColor: "#d3bf8e" },
  screen: { backgroundColor: "#131210", flex: 1 },
  source: {
    borderColor: "#d3bf8e",
    borderRadius: 8,
    borderWidth: 1,
    gap: 12,
    padding: 20,
  },
  title: {
    color: "#eeebe4",
    fontSize: 36,
    fontWeight: "800",
    letterSpacing: -1,
  },
  top: {
    alignItems: "center",
    borderBottomColor: "#45413a",
    borderBottomWidth: 1,
    flexDirection: "row",
    justifyContent: "space-between",
    padding: 16,
  },
});
