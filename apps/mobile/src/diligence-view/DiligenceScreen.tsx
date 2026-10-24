import { View } from "react-native";

import { Body, useReadoutColors } from "../readout/ui";

export default function DiligenceScreen() {
  const colors = useReadoutColors();
  return (
    <View
      style={{
        backgroundColor: colors.bg,
        flex: 1,
        justifyContent: "center",
        padding: 24,
      }}
    >
      <Body>The Diligence view is on the web build. Open Tricorder in a browser to use it.</Body>
    </View>
  );
}
