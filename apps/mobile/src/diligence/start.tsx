// "Diligence on whom?": one box for a company URL. Dropping in the URL starts the research.
import { useState } from "react";
import { View } from "react-native";

import { Action, Field, Heading } from "../readout/ui";

export const DEMO_URL = "https://www.sazabi.com/";

export function StartScreen({ onStart }: { onStart: (url: string) => void }) {
  const [url, setUrl] = useState(DEMO_URL);
  return (
    <View style={{ gap: 16, paddingVertical: 32 }}>
      <Heading style={{ fontSize: 34, lineHeight: 40 }}>Diligence on whom?</Heading>
      <Field
        label="Company URL"
        value={url}
        onChangeText={setUrl}
        placeholder="Its website or its YC page"
        autoCapitalize="none"
        autoCorrect={false}
        keyboardType="url"
        onSubmitEditing={() => url.trim() && onStart(url.trim())}
      />
      <Action title="Start" primary disabled={!url.trim()} onPress={() => onStart(url.trim())} />
    </View>
  );
}
