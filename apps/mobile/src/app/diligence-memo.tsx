// Temporary preview route for the memo. "Send to the partners" switches to the partner view.
// ?view=partner opens the partner view directly.
import { useLocalSearchParams } from "expo-router";
import { useState } from "react";

import { MemoScreen } from "../diligence/memo";
import { PartnerScreen } from "../diligence/partner";

export default function DiligenceMemoPreview() {
  const { view } = useLocalSearchParams<{ view?: string }>();
  const [sent, setSent] = useState(view === "partner");
  return sent ? <PartnerScreen /> : <MemoScreen onSend={() => setSent(true)} />;
}
