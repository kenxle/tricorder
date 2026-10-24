import { z } from "zod";

export interface Persona {
  id: string;
  name: string;
  role: "associate" | "gp";
}

// Fictional identities for the on-device collaboration demo.
export const personas: readonly Persona[] = [
  { id: "maya", name: "Maya Chen", role: "associate" },
  { id: "alex", name: "Alex Rivera", role: "associate" },
  { id: "jordan", name: "Jordan Lee", role: "gp" },
];

export interface AnnotationTarget {
  scopeId: string;
  scopeLabel: string;
  blockId: string;
  text: string;
}

export interface Annotation {
  id: string;
  target: AnnotationTarget;
  start: number;
  end: number;
  quote: string;
  comment: string;
  authorId: string;
  createdAt: string;
}

export interface AnnotationInput {
  target: AnnotationTarget;
  start: number;
  end: number;
  comment: string;
}

const isTextBoundary = (text: string, offset: number): boolean => {
  if (offset === 0 || offset === text.length) {
    return true;
  }
  const before = text.codePointAt(offset - 1);
  return before === undefined || before <= 0xff_ff;
};

export const validSelection = (
  text: string,
  start: number,
  end: number
): boolean =>
  Number.isInteger(start) &&
  Number.isInteger(end) &&
  start >= 0 &&
  end > start &&
  end <= text.length &&
  isTextBoundary(text, start) &&
  isTextBoundary(text, end) &&
  text.slice(start, end).trim().length > 0;

const targetSchema = z.strictObject({
  blockId: z.string().min(1),
  scopeId: z.string().min(1),
  scopeLabel: z.string().trim().min(1),
  text: z.string().min(1),
});

export const annotationInputSchema = z
  .strictObject({
    comment: z.string().trim().min(1).max(10_000),
    end: z.number().int(),
    start: z.number().int(),
    target: targetSchema,
  })
  .refine(({ target, start, end }) => validSelection(target.text, start, end));

const annotationSchema = z
  .strictObject({
    authorId: z
      .string()
      .refine((id) =>
        personas.some(
          (persona) => persona.id === id && persona.role === "associate"
        )
      ),
    comment: z.string().trim().min(1).max(10_000),
    createdAt: z.iso.datetime(),
    end: z.number().int(),
    id: z.string().min(1),
    quote: z.string().min(1),
    start: z.number().int(),
    target: targetSchema,
  })
  .refine(
    ({ target, start, end, quote }) =>
      validSelection(target.text, start, end) &&
      target.text.slice(start, end) === quote
  );

export const savedAnnotationsSchema = z
  .strictObject({
    annotations: z.array(annotationSchema),
    personaId: z
      .string()
      .refine((id) => personas.some((persona) => persona.id === id)),
    version: z.literal(1),
  })
  .refine(
    ({ annotations }) =>
      new Set(annotations.map(({ id }) => id)).size === annotations.length
  );

export interface HighlightSegment {
  start: number;
  end: number;
  text: string;
  highlighted: boolean;
  annotationIds: string[];
}

// Callers filter by scope/block first. Exact text matching keeps old annotations
// attached to their captured snapshot instead of highlighting changed evidence.
export const highlightSegments = (
  text: string,
  annotations: readonly Annotation[]
): HighlightSegment[] => {
  const matching = annotations.filter(
    (annotation) =>
      annotation.target.text === text &&
      validSelection(text, annotation.start, annotation.end) &&
      text.slice(annotation.start, annotation.end) === annotation.quote
  );
  const boundaries = [
    ...new Set([
      0,
      text.length,
      ...matching.flatMap(({ start, end }) => [start, end]),
    ]),
  ];
  // Hermes in the iPhone development client does not implement Array.toSorted.
  // oxlint-disable-next-line unicorn/no-array-sort
  boundaries.sort((a, b) => a - b);
  return boundaries.slice(0, -1).map((start, index) => {
    const end = boundaries[index + 1];
    const annotationIds = matching
      .filter((annotation) => annotation.start < end && annotation.end > start)
      .map(({ id }) => id);
    return {
      annotationIds,
      end,
      highlighted: annotationIds.length > 0,
      start,
      text: text.slice(start, end),
    };
  });
};

export const annotationsForTarget = (
  annotations: readonly Annotation[],
  target: AnnotationTarget
): Annotation[] =>
  annotations.filter(
    (annotation) =>
      annotation.target.scopeId === target.scopeId &&
      annotation.target.blockId === target.blockId &&
      annotation.target.text === target.text
  );
