import { useState } from "react";
import { Linking } from "react-native";

import { AnnotationScope, useAnnotationScope } from "../annotations/context";
import { Action, Body, Card, Heading, Note } from "../readout/ui";
import { data } from "./data";
import { safeWebUrl } from "./model";
import type { ResearchClaim } from "./model";

export const EvidenceContent = ({ claim }: { claim: ResearchClaim }) => {
  const parentScope = useAnnotationScope() ?? {
    id: "company-evidence",
    label: "Company evidence",
  };
  const [error, setError] = useState("");
  const source = claim.source ? data.sources[claim.source] : undefined;
  const url = safeWebUrl(claim.url ?? source?.url ?? "");
  const openSource = async () => {
    if (!url) {
      return;
    }
    try {
      await Linking.openURL(url);
    } catch {
      setError("Could not open this source. You can copy the URL below.");
    }
  };
  return (
    <AnnotationScope
      id={`${parentScope.id}/source:${claim.source ?? claim.url ?? claim.text}`}
      label={`${parentScope.label} · ${source?.title ?? "Source"}`}
    >
      <Note>PUBLIC SOURCE · SAVED SNAPSHOT</Note>
      <Heading>{source?.title ?? "Source unavailable"}</Heading>
      <Body>{claim.text}</Body>
      {claim.excerpt ? (
        <Card>
          <Note>{claim.excerpt.before}</Note>
          <Body style={{ fontWeight: "600" }}>{claim.excerpt.match}</Body>
          <Note>{claim.excerpt.after}</Note>
        </Card>
      ) : null}
      {!claim.excerpt && claim.quote ? (
        <Card>
          <Body>{claim.quote}</Body>
        </Card>
      ) : null}
      {!claim.excerpt && !claim.quote && (
        <Note>No excerpt is included in this saved record.</Note>
      )}
      {url && (
        <>
          <Action title="Open original source ↗" onPress={openSource} />
          <Note>{url}</Note>
        </>
      )}
      {error ? <Body accessibilityRole="alert">{error}</Body> : null}
      <Note>Saved research: {data.built.replace("T", " ")}</Note>
    </AnnotationScope>
  );
};
