import { Host, Picker } from "@expo/ui";
import type { CompanyReadout, CompanyStage } from "@tricorder/schema/company";
import { useCallback, useState } from "react";
import { KeyboardAvoidingView, Platform, ScrollView, View } from "react-native";

import { NativeSheet } from "../readout/native-sheet";
import { Action, Heading, Note, useReadoutColors } from "../readout/ui";
import { RequestForm } from "../request-ui/request-form";
import { savedRequestStage, useRequestSession } from "../request-ui/session";
import type { RequestItem } from "./model";

export const SavedRequest = ({
  readout,
  visible,
  onClose,
}: {
  readout: CompanyReadout;
  visible: boolean;
  onClose: () => void;
}) => {
  const colors = useReadoutColors();
  const [stage, setStage] = useState<CompanyStage>(
    () =>
      savedRequestStage(readout.company.slug) ?? readout.request.defaultStage
  );
  const [layout, setLayout] = useState<{
    stage: CompanyStage;
    items: RequestItem[];
  } | null>(null);
  const baseItems = readout.request.itemsByStage[stage];
  const receiveItems = useCallback(
    (items: RequestItem[]) => setLayout({ items, stage }),
    [stage]
  );
  const session = useRequestSession(
    readout.company.slug,
    readout.company.name,
    readout.request.founder,
    stage,
    layout?.stage === stage ? layout.items : baseItems
  );
  return (
    <NativeSheet visible={visible} onClose={onClose}>
      <View style={{ gap: 12, padding: 16 }}>
        <Heading>Data-room request</Heading>
        <Action compact title="Done" onPress={onClose} />
      </View>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        enabled={Platform.OS !== "web"}
        behavior={Platform.OS === "ios" ? "padding" : "height"}
      >
        <ScrollView
          keyboardShouldPersistTaps="handled"
          contentContainerStyle={{ gap: 16, padding: 24 }}
        >
          <Note>{readout.company.name}</Note>
          <Host matchContents={{ vertical: true }} seedColor={colors.accent}>
            <Picker
              selectedValue={stage}
              onValueChange={setStage}
              testID="Request stage"
            >
              <Picker.Item value="pre_seed" label="Pre-seed" />
              <Picker.Item value="seed" label="Seed" />
              <Picker.Item value="series_a" label="Series A" />
            </Picker>
          </Host>
          {visible ? (
            <RequestForm
              company={readout.company.slug}
              stage={stage}
              items={baseItems}
              session={session}
              onItems={receiveItems}
            />
          ) : null}
        </ScrollView>
      </KeyboardAvoidingView>
    </NativeSheet>
  );
};
