import { defineCatalog, defineSchema } from "@json-render/core";
import type { JsonPatch, Spec, UIElement } from "@json-render/core";
import { z } from "zod";

import type { RequestItem } from "./model.ts";

export const requestQuerySchema = z.strictObject({
  company: z
    .string()
    .min(1)
    .max(100)
    .regex(/^[a-z0-9][a-z0-9-]*$/u),
  stage: z.enum(["pre_seed", "seed", "series_a"]),
});

export const itemID = z
  .string()
  .regex(/^(?:C\d+|custom-[a-zA-Z0-9-]+)$/u)
  .max(100);
const text = z.string().max(20_000);
export const requestItemSchema = z.strictObject({
  ask: text,
  checked: z.boolean(),
  guidance: text,
  id: itemID,
  reason: text,
  title: text,
});
export const requestFormSchema = z.strictObject({
  custom: z.string().max(2000),
  customItems: z.array(requestItemSchema).max(50),
  editedDraft: text.nullable(),
  selected: z.record(itemID, z.boolean()),
});

const componentProps = {
  RequestButton: z.strictObject({
    kind: z.enum(["add", "regenerate", "copy", "save"]),
    label: text,
  }),
  RequestColumn: z.strictObject({}),
  RequestCustomItems: z.strictObject({}),
  RequestInput: z.strictObject({
    field: z.enum(["custom", "draft"]),
    label: text,
    value: text.nullable(),
  }),
  RequestNote: z.strictObject({ text }),
  RequestStatus: z.strictObject({}),
  RequestToggle: z.strictObject({
    checked: z.boolean(),
    item: requestItemSchema,
  }),
};

// Platform-neutral catalog: only the mobile registry imports React Native.
const schema = defineSchema((s) => ({
  catalog: s.object({
    components: s.map({ description: s.string(), props: s.zod() }),
  }),
  spec: s.object({
    elements: s.record(
      s.object({
        children: s.array(s.string()),
        props: s.propsOf("catalog.components"),
        type: s.ref("catalog.components"),
      })
    ),
    root: s.string(),
  }),
}));

export const requestCatalog = defineCatalog(schema, {
  components: {
    RequestButton: {
      description: "An installed request action",
      props: componentProps.RequestButton,
    },
    RequestColumn: {
      description: "Request form layout",
      props: componentProps.RequestColumn,
    },
    RequestCustomItems: {
      description: "Operator-added request items",
      props: componentProps.RequestCustomItems,
    },
    RequestInput: {
      description: "Custom item or editable draft",
      props: componentProps.RequestInput,
    },
    RequestNote: {
      description: "Request guidance",
      props: componentProps.RequestNote,
    },
    RequestStatus: {
      description: "Local action result",
      props: componentProps.RequestStatus,
    },
    RequestToggle: {
      description: "Select a requested document",
      props: componentProps.RequestToggle,
    },
  },
});

const binding = (path: string) => ({ $bindState: path });
const leaf = (type: string, props: Record<string, unknown>): UIElement => ({
  children: [],
  props,
  type,
});

export const createRequestSpec = (items: RequestItem[]): Spec => {
  const elements: Record<string, UIElement> = {
    intro: leaf("RequestNote", {
      text: "Check what you need, add anything missing, then copy the draft into your own email.",
    }),
    request: { children: [], props: {}, type: "RequestColumn" },
  };
  const children = ["intro"];
  for (const item of items) {
    const parsed = requestItemSchema.parse(item);
    const id = `item-${parsed.id}`;
    elements[id] = leaf("RequestToggle", {
      checked: binding(`/selected/${parsed.id}`),
      item: parsed,
    });
    children.push(id);
  }
  const footer: Record<string, UIElement> = {
    add: leaf("RequestButton", { kind: "add", label: "Add to request" }),
    copy: leaf("RequestButton", { kind: "copy", label: "Copy request" }),
    custom: leaf("RequestInput", {
      field: "custom",
      label: "Add an item",
      value: binding("/custom"),
    }),
    customItems: leaf("RequestCustomItems", {}),
    draft: leaf("RequestInput", {
      field: "draft",
      label: "Draft message",
      value: binding("/editedDraft"),
    }),
    guidance: leaf("RequestNote", {
      text: "The draft updates with your selections until you edit it. Nothing is sent from this screen.",
    }),
    regenerate: leaf("RequestButton", {
      kind: "regenerate",
      label: "Regenerate from selected items",
    }),
    save: leaf("RequestButton", {
      kind: "save",
      label: "Save draft on this device",
    }),
    status: leaf("RequestStatus", {}),
  };
  Object.assign(elements, footer);
  elements.request.children = [
    ...children,
    "customItems",
    "custom",
    "add",
    "guidance",
    "regenerate",
    "draft",
    "copy",
    "save",
    "status",
  ];
  return { elements, root: "request" };
};

export const requestSpecPatches = (items: RequestItem[]): JsonPatch[] => {
  const spec = createRequestSpec(items);
  const patches: JsonPatch[] = [
    { op: "add", path: "/root", value: spec.root },
    {
      op: "add",
      path: "/elements/request",
      value: { children: [], props: {}, type: "RequestColumn" },
    },
  ];
  const children: string[] = [];
  for (const id of spec.elements.request.children ?? []) {
    patches.push({
      op: "add",
      path: `/elements/${id}`,
      value: spec.elements[id],
    });
    children.push(id);
    patches.push({
      op: "replace",
      path: "/elements/request/children",
      value: [...children],
    });
  }
  return patches;
};

const elementSchema = z.strictObject({
  children: z.array(z.string().regex(/^[a-zA-Z0-9-]+$/u)).max(250),
  props: z.record(z.string(), z.unknown()),
  type: z.enum(
    Object.keys(componentProps) as [
      keyof typeof componentProps,
      ...(keyof typeof componentProps)[],
    ]
  ),
});

// Validate the only bindings and layout operations this catalog permits. Streams
// cannot write form state, execute code, navigate, or select arbitrary actions.
export const validateRequestElement = (value: unknown): UIElement => {
  const element = elementSchema.parse(value);
  const props = { ...element.props };
  if (element.type === "RequestToggle") {
    const item = requestItemSchema.parse(props.item);
    z.strictObject({ $bindState: z.literal(`/selected/${item.id}`) }).parse(
      props.checked
    );
    props.checked = item.checked;
  }
  if (element.type === "RequestInput") {
    const path = props.field === "custom" ? "/custom" : "/editedDraft";
    z.strictObject({ $bindState: z.literal(path) }).parse(props.value);
    props.value = null;
  }
  componentProps[element.type].parse(props);
  if (element.type !== "RequestColumn" && element.children.length) {
    throw new Error("Request controls cannot contain children.");
  }
  return element;
};
