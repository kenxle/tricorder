import { Button, Host, Picker } from "@expo/ui";
import { useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Text,
  TextInput,
  View,
} from "react-native";

import { useReadoutColors } from "../readout/colors";
import { NativeSheet } from "../readout/native-sheet";
import type { Annotation, AnnotationTarget } from "./model";
import { personas } from "./model";
import { useAnnotations } from "./store";

export const AnnotationButton = ({
  title,
  onPress,
  disabled = false,
}: {
  title: string;
  onPress: () => void;
  disabled?: boolean;
}) => {
  const colors = useReadoutColors();
  return (
    <Host
      matchContents={{ vertical: true }}
      seedColor={colors.accent}
      style={{ minHeight: 44, width: "100%" }}
    >
      <Button
        label={title}
        testID={title}
        onPress={onPress}
        disabled={disabled}
        variant="outlined"
        style={{ paddingHorizontal: 4, paddingVertical: 8, width: "100%" }}
      />
    </Host>
  );
};

export const AnnotationComposer = ({
  target,
  start,
  end,
  onClose,
}: {
  target: AnnotationTarget;
  start: number;
  end: number;
  onClose: () => void;
}) => {
  const colors = useReadoutColors();
  const [comment, setComment] = useState("");
  const [failed, setFailed] = useState(false);
  const personaId = useAnnotations((state) => state.personaId);
  const addAnnotation = useAnnotations((state) => state.addAnnotation);
  const storageError = useAnnotations((state) => state.storageError);
  const person =
    personas.find((entry) => entry.id === personaId) ?? personas[0];
  const save = () => {
    if (addAnnotation({ comment, end, start, target })) {
      onClose();
    } else {
      setFailed(true);
    }
  };
  return (
    <NativeSheet visible onClose={onClose}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <ScrollView
          keyboardShouldPersistTaps="handled"
          contentContainerStyle={{ gap: 18, padding: 24 }}
        >
          <Text
            accessibilityRole="header"
            style={{
              color: colors.fg,
              fontFamily: "ArchivoBold",
              fontSize: 24,
            }}
          >
            Add annotation
          </Text>
          <Text style={{ color: colors.muted }}>
            {target.scopeLabel} · {person.name}
          </Text>
          <Text
            selectable
            style={{
              backgroundColor: colors.surface,
              color: colors.fg,
              fontSize: 18,
            }}
          >
            “{target.text.slice(start, end)}”
          </Text>
          <TextInput
            accessibilityLabel="Annotation comment"
            testID="Annotation comment"
            multiline
            autoFocus
            maxLength={4000}
            value={comment}
            onChangeText={setComment}
            placeholder="What should the team know?"
            placeholderTextColor={colors.muted}
            style={{
              borderColor: colors.line,
              borderRadius: 8,
              borderWidth: 1,
              color: colors.fg,
              fontSize: 17,
              minHeight: 130,
              padding: 12,
              textAlignVertical: "top",
            }}
          />
          {failed && (
            <Text accessibilityRole="alert" style={{ color: colors.red }}>
              {storageError ??
                "Could not save this annotation. Select a passage and use an associate persona."}
            </Text>
          )}
          <AnnotationButton
            title="Save annotation"
            disabled={!comment.trim() || person.role === "gp"}
            onPress={save}
          />
          <AnnotationButton title="Cancel annotation" onPress={onClose} />
          <Text style={{ color: colors.muted }}>
            Saved on this iPhone. Visible to all demo personas.
          </Text>
        </ScrollView>
      </KeyboardAvoidingView>
    </NativeSheet>
  );
};

const AnnotationCard = ({ annotation }: { annotation: Annotation }) => {
  const colors = useReadoutColors();
  const [expanded, setExpanded] = useState(false);
  const author = personas.find((person) => person.id === annotation.authorId);
  return (
    <View
      style={{
        borderColor: colors.line,
        borderRadius: 10,
        borderWidth: 1,
        gap: 10,
        padding: 16,
      }}
    >
      <Text style={{ color: colors.fg, fontFamily: "ArchivoBold" }}>
        {author?.name ?? "Associate"} · Associate
      </Text>
      <Text style={{ color: colors.muted }}>
        {annotation.target.scopeLabel}
      </Text>
      <Text style={{ color: colors.muted }}>
        {new Date(annotation.createdAt).toLocaleString()}
      </Text>
      <Text
        selectable
        style={{
          backgroundColor: colors.surface,
          color: colors.fg,
          fontSize: 17,
        }}
      >
        “{annotation.quote}”
      </Text>
      <Text selectable style={{ color: colors.fg, fontSize: 18 }}>
        {annotation.comment}
      </Text>
      <AnnotationButton
        title={expanded ? "Hide original passage" : "Show original passage"}
        onPress={() => setExpanded(!expanded)}
      />
      {expanded && (
        <>
          <Text style={{ color: colors.muted }}>Passage when annotated</Text>
          <Text selectable style={{ color: colors.fg, fontSize: 16 }}>
            {annotation.target.text.slice(0, annotation.start)}
            <Text style={{ backgroundColor: "#f1dda0", color: "#302714" }}>
              {annotation.quote}
            </Text>
            {annotation.target.text.slice(annotation.end)}
          </Text>
        </>
      )}
    </View>
  );
};

