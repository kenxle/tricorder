import type { Spec } from "@json-render/core";
import { z } from "zod";

import { createRequestSpec, validateRequestElement } from "./catalog.ts";

const patchSchema = z.strictObject({
  op: z.enum(["add", "replace"]),
  path: z.string(),
  value: z.unknown(),
});
const childSchema = z.array(z.string().regex(/^[a-zA-Z0-9-]+$/u)).max(250);
const elementPath = /^\/elements\/(?<id>[a-zA-Z0-9-]+)$/u;
const MAX_BYTES = 1_000_000;

export const applyRequestPatch = (spec: Spec, input: unknown): Spec => {
  const patch = patchSchema.parse(input);
  if (
    patch.path === "/root" &&
    patch.op === "add" &&
    patch.value === "request"
  ) {
    return { ...spec, root: "request" };
  }
  if (patch.path === "/elements/request/children" && patch.op === "replace") {
    const children = childSchema.parse(patch.value);
    if (
      !spec.elements.request ||
      new Set(children).size !== children.length ||
      children.some(
        (id) => id === "request" || !Object.hasOwn(spec.elements, id)
      )
    ) {
      throw new Error("Invalid request layout references.");
    }
    return {
      ...spec,
      elements: {
        ...spec.elements,
        request: { ...spec.elements.request, children },
      },
    };
  }
  const match = elementPath.exec(patch.path);
  if (!match?.groups?.id || patch.op !== "add") {
    throw new Error("Unsupported request layout update.");
  }
  const { id } = match.groups;
  if (["__proto__", "prototype", "constructor"].includes(id)) {
    throw new Error("Invalid request element identity.");
  }
  const element = validateRequestElement(patch.value);
  if (
    (id === "request") !== (element.type === "RequestColumn") ||
    element.children?.length
  ) {
    throw new Error("Invalid request layout structure.");
  }
  return { ...spec, elements: { ...spec.elements, [id]: element } };
};

// Required controls must be present with their installed meanings before success.
const requiredElements = createRequestSpec([]).elements;
const completeRequestSpec = (spec: Spec): boolean => {
  if (
    spec.root !== "request" ||
    spec.elements.request?.type !== "RequestColumn"
  ) {
    return false;
  }
  const children = spec.elements.request.children ?? [];
  return Object.entries(requiredElements).every(([id, expected]) => {
    const actual = spec.elements[id];
    return (
      actual?.type === expected.type &&
      (id === "request" || children.includes(id)) &&
      actual.props.kind === expected.props.kind &&
      actual.props.field === expected.props.field
    );
  });
};

export const readRequestStream = async (
  body: ReadableStream<Uint8Array>,
  onSpec: (spec: Spec) => void,
  signal: AbortSignal
): Promise<Spec> => {
  const reader = body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let bytes = 0;
  let spec: Spec = { elements: {}, root: "" };
  const abort = () => {
    void reader.cancel().catch(() => null);
  };
  signal.addEventListener("abort", abort, { once: true });
  const accept = (line: string) => {
    if (!line.trim()) {
      return;
    }
    spec = applyRequestPatch(spec, JSON.parse(line));
    if (spec.elements.request) {
      onSpec(spec);
    }
  };
  const readNext = async (): Promise<void> => {
    if (signal.aborted) {
      throw new Error("Request layout cancelled.");
    }
    const { done, value } = await reader.read();
    if (signal.aborted) {
      throw new Error("Request layout cancelled.");
    }
    if (done) {
      return;
    }
    bytes += value.byteLength;
    if (bytes > MAX_BYTES) {
      throw new Error("Request layout exceeds its size limit.");
    }
    buffer += decoder.decode(value, { stream: true });
    let newline = buffer.indexOf("\n");
    while (newline !== -1) {
      accept(buffer.slice(0, newline));
      buffer = buffer.slice(newline + 1);
      newline = buffer.indexOf("\n");
    }
    await readNext();
  };
  try {
    await readNext();
    buffer += decoder.decode();
    if (buffer.trim()) {
      accept(buffer);
    }
    if (!completeRequestSpec(spec)) {
      throw new Error("Request layout ended before it was complete.");
    }
    return spec;
  } finally {
    signal.removeEventListener("abort", abort);
    await reader.cancel().catch(() => null);
    reader.releaseLock();
  }
};
