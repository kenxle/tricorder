import assert from "node:assert/strict";
import { test } from "node:test";

import { createElement } from "react";

import {
  hasInlinePress,
  mapTextLeaves,
  plainText,
} from "../src/annotations/rich-text.ts";

test("annotation text keeps inline citation offsets and ignores empty nodes", () => {
  const children = [
    "A claim.",
    null,
    createElement("text", { key: "source" }, " ", "[", 25, "]"),
    false,
    " Next claim.",
  ];
  assert.equal(plainText(children), "A claim. [25] Next claim.");
  const leaves = [];
  const mapped = mapTextLeaves(children, (text, start) => {
    leaves.push([text, start]);
    return text;
  });
  assert.equal(plainText(mapped), plainText(children));
  assert.deepEqual(leaves, [
    ["A claim.", 0],
    [" ", 8],
    ["[", 9],
    ["25", 10],
    ["]", 12],
    [" Next claim.", 13],
  ]);
});

test("highlight mapping preserves nested source actions, labels, keys and styles", () => {
  let opened = 0;
  const onPress = () => {
    opened += 1;
  };
  const style = { color: "gold" };
  const children = createElement(
    "text",
    { key: "paragraph", style },
    "A claim.",
    createElement(
      "pressable",
      { accessibilityLabel: "Evidence 25", key: "citation", onPress },
      createElement("text", null, "[25]")
    )
  );
  assert.equal(hasInlinePress(children), true);
  assert.equal(hasInlinePress(["Plain prose", null]), false);
  const mapped = mapTextLeaves(children, (text, start) =>
    createElement("highlight", { key: start }, text)
  );
  assert.equal(plainText(mapped), "A claim.[25]");
  assert.equal(mapped.key, "paragraph");
  assert.equal(mapped.props.style, style);
  const [, citation] = mapped.props.children;
  assert.equal(citation.key, "citation");
  assert.equal(citation.props.accessibilityLabel, "Evidence 25");
  assert.equal(citation.props.onPress, onPress);
  citation.props.onPress();
  assert.equal(opened, 1);
  assert.equal(hasInlinePress(mapped), true);
});

test("inserted source attachments preserve existing prose anchors and selection offsets", () => {
  const citation = createElement(
    "pressable",
    {
      key: "citation",
      nativeID: "source-citation:ploy:pricing:0",
      onPress: () => {},
    },
    createElement("text", null, " [25]")
  );
  const children = ["A claim.", citation, " Next claim."];
  const original = "A claim. Next claim.";
  assert.equal(plainText(children), original);
  const leaves = [];
  const mapped = mapTextLeaves(children, (text, start) => {
    leaves.push([text, start]);
    return createElement("highlight", { key: start }, text);
  });
  assert.equal(plainText(mapped), original);
  assert.deepEqual(leaves, [
    ["A claim.", 0],
    [" Next claim.", 8],
  ]);
  const [, mappedCitation] = mapped;
  assert.equal(mappedCitation, citation);
  assert.equal(hasInlinePress(mapped), true);
});