export const AnnotationReview = ({
  annotations,
  onClose,
}: {
  annotations: Annotation[];
  onClose: () => void;
}) => {
  const colors = useReadoutColors();
  return (
    <NativeSheet visible onClose={onClose}>
      <ScrollView contentContainerStyle={{ gap: 16, padding: 24 }}>
        <Text
          accessibilityRole="header"
          style={{ color: colors.fg, fontFamily: "ArchivoBold", fontSize: 24 }}
        >
          Team annotations
        </Text>
        <Text style={{ color: colors.muted }}>
          Shared diligence · {annotations.length} annotations · on this device
        </Text>
        <AnnotationButton title="Close annotations" onPress={onClose} />
        {annotations.length === 0 && (
          <Text style={{ color: colors.fg }}>
            No annotations yet. Switch to an associate, select diligence text,
            and add a note.
          </Text>
        )}
        {annotations
          .map((_, index) => annotations[annotations.length - index - 1])
          .map((annotation) => (
            <AnnotationCard key={annotation.id} annotation={annotation} />
          ))}
      </ScrollView>
    </NativeSheet>
  );
};

export const AnnotationToolbar = () => {
  const colors = useReadoutColors();
  const personaId = useAnnotations((state) => state.personaId);
  const setPersona = useAnnotations((state) => state.setPersona);
  const selectingText = useAnnotations((state) => state.selectingText);
  const setSelectingText = useAnnotations((state) => state.setSelectingText);
  const annotations = useAnnotations((state) => state.annotations);
  const storageError = useAnnotations((state) => state.storageError);
  const [reviewing, setReviewing] = useState(false);
  const person =
    personas.find((entry) => entry.id === personaId) ?? personas[0];
  return (
    <View style={{ gap: 10, paddingVertical: 12 }}>
      <Text
        style={{ color: colors.muted, fontFamily: "PlexMono", fontSize: 12 }}
      >
        DEMO PERSONA
      </Text>
      <Host
        matchContents={{ vertical: true }}
        seedColor={colors.accent}
        style={{ minHeight: 44, width: "100%" }}
      >
        <Picker
          selectedValue={personaId}
          onValueChange={setPersona}
          testID="Demo persona"
        >
          {personas.map((entry) => (
            <Picker.Item
              key={entry.id}
              value={entry.id}
              label={`${entry.name} · ${entry.role === "gp" ? "GP" : "Associate"}`}
            />
          ))}
        </Picker>
      </Host>
      <Text style={{ color: colors.muted }}>
        {person.role === "gp"
          ? "Review the team's notes and the passages behind them."
          : "Choose Select text to annotate, then long-press a word and adjust the selection handles."}
      </Text>
      {person.role === "associate" && Platform.OS === "ios" && (
        <>
          <AnnotationButton
            title={
              selectingText ? "Done selecting text" : "Select text to annotate"
            }
            onPress={() => setSelectingText(!selectingText)}
          />
          {selectingText && (
            <Text accessibilityRole="alert" style={{ color: colors.muted }}>
              Selection is on. Long-press a word, drag the handles, then tap
              Annotate selection. Finish selecting to use evidence links.
            </Text>
          )}
        </>
      )}
      <AnnotationButton
        title={`Team annotations (${annotations.length})`}
        onPress={() => setReviewing(true)}
      />
      {storageError && (
        <Text accessibilityRole="alert" style={{ color: colors.red }}>
          {storageError}
        </Text>
      )}
      {reviewing && (
        <AnnotationReview
          annotations={annotations}
          onClose={() => setReviewing(false)}
        />
      )}
    </View>
  );
};
