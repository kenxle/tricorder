import { createElement, isValidElement } from "react";
import type { ReactNode } from "react";

const isSourceCitation = (node: ReactNode): boolean =>
  isValidElement<{ nativeID?: string }>(node) &&
  node.props.nativeID?.startsWith("source-citation:") === true;

export const plainText = (children: ReactNode): string => {
  // Source markers are attachments, not changes to the annotated prose.
  if (isSourceCitation(children)) {
    return "";
  }
  if (typeof children === "string" || typeof children === "number") {
    return String(children);
  }
  if (Array.isArray(children)) {
    return children.map(plainText).join("");
  }
  return isValidElement<{ children?: ReactNode }>(children)
    ? plainText(children.props.children)
    : "";
};

export const hasInlinePress = (children: ReactNode): boolean => {
  if (Array.isArray(children)) {
    return children.some(hasInlinePress);
  }
  return (
    isValidElement<{ children?: ReactNode; onPress?: unknown }>(children) &&
    (typeof children.props.onPress === "function" ||
      hasInlinePress(children.props.children))
  );
};

// Keep links, accessibility props and formatting while mapping text at offsets
// in the same flattened string used by the annotation anchor.
export const mapTextLeaves = (
  children: ReactNode,
  render: (text: string, start: number) => ReactNode
): ReactNode => {
  let offset = 0;
  const visit = (node: ReactNode): ReactNode => {
    if (isSourceCitation(node)) {
      return node;
    }
    if (typeof node === "string" || typeof node === "number") {
      const text = String(node);
      const start = offset;
      offset += text.length;
      return render(text, start);
    }
    if (Array.isArray(node)) {
      return node.map(visit);
    }
    return isValidElement<{ children?: ReactNode }>(node)
      ? createElement(
          node.type,
          { ...node.props, key: node.key },
          visit(node.props.children)
        )
      : node;
  };
  return visit(children);
};
