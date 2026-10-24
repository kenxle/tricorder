import { useMemo, useState } from "react";
import type { ReactNode } from "react";
import { Platform, Text, TextInput, View } from "react-native";
import type { TextProps } from "react-native";

import {
  AnnotationButton,
  AnnotationComposer,
  AnnotationReview,
} from "./annotation-panel";
import { useAnnotationScope } from "./context";
import {
  annotationsForTarget,
  highlightSegments,
  personas,
  validSelection,
} from "./model";
import type { AnnotationTarget } from "./model";
import { hasInlinePress, mapTextLeaves, plainText } from "./rich-text";
import { useAnnotations } from "./store";

const NativeSelectionText = ({
  target,
  textProps: props,
  children,
  onSelection,
}: {
  target: AnnotationTarget;
  textProps: TextProps;
  children: ReactNode;
  onSelection: (selection: { start: number; end: number }) => void;
}) => {
  const [contentHeight, setContentHeight] = useState(32);
  return (
    <>
      <Text
        accessible={false}
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
        pointerEvents="none"
        style={[
          props.style,
          { left: 0, opacity: 0, position: "absolute", right: 0, top: 0 },
        ]}
        onTextLayout={({ nativeEvent }) => {
          const last = nativeEvent.lines.at(-1);
          if (last) {
            setContentHeight(Math.ceil(last.y + last.height) + 2);
          }
        }}
      >
        {target.text}
      </Text>
      <TextInput
        testID={props.testID ?? `Diligence: ${target.text.slice(0, 60)}`}
        accessibilityLabel={props.accessibilityLabel ?? target.text}
        accessibilityHint="Select words to add a diligence annotation."
        multiline
        readOnly
        scrollEnabled={false}
        showSoftInputOnFocus={false}
        style={[props.style, { height: contentHeight, margin: 0, padding: 0 }]}
        onSelectionChange={({ nativeEvent: { selection: next } }) => {
          // iOS collapses selection when the annotation button takes focus.
          // Keep the last valid range until its comment is saved or cancelled.
          if (validSelection(target.text, next.start, next.end)) {
            onSelection(next);
          }
        }}
      >
        <Text>{children}</Text>
      </TextInput>
    </>
  );
};

const ScopedText = ({
  target,
  ...props
}: TextProps & { target: AnnotationTarget }) => {
  const all = useAnnotations((state) => state.annotations);
  const personaId = useAnnotations((state) => state.personaId);
  const selectingText = useAnnotations((state) => state.selectingText);
  const setSelectingText = useAnnotations((state) => state.setSelectingText);
  const associate =
    personas.find((person) => person.id === personaId)?.role === "associate";
  const annotations = useMemo(
    () => annotationsForTarget(all, target),
    [all, target]
  );
  const [selection, setSelection] = useState({ end: 0, start: 0 });
  const [composing, setComposing] = useState<{
    start: number;
    end: number;
  } | null>(null);
  const [reviewing, setReviewing] = useState(false);
  const segments = highlightSegments(target.text, annotations);
  const spans = segments.map((segment) => (
    <Text
      key={segment.start}
      style={
        segment.highlighted
          ? { backgroundColor: "#f1dda0", color: "#302714" }
          : undefined
      }
    >
      {segment.text}
    </Text>
  ));
  const highlightedChildren = mapTextLeaves(props.children, (text, start) =>
    segments.flatMap((segment) => {
      const from = Math.max(start, segment.start);
      const to = Math.min(
        start + text.length,
        segment.start + segment.text.length
      );
      return from < to ? (
        <Text
          key={from}
          style={
            segment.highlighted
              ? { backgroundColor: "#f1dda0", color: "#302714" }
              : undefined
          }
        >
          {text.slice(from - start, to - start)}
        </Text>
      ) : (
        []
      );
    })
  );
  // Plain evidence passages stay directly selectable, including inside sheets
  // without a toolbar. Linked prose uses the explicit mode to preserve sources.
  const linked = Boolean(props.onPress) || hasInlinePress(props.children);
  const selectable =
    Platform.OS === "ios" && associate && (selectingText || !linked);
  return (
    <View>
      {selectable ? (
        <NativeSelectionText
          key={personaId}
          target={target}
          textProps={props}
          onSelection={setSelection}
        >
          {spans}
        </NativeSelectionText>
      ) : (
        <Text
          {...props}
          selectable={
            Platform.OS === "ios" && associate ? false : props.selectable
          }
          suppressHighlighting
        >
          {annotations.length > 0 ? highlightedChildren : props.children}
        </Text>
      )}
      {selectable &&
        validSelection(target.text, selection.start, selection.end) && (
          <AnnotationButton
            title="Annotate selection"
            onPress={() => setComposing({ ...selection })}
          />
        )}
      {annotations.length > 0 && (
        <AnnotationButton
          title={`${annotations.length} ${annotations.length === 1 ? "annotation" : "annotations"}`}
          onPress={() => setReviewing(true)}
        />
      )}
      {composing && associate && (
        <AnnotationComposer
          target={target}
          start={composing.start}
          end={composing.end}
          onClose={() => {
            setComposing(null);
            setSelection({ end: 0, start: 0 });
            setSelectingText(false);
          }}
        />
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

export const AnnotatableText = (props: TextProps) => {
  const scope = useAnnotationScope();
  const personaId = useAnnotations((state) => state.personaId);
  const selectingText = useAnnotations((state) => state.selectingText);
  const text = plainText(props.children);
  if (
    !scope ||
    !text.trim() ||
    props.accessibilityRole === "header" ||
    props.accessibilityRole === "alert"
  ) {
    return <Text {...props} />;
  }
  // Exact text is part of the anchor: changed research never inherits an old highlight.
  const target = {
    blockId: text,
    scopeId: scope.id,
    scopeLabel: scope.label,
    text,
  };
  return (
    <ScopedText
      key={`${scope.id}:${text}:${personaId}:${selectingText}`}
      {...props}
      target={target}
    />
  );
};
