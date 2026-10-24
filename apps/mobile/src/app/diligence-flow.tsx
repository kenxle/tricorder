// The native diligence flow: start from a URL, the working page, the data-room request,
// then the room as it arrives (the room view comes from ../diligence/room-view).
// ?company=<url> opens a company directly.
import { useLocalSearchParams, useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { ScrollView, View } from "react-native";

import { Body, Note, useReadoutColors } from "../readout/ui";
import { researchFor } from "../diligence/diligence-data";
import { RequestDialog, RequestsBox, RoomNotice, UpNextBox, buildItems } from "../diligence/requests";
import type { RequestItem, RoomState } from "../diligence/requests";
import { RoomView } from "../diligence/room-view";
import { StartScreen } from "../diligence/start";
import { WorkingPage } from "../diligence/working";

const ARRIVAL_MS = 1800;

export default function DiligenceFlow() {
  const colors = useReadoutColors();
  const router = useRouter();
  const params = useLocalSearchParams<{ company?: string }>();
  const [url, setUrl] = useState(params.company ?? "");
  const research = researchFor(url);
  const [items, setItems] = useState<RequestItem[]>([]);
  const [dialog, setDialog] = useState(false);
  const [sent, setSent] = useState(false);
  const [room, setRoom] = useState<RoomState>("none");

  useEffect(() => {
    if (research) setItems(buildItems(research));
    setSent(false);
    setRoom("none");
  }, [research]);

  // The room arrives as a notification after the request goes out; the rest of the files follow.
  useEffect(() => {
    if (!sent || room !== "none") return;
    const t = setTimeout(() => setRoom("shared"), ARRIVAL_MS);
    return () => clearTimeout(t);
  }, [sent, room]);
  useEffect(() => {
    if (room !== "partial") return;
    const t = setTimeout(() => setRoom("more"), ARRIVAL_MS);
    return () => clearTimeout(t);
  }, [room]);

  const start = (u: string) => {
    setUrl(u);
    router.setParams({ company: u });
  };

  let body;
  if (!url) {
    body = <StartScreen onStart={start} />;
  } else if (!research) {
    body = (
      <View style={{ gap: 12, paddingVertical: 32 }}>
        <Body style={{ fontFamily: "ArchivoBold" }}>Research not cached for this company.</Body>
        <Note>Tricorder has saved research for Sazabi only.</Note>
        <StartScreen onStart={start} />
      </View>
    );
  } else if (room === "partial" || room === "more" || room === "full") {
    const k = research.room.filesTotal - research.room.partial.arrived.length;
    body = (
      <View style={{ gap: 12 }}>
        {room === "more" ? (
          <RoomNotice title={`${research.name} added ${k} more file${k === 1 ? "" : "s"}`} onOpen={() => setRoom("full")} />
        ) : null}
        <RequestsBox research={research} items={items} room={room} />
        <RoomView
          state={room === "full" ? "full" : "partial"}
          onMemo={() => router.push("/diligence-memo" as never)}
          onSteer={() => router.push("/diligence-memo?steer=1" as never)}
        />
      </View>
    );
  } else {
    const n = research.room.partial.arrived.length;
    body = (
      <WorkingPage
        research={research}
        notice={room === "shared" ? (
          <RoomNotice title={`${research.name} shared its data room · ${n} file${n === 1 ? "" : "s"}`} onOpen={() => setRoom("partial")} />
        ) : null}
        roomBox={sent ? <RequestsBox research={research} items={items} room={room} /> : <UpNextBox research={research} onDraft={() => setDialog(true)} />}
      />
    );
  }

  return (
    <ScrollView style={{ backgroundColor: colors.bg }} contentContainerStyle={{ alignSelf: "center", maxWidth: 1000, padding: 16, paddingBottom: 64, width: "100%" }}>
      <View style={{ alignItems: "center", flexDirection: "row", gap: 12, marginBottom: 8 }}>
        <Body onPress={() => start("")} style={{ fontFamily: "ArchivoBold", fontSize: 18, letterSpacing: 1, textTransform: "uppercase" }}>
          Tricorder
        </Body>
        {url ? <Note numberOfLines={1} style={{ flex: 1 }}>{url}</Note> : null}
      </View>
      {body}
      {research ? (
        <RequestDialog
          research={research}
          visible={dialog}
          items={items}
          setItems={setItems}
          onClose={() => setDialog(false)}
          onSent={() => {
            const now = new Date();
            setItems(items.map((i) => (i.checked ? { ...i, askedAt: now } : i)));
            setSent(true);
            setDialog(false);
          }}
        />
      ) : null}
    </ScrollView>
  );
}
